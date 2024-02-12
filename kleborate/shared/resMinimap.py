"""
Search for resistance genes, summarise by class (one class per column)

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

import collections

from collections import defaultdict
from Bio import pairwise2
from Bio.Align import substitution_matrices
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.Data.CodonTable import TranslationError
 
from .alignment import align_query_to_ref, call_redundant_hits, is_exact_aa_match, translate_nucl_to_prot, check_for_exact_aa_match, truncation_check
from .misc import load_fasta, reverse_complement
from kleborate.modules.kpsc_amr.shv_mutations import*



def resminimap_assembly(assembly, ref_file, gene_info, qrdr, trunc, omp,  min_cov, min_ident,
                          min_spurious_cov, min_spurious_ident):
    hits_dict = minimap_against_all(assembly, ref_file, gene_info, min_ident, min_spurious_cov, min_spurious_ident, min_cov)
    
    if qrdr:
        check_for_qrdr_mutations(hits_dict, assembly, qrdr, min_ident, 90.0)
        
    if trunc:
        check_for_mgrb_pmrb_gene_truncations(hits_dict, assembly, trunc, min_ident)
    if omp:
        check_omp_genes(hits_dict, assembly, omp, min_ident, 90.0)
    return hits_dict


def read_class_file(res_class_file):
    gene_info = {}  # key = sequence id (fasta header in ref file), value = (allele,class,Bla_Class)
    res_classes = []
    bla_classes = ['Bla', 'Bla_inhR', 'Bla_ESBL', 'Bla_ESBL_inhR', 'Bla_Carb', 'Bla_chr']

    with open(res_class_file, 'r') as f:
        header = 0
        for line in f:
            if header == 0:
                header = 1
                # clusterid,queryID,class,gene,allele,seqID,accession,positions,size,
                # cluster_contains_multiple_genes,gene_found_in_multiple_clusters,bla_description,
                # bla_class
            else:
                fields = line.rstrip().split(',')

                cluster_id, res_class, gene, allele_symbol, seq_id, bla_class = \
                    fields[0], fields[2], fields[3], fields[4], fields[5], fields[12]
                seq_header = '__'.join([cluster_id, gene + '_' + res_class, allele_symbol, seq_id])

                if res_class == 'Bla' and bla_class == 'NA':
                    bla_class = 'Bla'
                gene_info[seq_header] = (allele_symbol, res_class, bla_class)
                if res_class not in res_classes:
                    res_classes.append(res_class)
                if bla_class not in bla_classes:
                    bla_classes.append(bla_class)

    res_classes.sort()
    if 'Bla' in res_classes:
        res_classes.remove('Bla')
    if 'NA' in bla_classes:
        bla_classes.remove('NA')

    if 'SHV_mutations' not in res_classes:
        res_classes.append('SHV_mutations')
    if 'Omp_mutations' not in res_classes:
        res_classes.append('Omp_mutations')
    if 'Col_mutations' not in res_classes:
        res_classes.append('Col_mutations')
    if 'Flq_mutations' not in res_classes:
        res_classes.append('Flq_mutations')

    return gene_info, res_classes, bla_classes


def get_res_headers(res_classes, bla_classes):
    res_headers = res_classes + bla_classes

    # Rearrange the headers a bit. First move Bla_chr to the end:
    res_headers = ([h for h in res_headers if h != 'Bla_chr'] +
                   [h for h in res_headers if h == 'Bla_chr'])

    # Then move mutation columns to the end:
    res_headers = ([h for h in res_headers if '_mutations' not in h] +
                   [h for h in res_headers if '_mutations' in h])

    # Add '_acquired' to the end of the rest of the columns:
    res_headers = [h if h.endswith('_chr') or h.endswith('_mutations') else h + '_acquired'
                   for h in res_headers]

    return res_headers


def minimap_against_all(assembly, ref_file, gene_info, min_ident, min_spurious_cov, min_spurious_ident, min_cov):
    
    """
    This function takes:
    * assembly:  assembly in FASTA format
    * ref_file: a path for a CARD reference in FASTA format
    * minimap2_index: a path for the assembly's minimap2 index (for faster alignment) (optional)
    * min_identity: hits with a lower percent identity than this are discarded
    
    This function returns:
    * dictionary with SHV mutations, truncated_resistance_hits, spurious_resistance_hits, _acquired mutations
    """
    
    hits_dict = collections.defaultdict(list)  # key = class, value = list
    alignment_hits = align_query_to_ref(ref_file, assembly, min_identity=min_ident, min_query_coverage=None)
    alignment_hits = call_redundant_hits(alignment_hits)
    
    # calculate alignment coverage
    for hit in alignment_hits:
        alignment_length = hit.ref_end - hit.ref_start
        coverage = (alignment_length / hit.query_length) * 100
        if coverage >= min_spurious_cov:
            if hit.percent_identity < 100.0:
                aa_result = check_for_exact_aa_match(ref_file, hit, assembly)
                if aa_result is not None:
                    hit.query_name = aa_result
                    exact_match = True
                else:
                    exact_match = False
            else:
                aa_result = None
                exact_match = True
                

            hit_allele, hit_class, hit_bla_class = gene_info[hit.query_name]
            

            hit_bla_class, shv_muts, class_changing_muts, omega_loop_seq = \
                    check_for_shv_mutations(hit, hit_allele, hit_bla_class, exact_match)
            
            # checks if the variable hit_class contains the string value 'Bla'
            # If it does, then the value of hit_class is replaced with the value of hit_bla_class.
            if hit_class == 'Bla':
                hit_class = hit_bla_class

            # append the list shv_muts to hits_dict['SHV_mutations']
            hits_dict['SHV_mutations'] += shv_muts
            if omega_loop_seq is not None:
                hits_dict['SHV_mutations'].append(f'omega-loop={omega_loop_seq}')

            # checks if the list associated with the 'SHV_mutations' key in the hits_dict dictionary is empty
            # If it is, the key 'SHV_mutations' and its associated value are deleted from the dictionary.
            if not hits_dict['SHV_mutations']:
                del hits_dict['SHV_mutations']

            # checks if the value in hit_class does not end with the strings '_chr' or '_mutations'.
            # append '_acquired'  to hit_class
            if not (hit_class.endswith('_chr') or hit_class.endswith('_mutations')):
                hit_class += '_acquired'

            trunc_cov = 100.0
            if aa_result is not None:
                hit_allele += '^'
            else:
                if hit.percent_identity < 100:
                    hit_allele += '*'
                    
                if hit.ref_length < hit.query_length:
                        hit_allele += '?'
                trunc_suffix, trunc_cov, _ = truncation_check(hit)
                hit_allele += trunc_suffix
                
            if class_changing_muts:
                hit_allele += ' +' + ' +'.join(class_changing_muts)
            
            
            # If the hit is decent (above the min coverage and identity thresholds), it goes in the
            # column for the class.
            if coverage >= min_cov and hit.percent_identity >= min_ident and trunc_cov >= 90.0:
                hits_dict[hit_class].append(hit_allele)
                
            # If the hit is decent but the gene is truncated, it goes in the
            # truncated_resistance_hits column.
            elif coverage >= min_cov and hit.percent_identity >= min_ident and trunc_cov < 90.0:
                hits_dict['truncated_resistance_hits'].append(hit_allele)
                
            # If the hit is bad (below the min coverage and identity thresholds but above the
            # thresholds for spurious hits) then it goes in the spurious hit column.
            else:
                hits_dict['spurious_resistance_hits'].append(hit_allele)
    
    return hits_dict


def check_for_qrdr_mutations(hits_dict, assembly, qrdr, min_ident, min_cov):
    
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

    alignment_hits = align_query_to_ref(qrdr, assembly)
    for hit in alignment_hits:
        _, coverage, translation = truncation_check(hit)
        
        if coverage > min_cov:
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


def get_bases_per_ref_pos(alignment):
    aligned_seq1, aligned_seq2 = alignment[0], alignment[1]
    bases_per_ref_pos = {}
    ref_pos = 1
    for i, ref_b in enumerate(aligned_seq1):
        if ref_b == '-' or ref_b == '.':
            continue
        assembly_b = aligned_seq2[i]
        bases_per_ref_pos[ref_pos] = assembly_b
        ref_pos += 1
    return bases_per_ref_pos


def check_for_mgrb_pmrb_gene_truncations(hits_dict, assembly, trunc, min_ident):
    best_mgrb_cov, best_pmrb_cov = 0.0, 0.0

    alignment_hits = align_query_to_ref(trunc, assembly, min_identity=None)
    for hit in alignment_hits:
        assert hit.query_name == 'pmrB' or hit.query_name == 'mgrB'
        _, coverage, _ = truncation_check(hit)
        
        if hit.query_name == 'mgrB' and coverage > best_mgrb_cov:
            best_mgrb_cov = coverage
        elif hit.query_name == 'pmrB' and coverage > best_pmrb_cov:
            best_pmrb_cov = coverage
            

    truncations = []
    if best_mgrb_cov < 90.0:
        truncations.append('MgrB-' + ('%.0f' % best_mgrb_cov) + '%')
    if best_pmrb_cov < 90.0:
        truncations.append('PmrB-' + ('%.0f' % best_pmrb_cov) + '%')

    if truncations:
        hits_dict['Col_mutations'] += truncations


def check_omp_genes(hits_dict, assembly, omp, min_ident, min_cov):

    best_ompk35_cov, best_ompk36_cov = 0.0, 0.0
    
    alignment_hits = align_query_to_ref(omp, assembly, min_identity=None, min_query_coverage=None)
    
    for hit in  alignment_hits:
        _, coverage, translation = truncation_check(hit)
        
        if hit.query_name == 'OmpK35':
            if coverage > best_ompk35_cov:
                best_ompk35_cov = coverage

        elif hit.query_name == 'OmpK36':
            if coverage > best_ompk36_cov:
                best_ompk36_cov = coverage

            if coverage >= min_cov:
                if 'GDGDTY' in translation:
                    hits_dict['Omp_mutations'].append('OmpK36GD')
                    
                elif 'GDTDTY' in translation:
                    hits_dict['Omp_mutations'].append('OmpK36TD')
        else:
            assert False


    truncations = []
    if best_ompk35_cov < 90.0:
        truncations.append('OmpK35-' + ('%.0f' % best_ompk35_cov) + '%')
   
    if best_ompk36_cov < 90.0:
        truncations.append('OmpK36-' + ('%.0f' % best_ompk36_cov) + '%')
    

    if truncations:
        if 'Omp_mutations' not in hits_dict:
            hits_dict['Omp_mutations'] = []
        hits_dict['Omp_mutations'] += truncations




