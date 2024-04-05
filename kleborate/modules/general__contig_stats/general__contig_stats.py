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

import collections
import json
import pathlib
from pathlib import Path
import ast

from ...shared.misc import load_fasta



def description():
    return 'basic stats on the assembly\'s contigs'


def prerequisite_modules():
    return []


def get_headers():
    full_headers = ['contig_count', 'n50', 'largest_contig', 'total_size', 'ambiguous_bases',
                    'qc_warnings']
    stdout_headers = ['n50']
    return full_headers, stdout_headers


def add_cli_options(parser):
    pass


def check_cli_options(args):
    pass


def check_external_programs():
    return []


def data_dir():
    return pathlib.Path(__file__).parents[0] 

def get_results(assembly, minimap2_index, args, previous_results, species):
    species_file = data_dir() / 'species_specification.txt'
    species_specification_dict = load_species_specifications(species_file)
    #print(previous_results)
    
    contig_count, n50, longest_contig, total_size, ambiguous_bases = get_contig_stats(assembly)
    qc_warnings = get_qc_warnings(total_size, n50, ambiguous_bases, species, species_specification_dict)
    return {'contig_count': str(contig_count),
            'n50': str(n50),
            'largest_contig': str(longest_contig),
            'total_size': str(total_size),
            'ambiguous_bases': ambiguous_bases,
            'qc_warnings': qc_warnings}


def get_contig_stats(assembly):
    fasta = load_fasta(assembly)

    base_counts = collections.defaultdict(int)
    for _, seq in fasta:
        for b in seq:
            base_counts[b] += 1
    base_counts.pop('A', None)
    base_counts.pop('C', None)
    base_counts.pop('G', None)
    base_counts.pop('T', None)
    ambiguous_base_count = sum(base_counts.values())
    if ambiguous_base_count:
        ambiguous_bases = 'yes (' + str(ambiguous_base_count) + ')'
    else:
        ambiguous_bases = 'no'

    contig_lengths = sorted([len(x[1]) for x in fasta])
    if not contig_lengths:
        return 0, 0, 0, 0, 'no'
    longest = contig_lengths[-1]

    total_size = sum(contig_lengths)
    half_total_length = total_size / 2
    total_so_far = 0
    segment_lengths = contig_lengths[::-1]
    n50 = 0
    for length in segment_lengths:
        total_so_far += length
        if total_so_far >= half_total_length:
            n50 = length
            break

    return len(contig_lengths), n50, longest, total_size, ambiguous_bases


def load_species_specifications(file_path):
    with open(file_path, 'r') as file:
        # Read the entire file content into a single string
        file_content = file.read()
        
        # Safely evaluate the string as a Python expression
        species_specifications = ast.literal_eval(file_content)
    
    return species_specifications


def get_qc_warnings(total_size, n50, ambiguous_bases, species, species_specification_dict): 
    warnings = []
    species_spec = species_specification_dict[species]
    min_size, max_size = species_spec['min_genome_size'], species_spec['max_genome_size']

    if total_size < min_size:
        warnings.append('total_size below min threshold')
    elif total_size > max_size:
        warnings.append('total_size above max threshold')
    

    if n50 < 10000:
        warnings.append('N50')
    if 'yes' in ambiguous_bases:
        warnings.append('ambiguous_bases')
    if warnings:
        return ','.join(warnings)
    else:
        return '-'