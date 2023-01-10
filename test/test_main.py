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


def test_output_headers(capfd):
    full_headers = ['header_a', 'header_b', 'header_c']
    stdout_headers = ['header_a', 'header_b']
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = pathlib.Path(tmp_dir) / 'out.txt'
        kleborate.__main__.output_headers(full_headers, stdout_headers, out_file)
        out, err = capfd.readouterr()
        assert out == 'header_a\theader_b\n'
        assert open(out_file, 'rt').read() == 'header_a\theader_b\theader_c\n'


def test_output_results_1(capfd):
    full_headers = ['header_a', 'header_b', 'header_c']
    stdout_headers = ['header_a', 'header_b']
    results = {'header_a': 'result_a', 'header_b': 'result_b', 'header_c': 'result_c'}
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = pathlib.Path(tmp_dir) / 'out.txt'
        kleborate.__main__.output_results(full_headers, stdout_headers, out_file, results)
        out, err = capfd.readouterr()
        assert out == 'result_a\tresult_b\n'
        assert open(out_file, 'rt').read() == 'result_a\tresult_b\tresult_c\n'


def test_output_results_2(capfd):
    full_headers = ['header_a', 'header_b']
    stdout_headers = ['header_a']
    results = {'header_a': 'result_a', 'header_b': 'result_b', 'header_c': 'result_c'}
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = pathlib.Path(tmp_dir) / 'out.txt'
        with pytest.raises(SystemExit) as e:
            kleborate.__main__.output_results(full_headers, stdout_headers, out_file, results)
        assert 'not covered by the output headers' in str(e.value)


def test_get_presets():
    presets = kleborate.__main__.get_presets()
    all_module_names = kleborate.__main__.get_all_module_names()
    for preset, modules in presets.items():
        assert len(modules) == len(set(modules))  # duplicates not allowed
        for module in modules:
            assert module in all_module_names


def test_get_used_module_names_1():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    modules = kleborate.__main__.get_used_module_names(Args(modules='b,c,d', preset=None),
                                                       all_module_names, presets)
    assert modules == ['b', 'c', 'd']


def test_get_used_module_names_2():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    modules = kleborate.__main__.get_used_module_names(Args(modules='c,b,a', preset=None),
                                                       all_module_names, presets)
    assert modules == ['c', 'b', 'a']


def test_get_used_module_names_3():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    modules = kleborate.__main__.get_used_module_names(Args(modules=None, preset='2'),
                                                       all_module_names, presets)
    assert modules == ['c', 'd', 'e']


def test_get_used_module_names_4():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    modules = kleborate.__main__.get_used_module_names(Args(modules='b,c', preset='2'),
                                                       all_module_names, presets)
    assert modules == ['c', 'd', 'e', 'b']


def test_get_used_module_names_5():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.get_used_module_names(Args(modules=None, preset='3'),
                                                 all_module_names, presets)
    assert '3 is not a valid preset' in str(e.value)


def test_get_used_module_names_6():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.get_used_module_names(Args(modules='a,b,f', preset=None),
                                                 all_module_names, presets)
    assert 'f is not a valid module name' in str(e.value)


def test_get_used_module_names_7():
    all_module_names = ['a', 'b', 'c', 'd', 'e']
    presets = {'1': ['a', 'b', 'c'], '2': ['c', 'd', 'e']}
    Args = collections.namedtuple('Args', ['modules', 'preset'])
    with pytest.raises(SystemExit) as e:
        kleborate.__main__.get_used_module_names(Args(modules=None, preset=None),
                                                 all_module_names, presets)
    assert 'either --preset or --modules is required' in str(e.value)
