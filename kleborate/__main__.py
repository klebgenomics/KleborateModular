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
import sys
import tempfile

from .help_formatter import MyParser, MyHelpFormatter
from .misc import get_compression_type, load_fasta
from .version import __version__


def parse_arguments():
    parser = MyParser(description='Kleborate: a tool for characterising virulence and resistance '
                                  'in pathogen assemblies',
                      formatter_class=MyHelpFormatter, add_help=False,
                      epilog='R|If you use Kleborate, please cite the paper:\nLam MMC, et al. A '
                             'genomic surveillance framework and genotyping tool for Klebsiella '
                             'pneumoniae and its related species complex. Nature Communications. '
                             '2021. doi:10.1038/s41467-021-24448-3.\n\n'
                             'If you turn on the Kaptive option for full K and O typing, please '
                             'also cite:\nWyres KL, et al. Identification of Klebsiella capsule '
                             'synthesis loci from whole genome data. Microbial Genomics. 2016. '
                             'doi:10.1099/mgen.0.000102.')

    io_args = parser.add_argument_group('Input/output')
    io_args.add_argument('-a', '--assemblies', nargs='+', type=str, required=True,
                         help='FASTA file(s) for assemblies')
    io_args.add_argument('-o', '--outfile', type=str, default='Kleborate_results.txt',
                         help='File for detailed output (default: Kleborate_results.txt)')

    module_args = parser.add_argument_group('Modules')
    module_args.add_argument('-m', '--modules', type=str,
                             help='Comma-delimited list of Kleborate modules to use')
    module_args.add_argument('-p', '--preset', type=str,
                             help='Module presets')

    # TODO: ADD MODULE OPTIONS HERE

    help_args = parser.add_argument_group('Help')
    help_args.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                           help='Show this help message and exit')
    help_args.add_argument('--version', action='version', version='Kleborate v' + __version__,
                           help="Show program's version number and exit")

    # If no arguments were used, print the entire help (argparse default is to just give an error
    # like '-a is required').
    if len(sys.argv) == 1:
        parser.print_help(file=sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    check_args(args)
    module_names, modules = import_modules(args)
    check_assembles(args)

    full_headers, stdout_headers = get_headers(module_names, modules)
    output_headers(full_headers, stdout_headers, args.outfile)

    for assembly in args.assemblies:
        with tempfile.TemporaryDirectory() as tmp_dir:
            unzipped_assembly = gunzip_contigs_if_necessary(assembly, tmp_dir)
            results = {'assembly': assembly}
            for m in module_names:
                results.update(modules[m].get_results(unzipped_assembly))
            output_results(full_headers, stdout_headers, args.outfile, results)


def check_args(args):
    if args.modules is None and args.preset is None:
        sys.exit('Error: either --modules or --preset is required')


def import_modules(args):
    module_names = args.modules.split(',')
    modules = {}
    for m in module_names:
        modules[m] = importlib.import_module(f'..modules.{m}.{m}', __name__)
    return module_names, modules


def check_assembles(args):
    for assembly in args.assemblies:
        if os.path.isdir(assembly):
            sys.exit('Error: ' + assembly + ' is a directory (please specify assembly files)')
        if not os.path.isfile(assembly):
            sys.exit('Error: could not find ' + assembly)
        fasta = load_fasta(assembly)
        if len(fasta) < 1:
            sys.exit('Error: invalid FASTA file: ' + assembly)
        for header, seq in fasta:
            if len(header) == 0:
                sys.exit('Error: invalid FASTA file (contains a zero-length header): ' + assembly)
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


def gunzip_contigs_if_necessary(contigs, temp_dir):
    if get_compression_type(contigs) == 'gz':
        new_contigs = str(temp_dir) + '/' + get_strain_name(contigs) + '.fasta'
        decompress_file(contigs, new_contigs)
        return new_contigs
    else:
        return contigs


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


def get_strain_name(full_path):
    filename = os.path.split(full_path)[1]
    if filename.endswith('_temp_decompress.fasta'):
        filename = filename[:-22]
    if filename.endswith('.gz'):
        filename = filename[:-3]
    return os.path.splitext(filename)[0]


if __name__ == '__main__':
    main()
