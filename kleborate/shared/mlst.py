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

import re

from .alignment import align_a_to_b


def mlst(assembly_path, profiles_path, allele_paths, min_identity, min_coverage,
         required_exact_matches):
    """
    This function takes:
    * assembly_path: a path for an assembly in FASTA format
    * profiles_path: a path for the MLST profiles file in TSV format
    * allele_paths: a dictionary {gene name: path for the allele FASTA file}
    * min_identity: hits with a lower percent identity than this are discarded
    * min_coverage: hits with a lower percent coverage than this are discarded
    * required_exact_matches: at least this many alleles in the ST must be an exact match for this
                              function to assign an ST

    This function returns:
    * the best matching ST profile (e.g. 'ST123', 'ST456-1LV' or 'NA')
    * a dictionary of allele numbers {gene name: allele number}
    """
    profiles, gene_names = load_st_profiles(profiles_path)
    best_hits_per_gene = get_best_hits_per_gene(gene_names, allele_paths, assembly_path,
                                                min_identity, min_coverage)
    best_st, best_st_alleles = get_best_matching_profile(profiles, gene_names, best_hits_per_gene)
    best_hit_per_gene = get_best_hit_per_gene(gene_names, best_hits_per_gene, best_st_alleles)

    exact_matches, lv_count, allele_numbers = 0, 0, {}
    for gene_name, st_allele in zip(gene_names, best_st_alleles):
        hit = best_hit_per_gene[gene_name]
        hit_allele = number_from_hit(hit)

        if hit is None:
            allele_numbers[gene_name] = '-'
        elif hit.is_exact():
            allele_numbers[gene_name] = str(hit_allele)
        else:
            allele_numbers[gene_name] = str(hit_allele) + '*'

        if hit is not None and hit.is_exact() and st_allele == hit_allele:
            exact_matches += 1
        else:
            lv_count += 1

    if exact_matches < required_exact_matches:
        best_st = 'NA'
    elif lv_count == 0:
        best_st = 'ST' + str(best_st)
    else:
        best_st = 'ST' + str(best_st) + f'-{lv_count}LV'

    return best_st, allele_numbers


def load_st_profiles(database_path):
    """
    This function reads through a tab-delimited MLST database file where the first column is the ST
    number and the subsequent columns are allele numbers. The first line of the file should be a
    header ('ST' followed by gene names), and all other lines should only contain positive
    integers.

    This function returns:
    * A list of ST profiles, where each value is a tuple: (ST number, list of allele numbers).
    * A list of the gene names for this MLST scheme
    """
    profiles, gene_names = [], []
    with open(database_path, 'r') as f:
        for line in f:
            parts = line.rstrip('\n').split('\t')
            if len(gene_names) == 0:
                gene_names = parts[1:]
            else:
                st = int(parts[0])
                alleles = [int(a) for a in parts[1:]]
                profiles.append((st, alleles))
    return profiles, gene_names


def get_best_hits_per_gene(gene_names, allele_paths, assembly_path, min_identity, min_coverage):
    """
    This function does the alignment of each gene's allele's to the assembly. It returns a
    dictionary where key is the gene name and value is a list of the best hits (Alignment objects)
    for that gene. For most genes, there will be only one hit (a list of one), but multiple best
    hits are possible.
    """
    best_hit_per_gene = {}
    for gene in gene_names:
        assert gene in allele_paths
        hits = align_a_to_b(allele_paths[gene], assembly_path)
        best_hit = get_best_hits(hits, min_identity, min_coverage)
        best_hit_per_gene[gene] = best_hit
    return best_hit_per_gene


def get_best_hits(hits, min_identity, min_coverage):
    """
    Given a bunch of hits to an allele, this function returns a list of the best hits. 'Best' is
    defined as highest identity. If there is a tie, hits with higher alignment scores are
    preferred. Usually this results in just a single hit, but if there is still a tie (i.e. same
    identity and same alignment score), then multiple hits can be returned. This function can also
    return an empty list where then are no hits which meet the identity and coverage thresholds.
    """
    hits = [h for h in hits if h.percent_identity >= min_identity and h.query_cov >= min_coverage]
    if not hits:
        return []
    best_identity = max(h.percent_identity for h in hits)
    hits = [h for h in hits if h.percent_identity == best_identity]
    best_score = max(h.alignment_score for h in hits)
    return [h for h in hits if h.alignment_score == best_score]


def number_from_hit(hit):
    """
    Given an alignment, returns the numerical part of the query name as an int. E.g if the query
    name was gapA_234, it will return 234.
    """
    if hit is None:
        return 0
    try:
        return int(re.sub('[^0-9]', '', hit.query_name))
    except ValueError:
        return 0


def get_best_matching_profile(profiles, gene_names, best_hits_per_gene):
    """
    This function looks for an ST which best matches the hits. Each ST is scored based on the
    number of genes which have a matching hit (i.e. a hit with the same number). So the score for
    any ST can be 0 to the number of genes in the scheme.
    """
    best_st, best_st_alleles, best_matches = 0, [0] * len(gene_names), 0
    for st, alleles in profiles:
        matches = 0
        for gene_name, allele in zip(gene_names, alleles):
            if any(allele == number_from_hit(h) for h in best_hits_per_gene[gene_name]):
                matches += 1
        if matches > best_matches:
            best_st = st
            best_st_alleles = alleles
            best_matches = matches
    return best_st, best_st_alleles


def get_best_hit_per_gene(gene_names, best_hits_per_gene, st_alleles):
    """
    This function takes the best_hits_per_gene dict, and for any genes that have multiple hits, it
    chooses a single hit. Which hit is chosen is first based on the ST call, i.e. if one of the
    hits matches the ST allele, that's chosen. If none of the hits match the ST allele, then the
    lowest allele number is chosen.
    """
    best_hit_per_gene = {}
    for gene_name, st_allele in zip(gene_names, st_alleles):
        best_hits = best_hits_per_gene[gene_name]
        hits_matching_st = [h for h in best_hits if number_from_hit(h) == st_allele]
        if not best_hits:
            best_hit_per_gene[gene_name] = None
        elif hits_matching_st:
            best_hit_per_gene[gene_name] = hits_matching_st[0]
        else:
            best_hit_per_gene[gene_name] = sorted(best_hits, key=lambda h: number_from_hit(h))[0]
    return best_hit_per_gene
