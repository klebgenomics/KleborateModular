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

import os
import pathlib
import shutil
import sys

from ...shared.resMinimap import read_class_file, get_res_headers, resminimap_assembly


def description():
    return 'Genotyping acquired genes and mutations for the Klebsiella pneumoniae species complex'


def prerequisite_modules():
    return []


def get_headers():
    _, res_classes, bla_classes = read_class_file(data_dir() / 'CARD_AMR_clustered.csv')
    res_headers = get_res_headers(res_classes, bla_classes)
    res_headers += ['truncated_resistance_hits', 'spurious_resistance_hits']
    full_headers = res_headers
    stdout_headers = []
    return full_headers, stdout_headers



def add_cli_options(parser):
    module_name = os.path.basename(__file__)[:-3]
    group = parser.add_argument_group(f'{module_name} module')

    group.add_argument('--min_identity', type=float, default=90.0,
                       help='Minimum alignment percent identity for main results')
    group.add_argument('--min_coverage', type=float, default=80.0,
                       help='Minimum alignment percent coverage for main results')
    group.add_argument('--min_spurious_identity', type=float, default=80.0,
                       help='Minimum alignment percent identity for spurious results')
    group.add_argument('--min_spurious_coverage', type=float, default=40.0,
                       help='Minimum alignment percent coverage for spurious results')
    
    return group


def check_cli_options(args):
    if args.min_identity <= 50.0 or args.min_identity >= 100.0:
        sys.exit('Error: --min_identity must be between 50.0 and 100.0')
    if args.min_coverage <= 50.0 or args.min_coverage >= 100.0:
        sys.exit('Error: --min_coverage must be between 50.0 and 100.0')
    if args.min_spurious_identity <= 50.0 or args.min_spurious_identity >= 100.0:
        sys.exit('Error: --min_spurious_identity must be between 50.0 and 100.0')
    if args.min_spurious_coverage <= 30.0 or args.min_spurious_coverage >= 100.0:
        sys.exit('Error: --min_spurious__coverage  must be between 40.0 and 100.0')


def check_external_programs():
    if not shutil.which('minimap2'):
        sys.exit('Error: could not find minimap2')
    return ['minimap2']


def data_dir():
    return pathlib.Path(__file__).parents[0] / 'data'



def get_results(assembly, minimap2_index, args, previous_results):
    gene_info, _, _ = read_class_file(data_dir() / 'CARD_AMR_clustered.csv')
    full_headers, _ = get_headers() 
    qrdr = data_dir() / 'QRDR_120.fasta'
    trunc = data_dir() / 'MgrB_and_PmrB.fasta'
    omp = data_dir() / 'OmpK.fasta'
    ref_file = data_dir() / 'CARD_v3.1.13.fasta'

    res_hits = resminimap_assembly(
        assembly, 
        ref_file, 
        gene_info, 
        qrdr, 
        trunc, 
        omp, 
        args.min_identity,  
        args.min_coverage,
        args.min_spurious_identity, 
        args.min_spurious_coverage
    )

    # Double check that there weren't any results without a corresponding output header.
    for h in res_hits.keys():
        if h not in full_headers:
            sys.exit( f'Error: results contained a value ({h}) that is not covered by the '
                      f'output headers')

    return {r: ';'.join(sorted(res_hits[r])) if r in res_hits else '-' for r in full_headers}




   

   

   






