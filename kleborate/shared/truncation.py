"""
Copyright 2024 Kat Holt
https://github.com/katholt/Kleborate/

This file is part of Kleborate. Kleborate is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Kleborate is distributed in
the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Kleborate. If
not, see <http://www.gnu.org/licenses/>.
"""

from Bio.Seq import Seq

def truncation_check(hit, cov_threshold=90.0):
    """
    This function checks to see if a gene alignment is truncated at the amino acid level. It
    assumes that the query sequence is a full coding sequence for a gene and the reference is an
    assembly which may or may not be a complete coding sequence.

    It returns:
    * a string to be appended to the Kleborate result, e.g. '-60%'.
    * the amino acid coverage of the reference sequence, e.g. 60.3.
    """
    # The hit must start at the first base of the gene. If not, the gene is considered 0%.
    if hit.query_start != 0:
        return '-0%', 0.0,''

    # The assumption is that the reference allele is a full CDS with a stop codon at the end. This
    # isn't always true (the reference sequence is sometimes broken) but will serve to make our
    # denominator for coverage.
    query_aa_length = (hit.query_length - 3) // 3

    translation = hit.get_translated_ref_seq()
    coverage = 100.0 * len(translation) / query_aa_length
    
    if coverage >= cov_threshold:
        return '', coverage, translation
    else:
        return '-{:.0f}%'.format(coverage), coverage, translation


