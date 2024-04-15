.. role:: raw-html-m2r(raw)
   :format: html


KleborateModular examines five key acquired virulence loci that are associated with invasive infections and are found at high prevalence among hypervirulent *K. pneumoniae* strains: the siderophores yersiniabactin (\ *ybt*\ ), aerobactin (\ *iuc*\ ) and salmochelin (\ *iro*\ ), the genotoxin colibactin (\ *clb*\ ), and the hypermucoidy locus *rmpADC*. Each of these loci comprises multiple genes and will only be reported if >50% of the genes are detected. We also screen for the alternative hypermucoidy marker gene *rmpA2*.

When the *ybt*\ , *clb*\ , *iuc*\ , *iro* or *rmpADC* loci are detected KleborateModular will:


* Call a sequence type using the same logic as for `7-gene MLST <https://github.com/katholt/Kleborate/wiki/MLST>`_
* Report the phylogenetic lineage associated with each sequence type, as outlined below and detailed in the corresponding papers
* Report the structural variant of the mobile genetic element that is usually associated with that phylogenetic lineage (for *ybt* and *iuc* only)

The *ybt*\ , *clb*\ , *iuc*\ , *iro* and *rmpADC* locus-specific ST schemes are defined in the *K. pneumoniae* `BIGSdb <http://bigsdb.pasteur.fr/klebsiella/klebsiella.html>`_.

Notes on virulence allele reporting:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Virulence alleles are treated in the same way as [MLST] alleles:


* In order to consider a Minimap2 hit, it must exceed both 80% identity and 40% coverage (adjustable via the --min_spurious_identity and --min_spurious_coverage options).
* Hits that fail to meet 90% identity and 80% coverage (adjustable via the ``--min_identity`` and ``--min_coverage`` options) are reported in the ``spurious_virulence_hits`` column but not used for sequence typing.
* Imperfect hits (either <100% identity or <100% coverage) are reported with a ``*``. E.g. ``15*`` means that no perfect match was found but the closest match is allele 15.
* KleborateModular will next translate the hit into amino acid sequence and look for truncations (expressed as % amino acid length from the start codon). If the result is less than 90%, it is added to the result (e.g. ``15*-42%``\ ).

Notes on virulence sequence type reporting:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Virulence locus STs are only reported if >50% of the genes in a locus are detected (e.g. at least 6 of the 11 *ybt* locus genes are required to report a *ybt* ST).
* If <50% of the genes in a locus are detected, KleborateModular reports the ST as ``0`` and the lineage as ``-``.
* If <100% but >50% of the genes in a locus are detected, KleborateModular will report the locus as (incomplete), along with the closest matching ST and its corresponding phylogenetic lineage. E.g. if only 7 of the 11 *ybt* genes are detected, this will be reported as ``ybtX; ICEKpX (incomplete)``.
* For genomes with multiple copies of a virulence locus (e.g. a strain that carries ICE *Kp1* and the KpVP-1 plasmid will have two copies of *iro* and *rmp*\ ), KleborateModular will report and assign a ST or closest matching ST to each of these virulence loci provided that the locus is relatively intact in the genome (i.e. >50% of the genes in a locus are present on a single contig) and according to the above criteria.  

Yersiniabactin and colibactin (primarily mobilised by ICE *Kp*)
---------------------------------------------------------------------------------------

