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
from ...shared.alignment import align_query_to_ref, call_redundant_hits, is_exact_aa_match, translate_nucl_to_prot, check_for_exact_aa_match, truncation_check


def check_omp_genes(hits_dict, assembly, omp, min_identity, min_coverage):

    best_ompk35_cov, best_ompk36_cov = 0.0, 0.0
    
    alignment_hits = align_query_to_ref(omp, assembly, min_query_coverage=None, min_identity=min_identity)
    alignment_hits = call_redundant_hits(alignment_hits)
    
    ompk35_hit = False
    ompk36_hit = False
    
    for hit in alignment_hits:
        _, coverage, translation = truncation_check(hit)
        
        if hit.query_name == 'OmpK35':
            ompk35_hit = True
            if coverage > best_ompk35_cov:
                best_ompk35_cov = coverage

        elif hit.query_name == 'OmpK36':
            ompk36_hit = True
            if coverage > best_ompk36_cov:
                best_ompk36_cov = coverage

            if coverage >= min_coverage:
                if 'GDGDTY' in translation:
                    hits_dict['Omp_mutations'].append('OmpK36GD')
                    
                elif 'GDTDTY' in translation:
                    hits_dict['Omp_mutations'].append('OmpK36TD')
        else:
            assert False

    truncations = []
    if ompk35_hit and best_ompk35_cov < 90.0:
        truncations.append('OmpK35-' + ('%.0f' % best_ompk35_cov) + '%')
   
    if ompk36_hit and best_ompk36_cov < 90.0:
        truncations.append('OmpK36-' + ('%.0f' % best_ompk36_cov) + '%')
    

    if truncations:
        if 'Omp_mutations' not in hits_dict:
            hits_dict['Omp_mutations'] = []
        hits_dict['Omp_mutations'] += truncations

# def check_omp_genes(hits_dict, assembly, omp, min_identity, min_coverage):

#     best_ompk35_cov, best_ompk36_cov = 0.0, 0.0
    
#     alignment_hits = align_query_to_ref(omp, assembly, min_query_coverage=None, min_identity=min_identity)
#     alignment_hits = call_redundant_hits(alignment_hits)
    
#     for hit in  alignment_hits:
#         _, coverage, translation = truncation_check(hit)
        
#         if hit.query_name == 'OmpK35':
#             if coverage > best_ompk35_cov:
#                 best_ompk35_cov = coverage
                

#         elif hit.query_name == 'OmpK36':
#             if coverage > best_ompk36_cov:
#                 best_ompk36_cov = coverage

#             if coverage >= min_coverage:
#                 if 'GDGDTY' in translation:
#                     hits_dict['Omp_mutations'].append('OmpK36GD')
                    
#                 elif 'GDTDTY' in translation:
#                     hits_dict['Omp_mutations'].append('OmpK36TD')
#         else:
#             assert False
    
    

#     truncations = []
#     if best_ompk35_cov > 0.0 and best_ompk35_cov < 90.0:
#         truncations.append('OmpK35-' + ('%.0f' % best_ompk35_cov) + '%')
   
#     if best_ompk36_cov > 0.0 and best_ompk36_cov < 90.0:
#         truncations.append('OmpK36-' + ('%.0f' % best_ompk36_cov) + '%')
    

#     if truncations:
#         if 'Omp_mutations' not in hits_dict:
#             hits_dict['Omp_mutations'] = []
#         hits_dict['Omp_mutations'] += truncations


# def check_omp_genes(hits_dict, assembly, omp, min_identity, min_coverage):

#     best_ompk35_cov, best_ompk36_cov = 0.0, 0.0
    
#     alignment_hits = align_query_to_ref(omp, assembly, min_query_coverage=None, min_identity=min_identity)
#     alignment_hits = call_redundant_hits(alignment_hits)
    
#     for hit in alignment_hits:
#         _, coverage, translation = truncation_check(hit)
        
#         if hit.query_name == 'OmpK35':
#             if coverage > best_ompk35_cov:
#                 best_ompk35_cov = coverage

#         elif hit.query_name == 'OmpK36':
#             if coverage > best_ompk36_cov:
#                 best_ompk36_cov = coverage

#             if coverage >= min_coverage:
#                 if 'GDGDTY' in translation:
#                     hits_dict['Omp_mutations'].append('OmpK36GD')
                    
#                 elif 'GDTDTY' in translation:
#                     hits_dict['Omp_mutations'].append('OmpK36TD')
#         else:
#             assert False

#     truncations = []
#     if best_ompk35_cov < 90.0:
#         truncations.append('OmpK35-' + ('%.0f' % best_ompk35_cov) + '%')
   
#     if best_ompk36_cov < 90.0:
#         truncations.append('OmpK36-' + ('%.0f' % best_ompk36_cov) + '%')
    

#     if truncations:
#         if 'Omp_mutations' not in hits_dict:
#             hits_dict['Omp_mutations'] = []
#         hits_dict['Omp_mutations'] += truncations
