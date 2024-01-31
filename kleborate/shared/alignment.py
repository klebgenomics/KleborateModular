"""
Copyright 2024 Kat Holt
Copyright 2020 Ryan Wick (rrwick@gmail.com)
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

from Bio.Seq import Seq

from .misc import load_fasta, reverse_complement


class Alignment(object):
    """
    Defines a minimap2 alignment. Each object is created from a single line in a minimap2 PAF file.

    It is assumed that minimap2 was run with its -c option so that full alignment is performed. If
    -c wasn't used, then some pieces will be missing (e.g. CIGAR) and some will be incorrect (e.g.
    percent_identity).

    If dictionaries of the query and reference sequences are also provided (key=name, value=seq),
    then the Alignment object will also contain the
    """

    def __init__(self, paf_line, query_seqs=None, ref_seqs=None):
        self.query_name, self.query_length = None, None
        self.query_start, self.query_end = None, None
        self.strand = None
        self.ref_name, self.ref_length = None, None
        self.ref_start, self.ref_end = None, None
        self.matching_bases, self.num_bases = None, None
        self.percent_identity = None
        self.query_cov, self.ref_cov = None, None
        self.cigar, self.alignment_score = None, None
        self.query_seq, self.ref_seq = None, None

        self.parse_paf_line(paf_line)
        self.set_identity_and_coverages()
        self.set_sequences(query_seqs, ref_seqs)

    def parse_paf_line(self, paf_line):
        line_parts = paf_line.strip().split('\t')
        if len(line_parts) < 11:
            sys.exit('Error: alignment file does not seem to be in PAF format')

        self.query_name = line_parts[0]
        self.query_length = int(line_parts[1])
        self.query_start = int(line_parts[2])
        self.query_end = int(line_parts[3])
        self.strand = line_parts[4]

        self.ref_name = line_parts[5]
        self.ref_length = int(line_parts[6])
        self.ref_start = int(line_parts[7])
        self.ref_end = int(line_parts[8])

        self.matching_bases = int(line_parts[9])
        self.num_bases = int(line_parts[10])

        self.cigar, self.alignment_score = None, None
        for part in line_parts:
            if part.startswith('cg:Z:'):
                self.cigar = part[5:]
            if part.startswith('AS:i:'):
                self.alignment_score = int(part[5:])

    def set_identity_and_coverages(self):
        self.percent_identity = 100.0 * self.matching_bases / self.num_bases
        self.query_cov = 100.0 * (self.query_end - self.query_start) / self.query_length
        self.ref_cov = 100.0 * (self.ref_end - self.ref_start) / self.ref_length

    def set_sequences(self, query_seqs, ref_seqs):
        if query_seqs is not None:
            self.query_seq = query_seqs[self.query_name][self.query_start:self.query_end]
        if ref_seqs is not None:
            self.ref_seq = ref_seqs[self.ref_name][self.ref_start:self.ref_end]
            if self.strand == '-':
                self.ref_seq = reverse_complement(self.ref_seq)

    def __repr__(self):
        return self.query_name + ':' + str(self.query_start) + '-' + str(self.query_end) + \
               '(' + self.strand + '), ' + \
               self.ref_name + ':' + str(self.ref_start) + '-' + str(self.ref_end) + \
               ' (' + ('%.3f' % self.percent_identity) + '%)'

    def get_translated_ref_seq(self):
        nucl_seq = self.ref_seq
        ambiguous_bases = set(b for b in nucl_seq) - {'A', 'C', 'G', 'T'}
        for b in ambiguous_bases:
            nucl_seq = nucl_seq.split(b)[0]  # truncate to first ambiguous base
        nucl_seq = nucl_seq[:len(nucl_seq) // 3 * 3]  # truncate to a multiple of 3
        coding_dna = Seq(nucl_seq)
        return str(coding_dna.translate(table='Bacterial', to_stop=True))

    def is_exact(self):
        """
        Returns True if the alignment covers the entire query with perfect identity.
        """
        return (self.matching_bases == self.num_bases and  # 100% identity
                self.query_end - self.query_start == self.query_length)  # 100% coverage


def align_query_to_ref(query_filename, ref_filename, ref_index=None, preset='map-ont',
                       min_identity=None, min_query_coverage=None):
    """
    Runs minimap2 on two sequence files (FASTA or FASTQ) and returns a list of Alignment objects.
    Optional arguments:
    * ref_index: a minimap2 index for the reference. If provided, this will save a bit of time
                 because minimap2 won't need to make the index.
    * preset: the value for minimap2's preset option (-x)
    * min_identity: if provided, alignments with an identity lower than this are discarded.
                    Expressed as a percentage, so values should be 0-100.
    * min_query_coverage: if provided, alignments with a query coverage lower than this are
                          discarded. Expressed as a percentage, so values should be 0-100.
    """
    query_seqs = dict(load_fasta(query_filename))
    ref_seqs = dict(load_fasta(ref_filename))
    ref = ref_filename if ref_index is None else ref_index
    with open(os.devnull, 'w') as dev_null:
        out = subprocess.check_output(['minimap2', '--eqx', '-c', '-x', preset,
                                       str(ref), str(query_filename)], stderr=dev_null)
    alignments = [Alignment(x, query_seqs=query_seqs, ref_seqs=ref_seqs)
                  for x in out.decode().splitlines()]
    if min_identity is not None:
        alignments = [a for a in alignments if a.percent_identity >= min_identity]
    if min_query_coverage is not None:
        alignments = [a for a in alignments if a.query_cov >= min_query_coverage]
    return alignments


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


def hits_overlap(a, b):
    if a.ref_start <= b.ref_end and b.ref_start <= a.ref_end:  # There is some overlap
        allowed_overlap = 50
        overlap_size = min(a.ref_end, b.ref_end) - max(a.ref_start, b.ref_start) + 1
        return overlap_size > allowed_overlap
    else:
        return False


def overlapping(hits, existing_hits):
    # Only consider hits in the same reading frame.
    existing_hits = [h for h in existing_hits if
                     h.strand == hits.strand and h.ref_name == hits.ref_name]

    for existing_hit in existing_hits:
        if hits_overlap(hits, existing_hit):
            return True

    return False


def call_redundant_hits(hits):
    
    # Sort the hits from best to worst. Hit quality is defined as the product of gene coverage,
    # identity 
    
    minimap_hits = sorted(hits, key=lambda x: (1/(x.percent_identity * x.alignment_score * x.query_cov), x.query_name))

    filtered_minimap_hits = []

    for h in minimap_hits:
        if not overlapping(h, filtered_minimap_hits):
            filtered_minimap_hits.append(h)

    return filtered_minimap_hits



def truncation_check(alignment, cov_threshold=90.0):
    """
    This function checks to see if a gene alignment is truncated at the amino acid level. It
    assumes that the query sequence is a full coding sequence for a gene and the reference is an
    assembly which may or may not be a complete coding sequence.

    It returns:
    * a string to be appended to the Kleborate result, e.g. '-60%'.
    * the amino acid coverage of the reference sequence, e.g. 60.3.
    """
    # The hit must start at the first base of the gene. If not, the gene is considered 0%.
    if alignment.query_start != 0:
        return '-0%', 0.0

    # The assumption is that the reference allele is a full CDS with a stop codon at the end. This
    # isn't always true (the reference sequence is sometimes broken) but will serve to make our
    # denominator for coverage.
    query_aa_length = (alignment.query_length - 3) // 3

    translation = alignment.get_translated_ref_seq()
    coverage = 100.0 * len(translation) / query_aa_length
    if coverage >= cov_threshold:
        return '', coverage
    else:
        return '-{:.0f}%'.format(coverage), coverage