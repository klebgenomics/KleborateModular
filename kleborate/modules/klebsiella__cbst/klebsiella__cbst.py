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

from ...shared.multi_mlst import multi_mlst


def description():
    return 'MLST on the KpSC colibactin locus (clb genes)'


def prerequisite_modules():
    return []


def get_headers():
    full_headers = ['CbST', 'cb_lineage', 'clbA', 'clbB', 'clbC', 'clbD', 'clbE', 'clbF', 'clbG',
                    'clbH', 'clbI', 'clbL', 'clbM', 'clbN', 'clbO', 'clbP', 'clbQ']
    stdout_headers = []
    return full_headers, stdout_headers


def add_cli_options(parser):
    module_name = os.path.basename(__file__)[:-3]
    group = parser.add_argument_group(f'{module_name} module')
    group.add_argument('--klebsiella__cbst_min_identity', type=float, default=90.0,
                       help='Minimum alignment percent identity for colibactin MLST')
    group.add_argument('--klebsiella__cbst_min_coverage', type=float, default=80.0,
                       help='Minimum alignment percent coverage for colibactin MLST')
    group.add_argument('--klebsiella__cbst_required_exact_matches', type=int, default=8,
                       help='At least this many exact matches are required to call an ST')
    return group


def check_cli_options(args):
    if args.klebsiella__cbst_min_identity <= 50.0 or args.klebsiella__cbst_min_identity >= 100.0:
        sys.exit('Error: --klebsiella__cbst_min_identity must be between 50.0 and 100.0')
    if args.klebsiella__cbst_min_coverage <= 50.0 or args.klebsiella__cbst_min_coverage >= 100.0:
        sys.exit('Error: --klebsiella__cbst_min_coverage must be between 50.0 and 100.0')
    if args.klebsiella__cbst_required_exact_matches < 0:
        sys.exit('Error: --cbst_required_exact_matches must be a positive integer')


def check_external_programs():
    if not shutil.which('minimap2'):
        sys.exit('Error: could not find minimap2')
    return ['minimap2']


def data_dir():
    return pathlib.Path(__file__).parents[0] / 'data'


def get_results(assembly, minimap2_index, args, previous_results):
    genes = ['clbA', 'clbB', 'clbC', 'clbD', 'clbE', 'clbF', 'clbG', 'clbH', 'clbI', 'clbL',
             'clbM', 'clbN', 'clbO', 'clbP', 'clbQ']
    profiles = data_dir() / 'profiles.tsv'
    alleles = {gene: data_dir() / f'{gene}.fasta' for gene in genes}

    st, lineage, alleles = multi_mlst(assembly, minimap2_index, profiles, alleles, genes,
                                      'clb_lineage', args.klebsiella__cbst_min_identity,
                                      args.klebsiella__cbst_min_coverage, args.klebsiella__cbst_required_exact_matches,
                                      check_for_truncation=True, report_incomplete=True)

    return {'CbST': st, 'cb_lineage': lineage,
            'clbA': alleles['clbA'], 'clbB': alleles['clbB'], 'clbC': alleles['clbC'],
            'clbD': alleles['clbD'], 'clbE': alleles['clbE'], 'clbF': alleles['clbF'],
            'clbG': alleles['clbG'], 'clbH': alleles['clbH'], 'clbI': alleles['clbI'],
            'clbL': alleles['clbL'], 'clbM': alleles['clbM'], 'clbN': alleles['clbN'],
            'clbO': alleles['clbO'], 'clbP': alleles['clbP'], 'clbQ': alleles['clbQ']}
