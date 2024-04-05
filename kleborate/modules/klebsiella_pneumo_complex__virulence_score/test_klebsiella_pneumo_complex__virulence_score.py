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

from .kpsc_virulence_score import *


def test_prerequisite_modules():
    assert sorted(prerequisite_modules()) == ['abst', 'cbst', 'ybst']


def test_empty_functions():
    # Tests the functions that aren't used in this module.
    assert add_cli_options(None) is None
    assert check_cli_options(None) is None
    assert check_external_programs() == []


def test_get_results_1():
    previous_results = {'ybst__st': 'NA', 'abst__st': 'NA', 'cbst__st': 'NA'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '0'


def test_get_results_2():
    previous_results = {'ybst__st': 'ST1', 'abst__st': 'NA', 'cbst__st': 'NA'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '1'


def test_get_results_3():
    previous_results = {'ybst__st': 'NA', 'abst__st': 'NA', 'cbst__st': 'ST1'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '2'


def test_get_results_4():
    previous_results = {'ybst__st': 'ST1', 'abst__st': 'NA', 'cbst__st': 'ST1'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '2'


def test_get_results_5():
    previous_results = {'ybst__st': 'NA', 'abst__st': 'ST1', 'cbst__st': 'NA'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '3'


def test_get_results_6():
    previous_results = {'ybst__st': 'ST1', 'abst__st': 'ST1', 'cbst__st': 'NA'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '4'


def test_get_results_7():
    previous_results = {'ybst__st': 'NA', 'abst__st': 'ST1', 'cbst__st': 'ST1'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '5'


def test_get_results_8():
    previous_results = {'ybst__st': 'ST1', 'abst__st': 'ST1', 'cbst__st': 'ST1'}
    assert get_results(None, None, None, previous_results)['virulence_score'] == '5'
