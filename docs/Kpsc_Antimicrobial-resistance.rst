
Kleborate screens for acquired resistance genes and some chromosomal mutations for which there is good evidence of association with drug resistance.

Acquired AMR genes
------------------

Kleborate screens input genomes against a curated version of the `CARD database <https://card.mcmaster.ca/>`_ of acquired resistance gene alleles (see the following `spreadsheet <https://figshare.com/articles/dataset/CARD_v3_0_8_AMR_database_curation_for_Kleborate/13256759>`_ for details on curation), and groups these by drug class for reporting purposes. The chromosomal *fosA* and *oqxAB* genes that are intrinsic to all KpSC are not reported and usually do not confer fosfomycin/fluoroquinolone resistance in these species. (Note the resistance database was recently updated; up to v1.0.0 we used an alternative database based on ARG-Annot.)

Kleborate has logic to choose the best allele hit, annotate that hit with extra information and place it in an approprirate column in the output.

In brief:


* Exact nucleotide matches are preferred, followed by exact amino acid matches, followed by inexact nucleotide matches.
* Annotations indicate aspects of the hit: ``^`` (inexact nucleotide but exact amino acid match), ``*`` (inexact nucleotide and inexact amino acid match), ``?`` (incomplete match) and ``-X%`` (truncated amino acid sequence).
* The column indicates the confidence of the hit: strong hits go in the column for their drug class, truncated hits go in the ``truncated_resistance_hits`` column and low identity/coverage hits go in the ``spurious_resistance_hits`` column.

And here is the logic in more detail:


* In order to consider a Minimap hit, it must exceed both 80% identity and 40% coverage (adjustable via the ``--min_spurious_identity`` and ``--min_spurious_coverage`` options).
* If the hit is 100% identity and 100% coverage, then it will be reported with no further annotation (e.g. ``TEM-15``\ ).
* If no exact nucleotide match is found, Kleborate searches for an exact amino acid match, and will report this with a ``^`` symbol. E.g. ``TEM-15^`` indicates an exact match to the TEM-15 protein sequence but with one or more nucleotide differences.
* If no exact amino acid match is found, the closest nucleotide match is reported with a ``*`` symbol. E.g. ``TEM-15*`` indicates no precise nucleotide or amino acid match is found, but the closest nucleotide match is to TEM-15.
* If the hit is less than 100% coverage, a ``?`` is added to the result E.g. ``TEM-15?`` indicates an incomplete match at 100% identity, and ``TEM-15*?`` indicates an incomplete match at <100% identity.
* Kleborate will next translate the hit into amino acid sequence and look for truncations (expressed as % amino acid length from the start codon). If the result is less than 90%, it is added to the result (e.g. ``TEM-15*-42%``\ ) and the hit is reported in the ``truncated_resistance_hits`` column.
* If the hit is less than 90% identity or 80% nucleotide coverage (adjustable via the ``--min_identity`` and ``--min_coverage`` options), it is reported in the ``spurious_resistance_hits`` column. Otherwise, it is reported in the column for its drug class (e.g. ``Bla_ESBL_acquired``\ ).

SHV beta-lactamases
-------------------

All KpSC carry a core chromosomal beta-lactamase gene (SHV in *K. pneumoniae*\ , LEN in *K. variicola*\ , OKP in *K. quasipneumoniae*\ ) that confers clinically significant resistance to ampicillin. Some KpSC also carry acquired mobile SHV alleles, which can confer additional inhibitor resistance and/or resistance to extended spectrum beta-lactams.

Kleborate will report all of the SHV alleles it detects and separate them into columns based on the resistance phenotype they are predicted to encode:


* SHV alleles associated with ampicillin resistance only, will be reported in the ``Bla_chr`` column because they are assumed to represent the chromosomal allele. These genes are not included in the count of acquired resistance genes or drug classes.
* Other SHV alleles e.g. those predicted to encode ESBLs (extended-spectrum beta-lactamases) or beta-lactamases with inhibitor resistance will be reported in the relevant ``Bla_ESBL_acquired`` or ``Bla_inhR_acquired`` columns etc (see below), because these SHV alleles are almost always carried on plasmids. (However it is possible to have a mutation in a chromosomal SHV gene that gives a match to an ESBL allele, which would also be reported in the ``Bla_ESBL_acquired`` column and counted as an acquired gene because it is very hard to tell the difference without manual exploration of the genetic context.)

SHV mutations associated with ESBL resistance and resistance to inhibitors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There exists large discrepancies in the functional subclass assignment (e.g. narrow-spectrum, ESBL etc.) of beta-lactamases across the various AMR databases. Functional class assignment for the SHV beta-lactamases is particularly complicated because some intrinsic SHV alleles seem to have been mis-identified as causal variants of extended-spectrum or inhibitor resistances, due to the difficulties in distinguishing chromosomal and mobile variants.

