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

import collections
import pathlib
import pytest
import re
import tempfile

import kleborate.__main__
import kleborate.version


def test_version():
    assert re.match(r'\d+\.\d+\.\d+', kleborate.version.__version__)


def test_get_all_module_names():
    module_names = kleborate.__main__.get_all_module_names()
    assert 'contig_stats' in module_names
    assert 'template' not in module_names


def test_get_headers():
    module_names, modules = kleborate.__main__.import_modules()
    full_headers, stdout_headers = kleborate.__main__.get_headers(['contig_stats'], modules)
    assert full_headers[0] == 'assembly'
    assert stdout_headers[0] == 'assembly'
    assert all(h in full_headers for h in stdout_headers)


def test_check_assemblies_1():
    Args = collections.namedtuple('Args', ['assemblies'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main']))
    assert 'is a directory' in str(e.value)


def test_check_assemblies_2():
    Args = collections.namedtuple('Args', ['assemblies'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main/does_not_exist']))
    assert 'could not find' in str(e.value)


def test_check_assemblies_3():
    Args = collections.namedtuple('Args', ['assemblies'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main/bad_format.fasta']))
    assert 'invalid' in str(e.value)


def test_check_assemblies_4():
    Args = collections.namedtuple('Args', ['assemblies'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main/empty_seq.fasta']))
    assert 'zero-length sequence' in str(e.value)


def test_check_assemblies_5():
    Args = collections.namedtuple('Args', ['assemblies'])
    kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main/test.fasta']))
    kleborate.__main__.check_assemblies(Args(assemblies=['test/test_main/test.fasta.gz']))


def test_decompress_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        in_file = 'test/test_main/test.fasta.gz'
        out_file = pathlib.Path(tmp_dir) / 'temp.fasta'
        ref_file = 'test/test_main/test.fasta'
        kleborate.__main__.decompress_file(in_file, out_file)
        assert open(out_file, 'rt').read() == open(ref_file, 'rt').read()


def test_gunzip_assembly_if_necessary_1():
    with tempfile.TemporaryDirectory() as tmp_dir:
        assembly = 'test/test_main/test.fasta'
        assert kleborate.__main__.gunzip_assembly_if_necessary(assembly, tmp_dir) == assembly


def test_gunzip_assembly_if_necessary_2():
    with tempfile.TemporaryDirectory() as tmp_dir:
        assembly = 'test/test_main/test.fasta.gz'
        assert kleborate.__main__.gunzip_assembly_if_necessary(assembly, tmp_dir) != assembly
