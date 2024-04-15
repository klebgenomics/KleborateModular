"""
This module contains classes for interacting with bacterial genome assemblies and contigs and a pipeline
to type them.

Copyright 2024 Mary Maranga, Kat Holt, Tom Stanton, Ryan Wick
https://github.com/klebgenomics/KleborateModular/
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
        'K_locus', 'K_type', 'K_Confidence', 'K_Problems', 'K_Identity', 
        'K_Coverage', 'K_Length discrepancy', 'K_Expected genes in locus', 
        'K_Expected genes in locus, details', 'K_Missing expected genes', 
        'K_Other genes in locus', 'K_Other genes in locus, details', 
        'K_Expected genes outside locus', 'K_Expected genes outside locus, details', 
        'K_Other genes outside locus', 'K_Other genes outside locus, details',
        'O_locus', 'O_type', 'O_Confidence', 'O_Problems', 'O_Identity', 
        'O_Coverage', 'O_Length discrepancy', 'O_Expected genes in locus', 
        'O_Expected genes in locus, details', 'O_Missing expected genes', 
        'O_Other genes in locus', 'O_Other genes in locus, details', 
        'O_Expected genes outside locus', 'O_Expected genes outside locus, details', 
        'O_Other genes outside locus', 'O_Other genes outside locus, details'
    ]
    stdout_headers = []
    return full_headers, stdout_headers


def add_cli_options(parser):
    module_name = os.path.basename(__file__)[:-3]
    group = parser.add_argument_group(f'{module_name} module')
    group.add_argument('-t', '--threads', type=check_cpus, default=1, metavar='',
                      help="Kaptive number of threads for alignment (default: %(default)s)")

    return group


def check_cli_options(args):
    if args.threads < 1:
        raise ValueError("The number of threads must be at least 1.")
    

def check_external_programs():
    if not shutil.which('minimap2'):
        sys.exit('Error: could not find minimap2')
    return ['minimap2']


def data_dir():
    return pathlib.Path(__file__).parents[0] / 'reference_database'


def get_results(assembly, minimap2_index, args, previous_results):
    full_headers, _ = get_headers()
    
    # Filter for k_ and o_ prefixed headers
    k_headers = [h for h in full_headers if h.startswith('K_')]
    o_headers = [h for h in full_headers if h.startswith('O_')]

    if not isinstance(assembly, list):
        assembly = [assembly]

    ref_database = Path(data_dir())
    k_database_path = ref_database / 'Klebsiella_k_locus_primary_reference.gbk'
    o_database_path = ref_database / 'Klebsiella_o_locus_primary_reference.gbk'

    k_db, o_db = Database.from_genbank(k_database_path, load_seq=False), Database.from_genbank(o_database_path, load_seq=False)

    assembly_paths = [Path(asmbly) if not isinstance(asmbly, Path) else asmbly for asmbly in assembly]

    results_dict = {}

    for assembly_path in assembly_paths:
        # Process k typing results
        k_results = typing_pipeline(assembly_path, k_db, threads=args.threads)
        k_result_table = k_results.as_table()
        for line in k_result_table.split('\n'):
            if line:
                parts = line.split('\t')[1:-1]  # Slice to exclude the first and last fiels
                for key, value in zip(k_headers, parts):  
                    results_dict[key] = value

        # Process O typing results
        o_results = typing_pipeline(assembly_path, o_db, threads=args.threads)
        o_result_table = o_results.as_table()
        for line in o_result_table.split('\n'):
            if line:
                parts = line.split('\t')[1:-1]  # Slice to exclude the first and last field
                for key, value in zip(o_headers, parts):  
                    results_dict[key] = value
    return results_dict


# def get_results(assembly, minimap2_index, args, previous_results):

#     full_headers, _ = get_headers()

#     if not isinstance(assembly, list):
#         assembly = [assembly]

#     ref_database = Path(data_dir())
#     k_database_path = ref_database / 'Klebsiella_k_locus_primary_reference.gbk'
#     o_database_path = ref_database / 'Klebsiella_o_locus_primary_reference.gbk'

#     k_db, o_db = Database.from_genbank(k_database_path, load_seq=False), Database.from_genbank(o_database_path, load_seq=False)

#     assembly_paths = [Path(asmbly) if not isinstance(asmbly, Path) else asmbly for asmbly in assembly]

#     results_dict = {}

#     for assembly_path in assembly_paths:
#         k_results = typing_pipeline(assembly_path, k_db, threads=args.threads)
#         k_result_table = k_results.as_table()
#         for line in k_result_table.split('\n'):
#             if line:
#                 parts = line.split('\t')
#                 for key, value in zip(full_headers, parts):
#                     results_dict['k_' + key] = value

#     for assembly_path in assembly_paths:
#         o_results = typing_pipeline(assembly_path, o_db, threads=args.threads)
#         o_result_table = o_results.as_table()
#         for line in o_result_table.split('\n'):
#             if line:
#                 parts = line.split('\t')
#                 for key, value in zip(full_headers, parts):
#                     results_dict['o_' + key] = value

#     for key, value in results_dict.items():
#         print(f"{key}: {value}")

#     return results_dict










    




        

    
    




	