We previously explored the diversity of the *K. pneumoniae* integrative conjugative element (ICE *Kp*), which mobilises the yersiniabactin locus *ybt*, using genomic analysis of a diverse set of 2498 *Klebsiella* (see `this paper <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_\ ). Overall, we found *ybt* in about a third of all *K. pneumoniae* genomes (and *clb* in about 14%). We identified 17 distinct lineages of *ybt* (see figure) embedded within 14 structural variants of ICE *Kp* that can integrate at any of four tRNA-Asn sites in the chromosome. Based on this analysis, we developed a MLST-style approach for assigning yersiniabactin sequence types (YbST) and colibactin sequence types (CbST), which is implemented in KleborateModular. 

The allele databases and schemes were updated in June 2021 following inspection of 250 genomes for which Kleborate had identified putative novel ybt sequence types/lineages (unpublished). This update included the addition of 11 novel ybt lineages and 8 novel ICE *Kp* variants for yersiniabactin, increasing the total number of ybt lineages from 17 to 28 and ICE *Kp* variants from 14 to 22 (see figure below). Annotations for all reference ICE *Kp1* sequences are available in the ICE *Kp* references folder in the data directory.


* Three of the 28 *ybt* lineages were associated with three lineages of colibactin, with which they are co-located in the same ICE structure designated ICE *Kp* : *ybt 12* with *clb 1*\ , *ybt 1* with *clb 2* (previously defined as *clb 2A* in Lam et al. 2018), *ybt 17* with *clb 3* (previously defined as *clb 2B* in Lam et al. 2018) 
* One ICE structure (ICE *Kp1*) carries a variant of the salmochelin synthesis locus *iro* (\ *iro3*\ ) and *rmpADC* hypermucoidy lineage 3 (\ *rmp3*\ ; see below for more detail) in addition to *ybt* lineage 2 (\ *ybt 2*\ ). 
* Additionally, one lineage of *ybt* is plasmid-encoded (\ *ybt 4*\ ). 

ICE *Kp1* is occasionally found in other species within the KpSC, and even in other genera of Enterobacteriaceae (see `original paper <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_\ ), however most of the known variation included in the database is derived from *K. pneumoniae*.


Aerobactin and salmochelin (primarily mobilised by virulence plasmids)
----------------------------------------------------------------------

We further explored the genetic diversity of the aerobactin (\ *iuc*\ ) and salmochelin (\ *iro*\ ) loci among a dataset of 2733 *Klebsiella* genomes (see `this paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_\ ). We identified five *iro* and six *iuc* lineages (see figure), each of which was associated with a specific location within *K. pneumoniae* genomes. Based on this analysis, we developed a MLST-style approach for assigning aerobactin sequence types (AbST) and salmochelin sequence types (SmST) which is implemented in Kleborate.


* The most common lineages are *iuc1* and *iro1*\ , which are found together on the FIBk virulence plasmid KpVP-1 (typified by pK2044 or pLVPK common to the hypervirulent clones ST23, ST86, etc). 
* *iuc2* and *iro2* lineages were associated with the alternative FIBk virulence plasmid KpVP-2 (typified by Kp52.145 plasmid II from the K2 ST66 lab strain known as Kp52.145 or CIP 52.145 or B5055). 
* *iuc5* and *iro5* originate from *E. coli* and are carried (often together) on *E. coli* FII plasmids that can transfer to *K. pneumoniae*. 
* The lineages *iuc2A*\ , *iuc3* and *iro4* were associated with other novel FIBk plasmids that had not been previously described in *K. pneumoniae*\ , but sequences for which are included in `the paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_. 
* The salmochelin locus present in ICE *Kp1* constitutes its own lineage *iro3*\ , and the aerobactin locus present in the chromosome of ST67 *K. pneumoniae* subsp *rhinoscleromatis* strains constitutes its own lineage *iuc4*. 


Please note that the aerobactin *iuc* and salmochelin *iro* lineage names were updated between Kleborate version 0.2.0 and 0.3.0 to match the consistent nomenclature used in `the paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_. The AbST and SmST allele numbers are unchanged. Lineage name re-assignments are:

.. list-table::
   :header-rows: 1

   * - v0.2.0
     - v0.3.0+
     - location (see `paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_ for details)
   * - *iuc 2*
     - *iuc 1*
     - KpVP-1 (e.g. pLVPK)
   * - *iuc 3B*
     - *iuc 2*
     - KpVP-2 (e.g. Kp52.145 plasmid II)
   * - *iuc 3A*
     - *iuc 2A*
     - other plasmids
   * - *iuc 4*
     - *iuc 3*
     - other plasmids
   * - *iuc 5*
     - *iuc 4*
     - rhinoscleromatis chromosome
   * - *iuc 1*
     - *iuc 5*
     - *E. coli* variant
   * - *iro 3*
     - *iro 1*
     - KpVP-1 (e.g. pLVPK)
   * - *iro 4*
     - *iro 2*
     - KpVP-2
   * - *iro 5*
     - *iro 3*
     - CE *Kp1*
   * - *iro 2*
     - *iro 4*
     - *Enterobacter* variant
   * - *iro 1*
     - *iro 5*
     - *E. coli* variant


