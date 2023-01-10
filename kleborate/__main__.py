"""
Copyright 2023 Kat Holt
Copyright 2023 Ryan Wick (rrwick@gmail.com)
https://github.com/katholt/Kleborate/

This file is part of Kleborate. Kleborate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kleborate is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kleborate. If
not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import gzip
import importlib
import os
import pathlib
import shutil
import sys
import tempfile
import textwrap
import uuid

from .help_formatter import MyParser, MyHelpFormatter
from .misc import get_compression_type, load_fasta
from .version import __version__


def parse_arguments(args, all_module_names, modules):
    parser = MyParser(description='Kleborate: a tool for characterising virulence and resistance '
                                  'in pathogen assemblies',
                      formatter_class=MyHelpFormatter, add_help=False, epilog=paper_refs())

    if '--helpall' in sys.argv or '--allhelp' in sys.argv or '--all_help' in sys.argv:
        sys.argv.append('--help_all')

    io_args = parser.add_argument_group('Input/output')
    io_args.add_argument('-a', '--assemblies', nargs='+', type=str, required=True,
                         help='FASTA file(s) for assemblies')
    io_args.add_argument('-o', '--outfile', type=str, default='Kleborate_results.txt',
                         help='File for detailed output (default: Kleborate_results.txt)')

    module_args = parser.add_argument_group('Modules')
    module_args.add_argument('-p', '--preset', type=str,
                             help=f'Module presets, choose from: ' + ', '.join(get_presets()))
    module_args.add_argument('-m', '--modules', type=str,
                             help='Comma-delimited list of Kleborate modules to use')

    add_module_cli_arguments(parser, all_module_names, modules)

    help_args = parser.add_argument_group('Help')
    help_args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                           help='Show this help message and exit')
    help_args.add_argument('--help_all', action='help',
                           help='Show a help message with all module options')
    help_args.add_argument('--version', action='version', version='Kleborate v' + __version__,
                           help="Show program's version number and exit")

    if len(sys.argv) == 1:  # if no arguments were used
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    return parser.parse_args(args)


def main():
    all_module_names, modules = import_modules()
    args = parse_arguments(sys.argv[1:], all_module_names, modules)
    module_names = get_used_module_names(args, all_module_names, get_presets())
    check_modules(args, modules, module_names)
    check_assemblies(args)

    full_headers, stdout_headers = get_headers(module_names, modules)
    output_headers(full_headers, stdout_headers, args.outfile)

    for assembly in args.assemblies:
        with tempfile.TemporaryDirectory() as tmp_dir:
            unzipped_assembly = gunzip_assembly_if_necessary(assembly, tmp_dir)
            results = {'assembly': assembly}
            for m in module_names:
                results.update(modules[m].get_results(unzipped_assembly, args))
            output_results(full_headers, stdout_headers, args.outfile, results)


def get_presets():
    """
    This function defines the module presets. The keys are the valid choices for the --preset
    option, and the values are a list of modules for the preset.
    """
    return {'klebsiella': ['contig_stats', 'klebsiella_species'],
            'escherichia': ['contig_stats']}


def add_module_cli_arguments(parser, all_module_names, modules):
    """
    This function add CLI argument for modules. Each modules that has options gets its own argument
    group. These are only displayed in the help text if the user used --help_all, otherwise they
    are hidden.
    """
    for m in all_module_names:
        group = modules[m].add_cli_options(parser)
        if '--help_all' not in sys.argv and group is not None:
            for a in group._group_actions:
                a.help = argparse.SUPPRESS


def get_used_module_names(args, all_module_names, presets):
    """
    Returns a list of the modules names used in this run of Kleborate. The user can select modules
    using --preset (pre-selected modules for a taxon), --modules (listing every module) or both
    (preset modules plus additional user-selected modules).
    """
    if args.preset is None and args.modules is None:
        sys.exit('Error: either --preset or --modules is required')
    module_names = []
    if args.preset:
        if args.preset not in presets:
            sys.exit(f'Error: {args.preset} is not a valid preset')
        module_names += presets[args.preset]
    if args.modules:
        for m in args.modules.split(','):
            if m not in all_module_names:
                sys.exit(f'Error: {m} is not a valid module name')
            if m not in module_names:
                module_names.append(m)
    return module_names


def get_all_module_names():
    """
    Looks for all Kleborate modules and returns their names. To qualify as a module, it must be in
    the 'modules' directory, in a subdirectory that matches the filename. For example:
    * modules/contig_stats/contig_stats.py  <- is a module
    * modules/kpsc_mlst/kpsc_mlst.py  <- is a module
    * modules/contig_stats/test.py  <- not a module
    """
    module_dir = pathlib.Path(__file__).parents[0] / 'modules'
    module_names = []
    for module_file in module_dir.glob('*/*.py'):
        dir_name = module_file.parts[-2]
        if module_file.parts[-1][:-3] == dir_name:
            module_names.append(dir_name)
    if 'template' in module_names:
        module_names.remove('template')
    return module_names


def import_modules():
    """
    This function imports all modules (whether or not they are used in this run of Kleborate).
    """
    all_module_names = get_all_module_names()
    modules = {}
    for m in all_module_names:
        modules[m] = importlib.import_module(f'..modules.{m}.{m}', __name__)
    return all_module_names, modules


def check_modules(args, modules, module_names):
    """
    This function checks the options and external requirements of the used modules.
    """
    for m in module_names:
        modules[m].check_cli_options(args)
        modules[m].check_external_programs()


def check_assemblies(args):
    """
    This function does a quick check to make sure that the input assemblies look good.
    """
    for assembly in args.assemblies:
        if os.path.isdir(assembly):
            sys.exit('Error: ' + assembly + ' is a directory (please specify assembly files)')
        if not os.path.isfile(assembly):
            sys.exit('Error: could not find ' + assembly)
        fasta = load_fasta(assembly)
        if len(fasta) < 1:
            sys.exit('Error: invalid FASTA file: ' + assembly)
        for _, seq in fasta:
            if len(seq) == 0:
                sys.exit('Error: invalid FASTA file (contains a zero-length sequence): ' + assembly)


def get_headers(module_names, modules):
    """
    This function returns two lists of headers:
    * full_headers: will be used in Kleborate's output file.
    * stdout_headers: will be displayed in Kleborate's stdout
    Each used module contributes headers to these lists.
    """
    full_headers, stdout_headers = ['assembly'], ['assembly']
    for m in module_names:
        module_full, module_stdout = modules[m].get_headers()
        full_headers += module_full
        stdout_headers += module_stdout
        assert len(full_headers) == len(set(full_headers))  # duplicates not allowed
        assert len(stdout_headers) == len(set(stdout_headers))  # duplicates not allowed
    return full_headers, stdout_headers


def gunzip_assembly_if_necessary(assembly, temp_dir):
    if get_compression_type(assembly) == 'gz':
        unzipped_assembly = str(temp_dir) + '/' + uuid.uuid4().hex + '.fasta'
        decompress_file(assembly, unzipped_assembly)
        return unzipped_assembly
    else:
        return assembly


def decompress_file(in_file, out_file):
    with gzip.GzipFile(in_file, 'rb') as i, open(out_file, 'wb') as o:
        s = i.read()
        o.write(s)


def output_headers(full_headers, stdout_headers, outfile):
    print('\t'.join(stdout_headers))
    with open(outfile, 'wt') as o:
        o.write('\t'.join(full_headers))
        o.write('\n')


def output_results(full_headers, stdout_headers, outfile, results):
    print('\t'.join([results[x] for x in stdout_headers]))
    with open(outfile, 'at') as o:
        o.write('\t'.join([results[x] for x in full_headers]))
        o.write('\n')

    # Double check that there weren't any results without a corresponding output header.
    for h in results.keys():
        if h not in full_headers:
            sys.exit(f'Error: results contained a value ({h}) that is not covered by the output '
                     f'headers')


def paper_refs():
    terminal_width = shutil.get_terminal_size().columns
    text = 'If you use Kleborate, please cite the paper:\n' \
           'Lam MMC, et al. A genomic surveillance framework and genotyping tool for Klebsiella ' \
           'pneumoniae and its related species complex. Nature Communications. 2021. ' \
           'doi:10.1038/s41467-021-24448-3.\n\n' \
           'If you turn on the Kaptive option for full K and O typing, please also cite:\n' \
           'Wyres KL, et al. Identification of Klebsiella capsule synthesis loci from whole ' \
           'genome data. Microbial Genomics. 2016. doi:10.1099/mgen.0.000102.'
    wrapped_text = ''
    for line in text.split('\n'):
        wrapped_text += '\n'.join(textwrap.wrap(line, width=terminal_width - 1))
        wrapped_text += '\n'
    return 'R|' + wrapped_text


if __name__ == '__main__':
    main()
