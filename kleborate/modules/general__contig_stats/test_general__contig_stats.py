"""
This file contains tests for Kleborate. To run all tests, go the repo's root directory and run:
  python3 -m pytest

To get code coverage stats:
  coverage run --source . -m pytest && coverage report -m

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

import pathlib

from .contig_stats import *


def get_file_dir():
    # Returns the path of the directory with the files for these tests.
    return pathlib.Path(__file__).parents[0] / 'test_files'


def test_prerequisite_modules():
    assert prerequisite_modules() == []


def test_get_headers():
    # stdout_headers must be a subset of full_headers.
    full_headers, stdout_headers = get_headers()
    assert all(h in full_headers for h in stdout_headers)


def test_empty_functions():
    # Tests the functions that aren't used in this module.
    assert add_cli_options(None) is None
    assert check_cli_options(None) is None
    assert check_external_programs() == []


def test_count_1():
    contig_count, _, _, _, _ = get_contig_stats(get_file_dir() / 'test_1.fasta')
    assert contig_count == 4


def test_count_2():
    contig_count, _, _, _, _ = get_contig_stats(get_file_dir() / 'test_2.fasta')
    assert contig_count == 3


def test_n50_1():
    _, n50, _, _, _ = get_contig_stats(get_file_dir() / 'test_1.fasta')
    assert n50 == 40


def test_n50_2():
    _, n50, _, _, _ = get_contig_stats(get_file_dir() / 'test_2.fasta')
    assert n50 == 200


def test_longest_1():
    _, _, longest_contig, _, _ = get_contig_stats(get_file_dir() / 'test_1.fasta')
    assert longest_contig == 45


def test_longest_2():
    _, _, longest_contig, _, _ = get_contig_stats(get_file_dir() / 'test_2.fasta')
    assert longest_contig == 200


def test_ambiguous_bases_1():
    _, _, _, _, ambiguous = get_contig_stats(get_file_dir() / 'test_1.fasta')
    assert ambiguous == 'no'


def test_ambiguous_bases_2():
    _, _, _, _, ambiguous = get_contig_stats(get_file_dir() / 'test_2.fasta')
    assert ambiguous == 'yes (1)'


def test_ambiguous_bases_3():
    _, _, _, _, ambiguous = get_contig_stats(get_file_dir() / 'test_3.fasta')
    assert ambiguous == 'no'


def test_ambiguous_bases_4():
    _, _, _, _, ambiguous = get_contig_stats(get_file_dir() / 'test_4.fasta')
    assert ambiguous == 'yes (4)'


def test_total_size_1():
    _, _, _, total_size, _ = get_contig_stats(get_file_dir() / 'test_1.fasta')
    assert total_size == 115


def test_total_size_2():
    _, _, _, total_size, _ = get_contig_stats(get_file_dir() / 'test_2.fasta')
    assert total_size == 260


def test_total_size_3():
    _, _, _, total_size, _ = get_contig_stats(get_file_dir() / 'test_3.fasta')
    assert total_size == 260


def test_total_size_4():
    _, _, _, total_size, _ = get_contig_stats(get_file_dir() / 'test_4.fasta')
    assert total_size == 260


def test_qc_warnings_1():
    # A perfectly nice assembly - yields no warnings.
    warnings = get_qc_warnings(250000, 'no')
    assert warnings == '-'


def test_qc_warnings_2():
    # Small N50.
    warnings = get_qc_warnings(1000, 'no')
    assert warnings == 'N50'


def test_qc_warnings_3():
    # Has ambiguous bases.
    warnings = get_qc_warnings(250000, 'yes (50)')
    assert warnings == 'ambiguous_bases'


def test_qc_warnings_4():
    # Small N50 and has ambiguous bases.
    warnings = get_qc_warnings(1000, 'yes (1000)')
    assert warnings == 'N50,ambiguous_bases'


def test_empty_file_1():
    contig_count, n50, longest_contig, total_size, ambiguous = \
        get_contig_stats(get_file_dir() / 'empty.fasta')
    assert contig_count == 0
    assert n50 == 0
    assert longest_contig == 0
    assert total_size == 0
    assert ambiguous == 'no'


def test_get_results():
    # Final results are all in string format.
    results = get_results(get_file_dir() / 'test_1.fasta', None, None, {})
    assert results['contig_count'] == '4'
    assert results['n50'] == '40'
    assert results['largest_contig'] == '45'
    assert results['total_size'] == '115'
    assert results['ambiguous_bases'] == 'no'
    assert results['qc_warnings'] == 'N50'
