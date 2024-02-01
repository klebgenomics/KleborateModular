"""
This file contains tests for Kleborate. To run all tests, go the repo's root directory and run:
  python3 -m pytest

To get code coverage stats:
  coverage run --source . -m pytest && coverage report -m

Copyright 2023 Kat Holt
Copyright 2020 Ryan Wick (rrwick@gmail.com)
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
import pytest
import pathlib


from kleborate.shared.resMinimap import read_class_file, get_res_headers, resminimap_assembly
from kleborate.modules.amr_genotyping.amr_genotyping import get_headers, get_results


def get_test_genome_dir():
    return pathlib.Path(__file__).parents[3] / 'test' / 'test_res_qrdr'


def test_get_results_1():
    Args = collections.namedtuple('Args', ['min_identity', 'min_coverage', 'min_spurious_identity', 'min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_qrdr_1.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0, min_spurious_identity=80.0, min_spurious_coverage=40.0), {})
    assert results['Flq_mutations'] == '-'

    
def test_get_results_2():
    Args = collections.namedtuple('Args', ['min_identity', 'min_coverage', 'min_spurious_identity', 'min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_qrdr_2.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0, min_spurious_identity=80.0, min_spurious_coverage=40.0), {})
    assert results['Flq_mutations'] == 'GyrA-83C'
    

def test_get_results_3():
    Args = collections.namedtuple('Args', ['min_identity', 'min_coverage', 'min_spurious_identity', 'min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_qrdr_3.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0, min_spurious_identity=80.0, min_spurious_coverage=40.0), {})
    assert results['Flq_mutations'] == 'ParC-84D'
    

def test_get_results_4():
    Args = collections.namedtuple('Args', ['min_identity', 'min_coverage', 'min_spurious_identity', 'min_spurious_coverage'])
    results = get_results(get_test_genome_dir() / 'test_res_qrdr_4.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0, min_spurious_identity=80.0, min_spurious_coverage=40.0), {})
    print(results)
    assert results['Flq_mutations'] == 'GyrA-83C;ParC-84D'