Recent mathematical modelling of the SHV alleles, followed by experimental validation, has revealed significant amino acid mutations that distinguish ESBL alleles from "wild type" narrow spectrum alleles and those with resistance to beta-lactamase inhibitors (see `this paper <https://aac.asm.org/content/64/7/e02293-19.abstract>`_ for more information). Notably, substitutions at amino acid positions 179 or 238 are essential for ESBLs while those at position 69 are linked to resistance of beta-lactamase inhibitors.

These mutations, along with those at the positions outlined in the table below, are detected and reported in the ``SHV_mutations`` column. Detection of essential mutations (i.e. those marked as class modifying) also guides the placement of novel SHV alleles to the suitable drug class column (e.g. detection of an ESBL-associated mutation at site 238 will place the novel SHV allele in the ESBL column even if the closest matching existing allele is not an ESBL).

.. list-table::
   :header-rows: 1

   * - AA site
     - Residue in SHV-1
     - Known mutations
     - Class modifying?
   * - 238
     - G
     - S, A
     - ESBL
   * - 179
     - D
     - N, A, G
     - ESBL
   * - 164-179 (omega loop)
     - RWETELNEALPGDARD
     - any change
     - ESBL
   * - 148
     - L
     - V
     - ESBL (only with 35Q)
   * - 69
     - M
     - I, L
     - Bla_inhR
   * - 234
     - K
     - R
     - Bla_inhR
   * - 235
     - T
     - A
     - Bla_inhR
   * - 25
     - A
     - T, S
     - -
   * - 35
     - L
     - Q
     - -
   * - 156
     - G
     - D
     - -
   * - 146
     - A
     - T, V
     - -
   * - 240
     - E
     - K, R
     - -


Additional chromosomal mutations associated with AMR
----------------------------------------------------


* Fluoroquinolone resistance mutations: GyrA 83 & 87 and ParC 80 & 84. These appear in the ``Flq_mutations`` column.
* Colistin resistance due to truncation or loss of core genes MgrB or PmrB. If these genes are missing or truncated, this information will be reported in the 'Col_mutations' column (truncations are expressed as % amino acid length from the start codon). Note if MgrB and PmrB are present and not truncated then nothing about them will be reported in the 'Col' column.
* OmpK35 and OmpK36 truncations and point mutations shown to result in reduced susceptibility to beta-lactamases. This information will be reported in the ``Omp_mutations`` column (truncations are expressed as % amino acid length from the start codon). Note if these core genes are present and not truncated then nothing about them will be reported in the 'Omp' column. The specific effect of OmpK mutations on drug susceptibility depends on multiple factors including what combinations of OmpK35 and OmpK36 alleles are present and what beta-lactamase genes are present (this is why we report them in their own column separate to Bla genes). See e.g. `paper <https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1007218>`_ and `this one <https://www.nature.com/articles/s41467-019-11756-y>`_ for more information on OmpK genes and drug resistance.

Note these do not count towards acquired resistance gene counts, but do count towards drug classes (with the exception of Omp mutations, whose spectrum of effects depends on the presence of acquired beta-lactamases and thus their impact on specific beta-lactam drug classes is hard to predict).

Reporting of AMR determinants by drug class
-------------------------------------------

All resistance results (both for the gene screen and mutation screen) are grouped by drug class (according to the `ARG-Annot <https://www.ncbi.nlm.nih.gov/pubmed/24145532>`_ DB), with beta-lactamases broken down into Lahey classes (now maintained at `BLDB <http://www.bldb.eu/>`_\ ), as follows: 


* AGly_acquired (aminoglycosides)
* Bla_acquired (beta-lactamases)
* Bla_inhR (beta-lactamases with resistance to beta-lactamase inhibitors)
* Bla_Carb (carbapenemase)
* Bla_ESBL (extended spectrum beta-lactamases)
* Bla_ESBL_inhR (extended spectrum beta-lactamases with resistance to beta-lactamase inhibitors)
* Fcyn (fosfomycin)
* Flq (fluoroquinolones)
* Gly (glycopeptides)
* MLS (macrolides)
* Phe (phenicols)
* Rif (rifampin)
* Sul (sulfonamides)
* Tet (tetracyclines)
* Tmt (trimethoprim)
* Tgc (tigecycline)

Note there is a separate column ``Omp_mutations`` reporting known resistance-related mutations in the OmpK35 and OmpK36 osmoporins. See above for details.

Note that Kleborate reports resistance results for all antimicrobial classes with confidently attributable resistance mechanisms in KpSC. Not all of these are actually used clinically for treatment of KpSC infections (e.g. MLS, Rif) but they are still reported as the presence of acquired resistance determinants to these classes is of interest to researchers for other reasons (e.g. these genes can be useful markers of MGEs and MGE spread; there is potential for use of these drugs against other organisms to select for KpSC in co-infected patients or in the environment). For an overview of antimicrobial resistance and consensus definitions of multidrug resistance (MDR), extensive drug resistance (XDR) and pan drug resistance in Enterobacteriaceae, see `Magiorakos 2012 <https://www.clinicalmicrobiologyandinfection.com/article/S1198-743X(1461632-3/fulltext)>`_\ 
