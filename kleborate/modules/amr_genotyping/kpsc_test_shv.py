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
import pytest


from kleborate.shared.shv_mutations import*
from kleborate.shared.resMinimap import read_class_file, get_res_headers, resminimap_assembly
from kleborate.modules.amr_genotyping.amr_genotyping import get_headers, get_results


def get_test_genome_dir():
    return pathlib.Path(__file__).parents[3] / 'test' / 'test_shv'


def test_prerequisite_modules():
    assert prerequisite_modules() == []


def test_check_external_programs_1(mocker):
    # Tests the good case where minimap2 is found.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'minimap2': '/usr/bin/minimap2'}[x],
    )
    assert check_external_programs() == ['minimap2']


def test_check_external_programs_2(mocker):
    # Tests the bad case where minimap2 is missing.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'minimap2': None}[x],
    )
    with pytest.raises(SystemExit):
        check_external_programs()



def test_get_results_1():
	"""
    This test has an exact match for SHV-1.
    """

    results = get_results(get_test_genome_dir() / '01.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_chr'] == 'SHV-1'
    assert results['SHV_mutations'] == '-'

def test_get_results_2():
	"""
    This test has a match for SHV-1 with a mutation at site 238 (G -> Y). This changes the
    class to ESBL, so the mutation is included in the
    """

    results = get_results(get_test_genome_dir() / '02.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_ESBL_acquired'] == 'SHV-1* +238Y'
    assert results['SHV_mutations'] == '-'


 def test_get_results_3():
	"""
    Same as test 2, but the gene is on the reverse strand.
    """

    results = get_results(get_test_genome_dir() / '03.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_ESBL_acquired'] == 'SHV-1* +238Y'
    assert results['SHV_mutations'] == '238Y'

def test_get_results_4():
	"""
    This test has a match for SHV-1 with a mutation at site 50 (G -> Y). This doesn't change
    resistance and so won't be reported.
    """

    results = get_results(get_test_genome_dir() / '04.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_chr'] == 'SHV-1*'
    assert results['SHV_mutations'] == '-'

def test_get_results_5():
	"""
    This test has an exact match for SHV-29.
    """

    results = get_results(get_test_genome_dir() / '05.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_ESBL_acquired'] == 'SHV-29'
    assert results['SHV_mutations'] == '238A;35Q'


def test_get_results_6():
	"""
    This test has SHV-29 plus an inhibition mutation.
    """

    results = get_results(get_test_genome_dir() / '06.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_ESBL_inhR_acquired'] == 'SHV-29* +234Y'
    assert results['SHV_mutations'] ==  '234Y;238A;35Q'

def test_get_results_7():
	
	"""
    This test has SHV-1 with position 238 deleted. Since it's not in the omega loop, this isn't
    reported and doesn't have an effect.
    """

    results = get_results(get_test_genome_dir() / '07.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_chr'] == 'SHV-1*'
    assert results['SHV_mutations'] == '-'

def test_get_results_8():
	"""
    This test has SHV-1 with a synonymous mutation in the omega loop (so not reported).
    """

    results = get_results(get_test_genome_dir() / '08.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_chr'] == 'SHV-1^'
    assert results['SHV_mutations'] == '-'

def test_get_results_9():
	"""
    This test has SHV-1 with a nonsynonymous mutation in the omega loop (so it is reported).
    """

    results = get_results(get_test_genome_dir() / '09.fasta', None,
                          Args(min_identity=90.0, min_coverage=80.0), {})
    assert results['Bla_ESBL_acquired'] == 'SHV-1* +174R'
    assert results['SHV_mutations'] == '174R;omega-loop=RWETELNEALRGDARD'





