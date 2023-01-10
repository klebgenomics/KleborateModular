"""
This file contains a template module for Kleborate. Any new modules must contain the functions
defined in this file.

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

import os
import shutil
import sys


def get_headers():
    """
    This function returns the headers (column titles) for this module. It returns two lists:
    * full_headers: contains all headers for this module, each of which will be used in Kleborate's
        output file.
    * stdout_headers: contains a subset of headers which will be displayed in Kleborate's stdout.

    stdout_headers can be empty, in which case this module will not add anything to stdout.
    stdout_headers can also be the same as full_headers, in which case all of this module's results
    will be displayed in stdout. But there cannot be a header in stdout_headers which is not in
    full_headers. Typically, stdout_headers would just contain one or two items so the user can get
    a quick preview of the results by looking at Kleborate's stdout.
    """
    full_headers = ['header_a', 'header_b', 'header_c']
    stdout_headers = ['header_a']
    return full_headers, stdout_headers


def add_cli_options(parser):
    """
    This function adds a group of arguments for this module. If the template doesn't require any
    option, this function can do nothing (just a single pass statement). CLI options must be unique
    (not used by any other module), so verbose names are preferred.
    """
    module_name = os.path.basename(__file__)[:-3]
    group = parser.add_argument_group(f'{module_name} module')
    group.add_argument('--template_opt1', type=str, default='opt1_default',
                       help='String option for module')
    group.add_argument('--template_opt2', type=int, default=1,
                       help='Integer option for module')
    group.add_argument('--template_flag', action='store_true',
                       help='Optional flag for module')
    return group


def check_cli_options(args):
    """
    This function checks the CLI options for this module. If any bad options are discovered, this
    function should quit the program with an error message. If no checks are needed, this function
    can do nothing (just a single pass statement).
    """
    if args.template_opt2 >= 10:
        sys.exit('Error: --template_opt2 must be less than 10')


def check_external_programs():
    """
    This function checks any external programs needed by this module. If any requirements are not
    found, this function should quit the program with an error message. If no external programs are
    needed, this function can do nothing (just a single pass statement).
    """
    if not shutil.which('mash'):
        sys.exit('Error: could not find mash')
    if not shutil.which('minimap2'):
        sys.exit('Error: could not find minimap2')


def get_results(assembly):
    """
    This function carries out the module's analysis on a single assembly. It returns a dictionary
    of results, where the module's headers are the keys and the values are the corresponding
    results in string format.
    """
    results = {'header_a': 'result_a', 'header_b': 'result_b', 'header_c': 'result_c'}

    assert sorted(results.keys()) == sorted(get_headers()[0])
    return results
