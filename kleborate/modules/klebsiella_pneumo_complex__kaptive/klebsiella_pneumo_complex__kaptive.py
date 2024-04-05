"""
This module contains classes for interacting with bacterial genome assemblies and contigs and a pipeline
to type them.

Copyright 2023 Tom Stanton (tomdstanton@gmail.com)
https://github.com/klebgenomics/Kaptive

This file is part of Kaptive. Kaptive is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kaptive is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kaptive.
If not, see <https://www.gnu.org/licenses/>.
"""

import os
import pathlib
from pathlib import Path
import shutil
import sys
import dna_features_viewer
from dna_features_viewer import GraphicFeature, GraphicRecord

from kaptive.database import Database
from kaptive.assembly import typing_pipeline
from kaptive.misc import check_python_version, check_programs, get_logo, check_cpus, check_dir, check_file

def description():
    return 'In silico serotyping of K and L locus for the Klebsiella pneumoniae species complex'


def prerequisite_modules():
    return []


def get_headers():
    full_headers = [
        'Assembly', 'Best match locus', 'Best match type', 'Confidence', 'Problems', 'Identity', 'Coverage',
        'Length discrepancy', 'Expected genes in locus', 'Expected genes in locus, details', 'Missing expected genes',
        'Other genes in locus', 'Other genes in locus, details', 'Expected genes outside locus',
        'Expected genes outside locus, details', 'Other genes outside locus', 'Other genes outside locus, details',
        'Truncated genes, details'
    ]
    stdout_headers = []
    return full_headers, stdout_headers




def add_cli_options(parser):
    module_name = os.path.basename(__file__)[:-3]
    group = parser.add_argument_group(f'{module_name} module')

    #group.add_argument('db', type=get_database, help='Kaptive database path or keyword')
    #group.add_argument('input', nargs='+', type=check_file, help='Assemblies in fasta(.gz) format')


    # group.add_argument("--score-metric", type=str, default='AS', metavar='',
    #                   help="Alignment metric to use for scoring (default: %(default)s)")
    # group.add_argument("--weight-metric", type=str, metavar='', default='prop_genes_found',
    #                   help="Weighting for scoring metric (default: %(default)s)\n"
    #                        " - none: No weighting\n"
    #                        " - locus_length: length of the locus\n"
    #                        " - genes_expected: # of genes expected in the locus\n"
    #                        " - genes_found: # of genes found in the locus\n"
    #                        " - prop_genes_found: genes_found / genes_expected")
    # group.add_argument("--min-zscore", type=float, metavar='', default=3.0,
    #                   help="Minimum zscore for confidence (default: %(default)s)")
    # group.add_argument('--min-cov', type=float, required=False, default=50.0, metavar='',
    #                   help='Minimum gene %%coverage to be used for scoring (default: %(default)s)')
    # group.add_argument("--gene-threshold", type=float, metavar='',
    #                   help="Species-level locus gene identity threshold (default: database specific)")
    group.add_argument('-t', '--threads', type=check_cpus, default=1, metavar='',
                      help="Number of threads for alignment (default: %(default)s)")


    return group


def check_cli_options(args):
    if args.threads < 1:
        raise ValueError("The number of threads must be at least 1.")
#     if args.min-zscore <= 3.0 or args.min-zscore >= 10.0:
#         sys.exit('Error: --min_identity must be between 3 and 10.0')
#     if args.min-cov <= 50.0 or args.min-cov >= 60.0:
#         sys.exit('Error: --min_coverage must be between 50.0 and 60.0')
    

def check_external_programs():
    if not shutil.which('minimap2'):
        sys.exit('Error: could not find minimap2')
    return ['minimap2']


def data_dir():
    return pathlib.Path(__file__).parents[0] / 'reference_database'



#def get_results(assembly:Path, minimap2_index, args, previous_results):
def get_results(assembly, minimap2_index, args, previous_results, species):

    k_database_path = Path(data_dir() / 'Klebsiella_k_locus_primary_reference.gbk')
    o_database_path = Path(data_dir() / 'Klebsiella_o_locus_primary_reference.gbk')

    k_db, o_db = Database.from_genbank(k_database_path, load_seq=False), Database.from_genbank(o_database_path, load_seq=False)


    # k_results = [typing_pipeline(assembly, k_db, threads=8) for assembly in assemblies]
    # o_results = [typing_pipeline(assembly, o_db, threads=8) for assembly in assemblies]


    k_results = [typing_pipeline(Path(ass), k_db, threads=8) for ass in assembly]
    o_results = [typing_pipeline(Path(ass), o_db, threads=8) for ass in assembly]

    
    
    k_result_dicts = []
    for result in k_results:
        k_result_dict = {}
        k_result_table = result.as_table()  
        for line in k_result_table.split('\n'):
            if line:
                parts = line.split('\t')
                k_result_dict = {'k_' + key: value for key, value in zip(full_headers, parts)}
                k_result_dicts.append(k_result_dict)

    o_result_dicts = []
    for result in o_results:
        o_result_dict = {}
        o_result_table = result.as_table()  
        for line in o_result_table.split('\n'):
            if line:
                parts = line.split('\t')
                o_result_dict = {'o_' + key: value for key, value in zip(full_headers, parts)}
                o_result_dicts.append(o_result_dict)
    return k_result_dicts, o_result_dicts




        

    
    




	














