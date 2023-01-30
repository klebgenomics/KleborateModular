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


def prerequisite_modules():
    return ['abst', 'cbst', 'ybst']


def get_headers():
    full_headers = ['virulence_score']
    stdout_headers = ['virulence_score']
    return full_headers, stdout_headers


def add_cli_options(parser):
    pass


def check_cli_options(args):
    pass


def check_external_programs():
    pass


def get_results(assembly, args, previous_results):
    has_ybt = (previous_results['ybst__st'] != 'NA')
    has_aero = (previous_results['abst__st'] != 'NA')
    has_coli = (previous_results['cbst__st'] != 'NA')

    if has_coli and has_aero:
        return {'virulence_score': '5'}
    elif has_aero and has_ybt:
        return {'virulence_score': '4'}
    elif has_aero:
        return {'virulence_score': '3'}
    elif has_coli:
        return {'virulence_score': '2'}
    elif has_ybt:
        return {'virulence_score': '1'}
    else:
        return {'virulence_score': '0'}
