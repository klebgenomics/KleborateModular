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

import os
import re
import subprocess
import sys


class Alignment(object):
    """
    Defines a minimap2 alignment. Each object is created from a single line in a minimap2 PAF file.

    It is assumed that minimap2 was run with its -c option so that full alignment is performed. If
    -c wasn't used, then some pieces will be missing (e.g. CIGAR) and some will be incorrect (e.g.
    percent_identity).
    """

    def __init__(self, paf_line):
        line_parts = paf_line.strip().split('\t')
        if len(line_parts) < 11:
            sys.exit('Error: alignment file does not seem to be in PAF format')

        self.query_name = line_parts[0]
        self.query_length = int(line_parts[1])
        self.query_start = int(line_parts[2])
        self.query_end = int(line_parts[3])
        self.strand = line_parts[4]

        self.target_name = line_parts[5]
        self.target_length = int(line_parts[6])
        self.target_start = int(line_parts[7])
        self.target_end = int(line_parts[8])

        self.matching_bases = int(line_parts[9])
        self.num_bases = int(line_parts[10])
        self.percent_identity = 100.0 * self.matching_bases / self.num_bases

        self.query_cov = 100.0 * (self.query_end - self.query_start) / self.query_length

        self.cigar, self.alignment_score = None, None
        for part in line_parts:
            if part.startswith('cg:Z:'):
                self.cigar = part[5:]
            if part.startswith('AS:i:'):
                self.alignment_score = int(part[5:])

    def __repr__(self):
        return self.query_name + ':' + str(self.query_start) + '-' + str(self.query_end) + \
               '(' + self.strand + '), ' + \
               self.target_name + ':' + str(self.target_start) + '-' + str(self.target_end) + \
               ' (' + ('%.3f' % self.percent_identity) + '%)'

    def is_exact(self):
        """
        Returns True if the alignment covers the entire query with perfect identity.
        """
        return (self.matching_bases == self.num_bases and  # 100% identity
                self.query_end - self.query_start == self.query_length)  # 100% coverage


def align_a_to_b(filename_a, filename_b, preset='asm20'):
    """
    Runs minimap2 on two sequence files (FASTA or FASTQ) and returns a list of Alignment objects.
    The first file (filename_a) is the query and the second (filename_b) is the target.
    """
    with open(os.devnull, 'w') as dev_null:
        out = subprocess.check_output(['minimap2', '--eqx', '-c', '-x', preset,
                                       str(filename_b), str(filename_a)], stderr=dev_null)
    return [Alignment(x) for x in out.decode().splitlines()]


def get_expanded_cigar(cigar):
    """
    Takes in a normal CIGAR string and returns an expanded version.
    E.g. 5=1D3= -> =====D===
    """
    expanded_cigar = []
    cigar_parts = re.findall(r'\d+[IDX=M]', cigar)
    for p in cigar_parts:
        size = int(p[:-1])
        letter = p[-1]
        expanded_cigar.append(letter * size)
    return ''.join(expanded_cigar)
