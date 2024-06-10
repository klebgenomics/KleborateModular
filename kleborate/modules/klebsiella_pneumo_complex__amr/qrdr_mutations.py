"""
Copyright 2024 Kat Holt
Copyright 2024 Ryan Wick (rrwick@gmail.com)
Copyright 2024 (gathonimaranga@gmail.com)
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
from Bio import pairwise2
from Bio.Align import substitution_matrices
from ...shared.alignment import align_query_to_ref, is_exact_aa_match, translate_nucl_to_prot, check_for_exact_aa_match, truncation_check, get_bases_per_ref_pos
from ...shared.misc import load_fasta, reverse_complement



def check_for_qrdr_mutations(hits_dict, assembly, qrdr, min_identity, min_coverage):
    
    """
    This function checks for qrdr mutations
    
    This function returns:
    * a hits dictionary with Fluoroquinolone(Qrdr) mutations
    """

    qrdr_loci = {'GyrA': [(83, 'S'), (87, 'D')],
                     'ParC': [(80, 'S'), (84, 'E')]}

    gyra_ref = 'MSDLAREITPVNIEEELKNSYLDYAMSVIVGRALPDVRDGLKPVHRRVLYAMNVLGNDWN' \
               'KAYKKSARVVGDVIGKYHPHGDSAVYDTIVRMAQPFSLRYMLVDGQGNFGSIDGDSAAAM'
    parc_ref = 'MSDMAERLALHEFTENAYLNYSMYVIMDRALPFIGDGLKPVQRRIVYAMSELGLNASAKF' \
               'KKSARTVGDVLGKYHPHGDSACYEAMVLMAQPFSYRYPLVDGQGNWGAPDDPKSFAAMRY'

    blosum62 = substitution_matrices.load('BLOSUM62')

    snps = []

    alignment_hits = align_query_to_ref(qrdr, assembly, min_query_coverage=None, min_identity=min_identity) 
    for hit in alignment_hits:
        _, coverage, translation = truncation_check(hit)
        
        if coverage > min_coverage:
            if hit.query_name == 'GyrA':
                alignments = pairwise2.align.globalds(gyra_ref, translation, blosum62, -10, -0.5)
            elif hit.query_name == 'ParC':
                alignments = pairwise2.align.globalds(parc_ref, translation, blosum62, -10, -0.5)
            else:
                assert False
            bases_per_ref_pos = get_bases_per_ref_pos(alignments[0])
            loci = qrdr_loci[hit.query_name]

            for pos, wt_base in loci:
                assembly_base = bases_per_ref_pos[pos]
                if pos in bases_per_ref_pos and assembly_base != wt_base \
                        and assembly_base != '-' and assembly_base != '.':
                    snps.append(hit.query_name + '-' + str(pos) + assembly_base)

        
    if snps:
        hits_dict['Flq_mutations'] += snps
