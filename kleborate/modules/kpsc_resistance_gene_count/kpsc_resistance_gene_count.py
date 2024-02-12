"""
Copyright 2023 Kat Holt
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
import collections
from collections import defaultdict

from ...shared.resMinimap import read_class_file, get_res_headers

def description():
    return 'Counts up all resistance genes, excluding the Bla class which is intrinsic' \
           'results of the kpsc_amr module'


def prerequisite_modules():
    return ['kpsc_amr']


def get_headers():
    full_headers = ['num_resistance_genes']
    stdout_headers = ['num_resistance_genes']
    return full_headers, stdout_headers


def add_cli_options(parser):
    pass


def check_cli_options(args):
    pass


def check_external_programs():
    return []

def data_dir():
    return pathlib.Path(__file__).parents[0] / 'data'



def get_results(assembly, minimap2_index, args, previous_results):

    """
    Counts up all resistance genes, excluding the 'Bla' class which is intrinsic.
    """


    _, res_classes, bla_classes = read_class_file(data_dir() / 'CARD_AMR_clustered.csv')
    res_headers = get_res_headers(res_classes, bla_classes)

    res_hits = {key.split('__')[1]: value for key, value in previous_results.items() if key.startswith('kpsc_amr__')}


    if not res_headers:
        return '-'
    res_indices = [i for i, h in enumerate(res_headers) if h.lower().endswith('_acquired')]
    gene_list = []
    for i in res_indices:
        # Check if the value is not a dash before splitting
        if res_hits[res_headers[i]] != '-':
            genes = res_hits[res_headers[i]].split(';')
            gene_list.extend(genes)

    return {'num_resistance_genes': len(gene_list)}