Note on *iucA* sequence update:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Kleborate version 2.2.0 and earlier, the majority of *iucA* alleles had a sequence length of 1791 bp, with the exception being those associated with lineage *iuc 5* which have a length of 1725 bp. Related to this, *iucA* in genomes with *iuc 3* encoded a premature stop codon resulting in a significantly truncated and presumably non-functional IucA protein (i.e. at 2% length of the intact amino acid sequence), despite experimental evidence showing siderophore activity in *iuc 3*\ + isolates. In light of this evidence, the sequences of *iucA* genes with the longer ~1791 bp length were updated to ~1725 bp by removing the first 66 bp. These changes are captured in Kleborate version 2.3.0 onwards, and address the truncation issue in *iuc 3*\ + genomes. The following *iucA* alleles and AbST profiles have also been retired due to sequence redundancy following the update:


* alleles: _iucA\ *48*\ , _iucA\ *49*\ , _iucA\ *52*
* profiles: AbST 70, 82, 83

Hypermucoidy genes
------------------

The *rmpA* and *rmpA2* genes are associated with the hypermucoidy phenotype that is a virulence feature that is often observed in hypervirulent *K. pneumoniae* strains. Recent work has revealed that *rmpA* serves as a transcriptional regulator for the *rmpD* and *rmpC* genes, and together these genes comprise the *rmpADC* (or *rmp*\ ) locus. *rmpC* is involved in the upregulation of capsule expression while *rmpD* drives hypermucoviscosity (see this paper on `rmpC <https://mbio.asm.org/content/10/2/e00089-19>`_ and this one on `rmpD <https://mbio.asm.org/content/11/5/e01750-20>`_ for more information.) 

In light of this information, we screened and extracted the *rmpA*\ , *rmpD* and *rmpC* sequences from the 2733 genomes included in the aerobactin and salmochelin study, and generated a RmST typing scheme. We observed four distinct *rmp* lineages, which were associated with the KpVP-1 (\ *rmp 1*\ ), KpVP-2 (\ *rmp 2*\ ), *iuc2A* virulence plasmids (\ *rmp 2A*\ ) and ICE *Kp1* (rmp 3). The details of this novel virulence typing scheme have not yet been published. As mentioned above, Kleborate will screen for *rmpADC* and report a sequence type, along with the associated lineage and mobile genetic element, in addition to screening for *rmpA2*\ , which is reported in a separate column.

Note:
~~~~~


* Alleles for each gene are sourced from the `BIGSdb <http://bigsdb.pasteur.fr/klebsiella/klebsiella.html>`_\ , while additional *rmpA* alleles have also been added to Kleborate.
* The *rmpA* and *rmpA2* share ~83% nucleotide identity so are easily distinguished.
* Unique (non-overlapping) nucleotide Minimap2 hits with >95% identity and >50% coverage are reported. Note multiple hits to the same gene are reported if found. E.g. the NTUH-K2044 genome carries *rmpA* in the virulence plasmid and also in ICE *Kp1* , which is reported in the *rmpA* column as ``rmpA_11(ICEKp1),rmpA_2(KpVP-1)``.
* As with the other virulence genes, truncations in the *rmpA* and *rmpA2* genes are expressed as a percentage of the amino acid length from the start codon, e.g. ``rmpA_5-54%`` indicates the RmpA protein is truncated after 54% length of the intact amino acid sequence. These truncations appear to be common, due to insertions and deletions within a poly-G tract, and almost certainly result in loss of protein function.
