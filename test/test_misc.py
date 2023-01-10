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

import gzip
import pytest
import re

import kleborate.misc
import kleborate.version


def test_version():
    assert re.match(r'\d+\.\d+\.\d+', kleborate.version.__version__)


def test_get_compression_type_1():
    assert kleborate.misc.get_compression_type('test/test_misc/test.txt') == 'plain'


def test_get_compression_type_2():
    assert kleborate.misc.get_compression_type('test/test_misc/test.gz') == 'gz'


def test_get_compression_type_3():
    with pytest.raises(SystemExit) as e:
        kleborate.misc.get_compression_type('test/test_misc/test.bz2')
    assert 'cannot use bzip2' in str(e.value)


def test_get_compression_type_4():
    with pytest.raises(SystemExit) as e:
        kleborate.misc.get_compression_type('test/test_misc/test.zip')
    assert 'cannot use zip' in str(e.value)


def test_get_open_func_1():
    assert kleborate.misc.get_open_func('test/test_misc/test.txt') == open


def test_get_open_func_2():
    assert kleborate.misc.get_open_func('test/test_misc/test.gz') == gzip.open


def test_reverse_complement_1():
    assert kleborate.misc.reverse_complement('GGGGaaaaaaaatttatatat') == 'atatataaattttttttCCCC'


def test_reverse_complement_2():
    assert kleborate.misc.reverse_complement('atatataaattttttttCCCC') == 'GGGGaaaaaaaatttatatat'


def test_reverse_complement_3():
    assert kleborate.misc.reverse_complement('ACGT123') == 'NNNACGT'


def test_load_fasta_1():
    fasta_seqs = kleborate.misc.load_fasta('test/test_misc/blank_lines.fasta')
    assert len(fasta_seqs) == 2


def test_load_fasta_2():
    fasta_seqs = kleborate.misc.load_fasta('test/test_misc/lowercase.fasta')
    assert len(fasta_seqs) == 2
    assert fasta_seqs[0][1].startswith('TTGCCTGTA')
    assert fasta_seqs[1][1].startswith('ATTCTCAGA')


def test_load_fasta_3():
    fasta_seqs = kleborate.misc.load_fasta('test/test_misc/empty.fasta')
    assert len(fasta_seqs) == 0
