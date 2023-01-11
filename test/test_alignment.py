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

import pytest

from kleborate.shared.alignment import *


def test_bad_paf():
    with pytest.raises(SystemExit) as e:
        Alignment('not_a_paf_line')
    assert 'PAF format' in str(e.value)


def test_repr():
    a = Alignment('A\t1000\t50\t150\t+\tC\t1000\t60\t160\t100\t100\tAS:i:100\tcg:Z:100=')
    assert str(a) == 'A:50-150(+), C:60-160 (100.000%)'


def test_get_expanded_cigar():
    assert get_expanded_cigar('5=') == '====='
    assert get_expanded_cigar('3=1I4=2D2=1X4=') == '===I====DD==X===='
    assert get_expanded_cigar('') == ''
