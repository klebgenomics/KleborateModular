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

from .klebsiella_species import *


def get_test_genome_dir():
    return pathlib.Path(__file__).parents[3] / 'test' / 'test_genomes'


def get_sketch_file():
    return pathlib.Path(__file__).parents[0] / 'data' / 'species_mash_sketches.msh'


def test_prerequisite_modules():
    assert prerequisite_modules() == []


def test_check_cli_options_1():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    check_cli_options(Args(klebsiella_species_strong=0.01, klebsiella_species_weak=0.05))


def test_check_cli_options_2():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(klebsiella_species_strong=0.05, klebsiella_species_weak=0.01))


def test_check_cli_options_3():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(klebsiella_species_strong=-0.01, klebsiella_species_weak=0.05))


def test_check_cli_options_4():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    with pytest.raises(SystemExit):
        check_cli_options(Args(klebsiella_species_strong=0.01, klebsiella_species_weak=1.5))


def test_check_external_programs_1(mocker):
    # Tests the good case where Mash is found.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'mash': '/usr/bin/mash'}[x],
    )
    assert check_external_programs() == ['mash']


def test_check_external_programs_2(mocker):
    # Tests the bad case where mash is missing.
    mocker.patch(
        'shutil.which',
        side_effect=lambda x: {'mash': None}[x],
    )
    with pytest.raises(SystemExit):
        check_external_programs()


def test_get_results_1():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    results = get_results(get_test_genome_dir() / 'GCF_000016305.1.fna.gz', None,
                          Args(klebsiella_species_strong=0.01, klebsiella_species_weak=0.04), {})
    assert results['species'] == 'Klebsiella pneumoniae'
    assert results['species_match'] == 'strong'


def test_get_results_2():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    results = get_results(get_test_genome_dir() / 'GCF_000016305.1.fna.gz', None,
                          Args(klebsiella_species_strong=0.001, klebsiella_species_weak=0.004), {})
    assert results['species'] == 'Klebsiella pneumoniae'
    assert results['species_match'] == 'weak'


def test_get_results_3():
    Args = collections.namedtuple('Args', ['klebsiella_species_strong', 'klebsiella_species_weak'])
    results = get_results(get_test_genome_dir() / 'GCF_000016305.1.fna.gz', None,
                          Args(klebsiella_species_strong=0.0001, klebsiella_species_weak=0.0004),
                          {})
    assert results['species'] == 'unknown'
    assert results['species_match'] == ''


def test_klebsiella_aerogenes():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000215745.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella aerogenes'


def test_klebsiella_grimontii():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000733495.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella grimontii'


def test_klebsiella_indica():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_005860775.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella indica'


def test_klebsiella_michiganensis():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000240325.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella michiganensis'


def test_klebsiella_oxytoca():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000247855.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella oxytoca'


def test_klebsiella_pasteurii():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCA_902158585.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella pasteurii'


def test_klebsiella_pneumoniae():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000016305.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella pneumoniae'


def test_klebsiella_quasipneumoniae_subsp_quasipneumoniae():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000492415.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella quasipneumoniae subsp. quasipneumoniae'


def test_klebsiella_quasipneumoniae_subsp_similipneumoniae():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000492795.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella quasipneumoniae subsp. similipneumoniae'


def test_klebsiella_quasivariicola():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000523395.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella quasivariicola'


def test_klebsiella_spallanzanii():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCA_901563875.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella spallanzanii'


def test_klebsiella_variicola_subsp_variicola():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000019565.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella variicola subsp. variicola'


def test_klebsiella_variicola_subsp_tropica():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_002806645.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella variicola subsp. tropica'


def test_klebsiella_africana():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_016804125.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella africana'


def test_raoultella_planticola():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000648315.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella planticola'


def test_raoultella_ornithinolytica():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000247895.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella ornithinolytica'


def test_raoultella_terrigena():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_000829965.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Klebsiella terrigena'


def test_salmonella():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_004010735.1.fna.gz',
                                        get_sketch_file())
    assert 'Salmonella' in species


def test_citrobacter():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_003937345.1.fna.gz',
                                        get_sketch_file())
    assert 'Citrobacter' in species


def test_yersinia_unknown():
    species, _ = get_klebsiella_species(get_test_genome_dir() / 'GCF_001123825.1.fna.gz',
                                        get_sketch_file())
    assert species == 'Yersinia (unknown species)'
