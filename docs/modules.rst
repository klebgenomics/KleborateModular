
KleborateModular includes a range of modules for typing bacterial genomes, most of which are specific to a particular species or complex (Klebsiella pneumoniae SC, Klebsiella oxytoca SC, Escherichia coli). We therefore recommend specifying a preset list of modules to run based on the organism, rather than specifying individual modules. This will run the species detection module first, and if the species matches that specified in --preset, the preset modules for that species will be run (if not, the species will be reported and the remaining fields will be blank). 

Details of the available modules, how they work, and how to interpret the outputs, are given below.

General modules
===============

Species detection
-----------------

.. code-block:: Python

   -m enterobacterales__species


This module will attempt to identify the species of each input assembly. It does this by comparing the assembly using `Mash <https://mash.readthedocs.io/>`_ to a curated set of *Klebsiella* and other Enterobacteriaceae assemblies from NCBI, and reporting the species of the closest match. 

Outputs
+++++++

Output of the species typing module is the following columns:

.. list-table::

   * - species
     - Species name (scientific name)

   * - species_match
     - Strength of the species call indicated as ``strong``\  (Mash distance ≤ 0.02) or ``weak``\  (Mash distance of > 0.02 and ≤ 0.04, may be novel or hybrid species)

The quality and completeness of Kleborate results depends on the quality of the input genome assemblies. In general, you can expect good results from draft genomes assembled with tools like SPAdes from high-depth (>50x) Illumina data, however it is always possible that key genes subject to genotyping may be split across contigs, which can create problems for detecting and typing them accurately.

Contig stats
------------

.. code-block:: Python

   -m general__contig_stats

This module generates some basic assembly statistics to help users understand their typing results in the context of assembly quality, although we recommend users conduct more comprehensive QC themselves before typing genomes (e.g. screen for contamination, etc).

The module reports a standard set of assembly quality metrics (see Outputs below).

It will also flag in the ``QC_warnings``\  column if an assembly size falls outside those specified in the ``species_specification.txt``\  in the module directory, or if N50 <10 kbp or ambiguous bases (Ns) are detected in the sequence.

Outputs
+++++++

Output of the contig stats module is the following columns:

.. list-table::

   * - contig_count
     - Number of contigs in the input assembly

   * - N50
     - `N50 <https://en.wikipedia.org/wiki/N50,_L50,_and_related_statistics>`_ calculated from the contig sizes

   * - largest_contig
     - Size of largest contig (in bp)

   * - total_size
     - Total assembly size (in bp)

   * - ambiguous_bases
     - Detection of ambiguous bases (yes or no). If yes, the number of ambiguous bases is also provided in brackets.

   * - QC_warnings
     - List of QC issues detected, including: ``ambiguous_bases``\ (ambiguous bases detected) ``N50``\ (N50 < 10 kbp), ``total_size`` (genome size falls outside expected range).

Klebsiella pneumoniae species complex
=====================================

.. code-block:: Python

   --preset kpsc

These modules will be run if the ``enterobacterales__species``\   module confirms the input assembly as a member of the *K. pneumoniae* species complex (KpSC) labelled in the tree below. 

We've included the phylogroup numbers in the table below for backwards compatibility with older literature, but these names are not used in the Kleborate output. See `this review <https://www.nature.com/articles/s41579-019-0315-1>`_ for an overview of the species complex. 


.. figure:: https://github.com/katholt/Kleborate/blob/main/images/species_tree.png
   :align: center
   :width: 90%
   :alt: Klebsiella species tree

.. list-table::
   :header-rows: 1

   * - Species
     - Kp phylogroup\ :sup:`a`
     - Kp phylogroup (alternative)\ :sup:`b`
     - Reference
   * - *K. pneumoniae*
     - Kp1
     - KpI
     - `Brenner, D.J. 1979 Int J Syst Evol Microbiol 29: 38-41 <https://ijs.microbiologyresearch.org/content/journal/ijsem/10.1099/00207713-29-1-38>`_
   * - *K. quasipneumoniae* subsp *quasipneumoniae*
     - Kp2
     - KpIIa
     - `Brisse et al. 2014 Int J Syst Evol Microbiol 64:3146-52 <https://ijs.microbiologyresearch.org/content/journal/ijsem/10.1099/ijs.0.062737-0#tab2>`_
   * - *K. quasipneumoniae* subsp *similipneumoniae*
     - Kp4
     - KpIIb
     - `Brisse et al. 2014 Int J Syst Evol Microbiol 64:3146-52 <https://ijs.microbiologyresearch.org/content/journal/ijsem/10.1099/ijs.0.062737-0#tab2>`_
   * - *K. variicola* subsp *variicola*
     - Kp3
     - KpIII
     - `Rosenblueth et al. 2004 Syst Appl Microbiol 27:27-35 <https://www.sciencedirect.com/science/article/abs/pii/S0723202004702349?via%3Dihub>`_
   * - *K. variicola* subsp *tropica*
     - Kp5
     - -
     - `Rodrigues et al. 2019 Res Microbiol ﻿S0923-2508:﻿30019-1 <https://www.sciencedirect.com/science/article/pii/S0923250819300191?via%3Dihub>`_ (described as subsp *tropicalensis* in this paper)
   * - *K. quasivariicola*
     - Kp6
     - -
     - `Long et al. 2017 Genome Announc 5: ﻿e01057-17 <https://mra.asm.org/content/5/42/e01057-17>`_
   * - *K. africana*
     - Kp7
     - -
     - `Rodrigues et al. 2019 Res Microbiol ﻿S0923-2508:﻿30019-1 <https://www.sciencedirect.com/science/article/pii/S0923250819300191?via%3Dihub>`_ (described as *africanensis* in this paper)


:sup:`a` Kp Kp phylogroup numbers as described in `Rodrigues et al. 2019 <https://www.sciencedirect.com/science/article/pii/S0923250819300191?via%3Dihub>`_

:sup:`b` alternative (older) Kp phylogroup numbers as described in `Brisse et al. 2001 <https://ijs.microbiologyresearch.org/content/journal/ijsem/10.1099/00207713-51-3-915#tab2>`_ and `Fevre et al. 2005 <https://aac.asm.org/content/49/12/5149>`_ prior to the identification of *K. variicola* subsp *tropica*\ , *K. quasivariicola* and *K. africana*.


KpSC MLST
---------

.. code-block:: Python

   -m klebsiella_pneumo_complex__mlst

Genomes identified by Kleborate as belonging to the *K. pneumoniae* species complex are subjected to MLST using the 7-locus scheme described at the  *K. pneumoniae* `\BIGSdb hosted at the Pasteur Institute <http://bigsdb.pasteur.fr/klebsiella/klebsiella.html>`_. Note that this scheme is not specific to *K. pneumoniae sensu stricto* but covers the whole species complex. 

A copy of the MLST alleles and ST definitions is stored in the /data directory of this module.

Rhinoscleromatis and Ozaenae
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *K. pneumoniae* clonal group CG67 is known as *K. pneumoniae* subsp. *rhinoscleromatis* because it causes rhinoscleroma (chronic granulomatous infection of the nose and upper airways), and clonal group CG91 is known as *K. pneumoniae* subsp. *ozaenae* as it can cause ozena (atrophic rhinitis). To alert users to this, when STs belonging to these clonal groups are detected by Kleborate this is flagged in the ST column, e.g. 'ST67 (subsp. rhinoscleromatis)' or 'ST97 (subsp. ozaenae)'. 

The relevant STs are:

.. list-table::

   * - **Species column**
     - **ST**
     - **MLST column**
   * - *K. pneumoniae*
     - 67, 68, 69, 3772, 3819
     - ST67 (subsp. rhinoscleromatis)
   * - *K. pneumoniae*
     - 90, 91, 92, 93, 95, 96, 97, 381, 777, 3193
       3766, 3768, 3771, 3781, 3782, 3784, 3802, 3803
     - ST91 (subsp. ozaenae)


Outputs
+++++++

Output of the KpSC module is the following columns:

.. list-table::

   * - ST
     - sequence type

   * - gapA, infB, mdh, pgi, phoE, rpoB, tonB
     - allele number

* Kleborate makes an effort to report the closest matching ST if a precise match is not found.
* Imprecise allele matches are indicated with a ``*``.
* Imprecise ST calls are indicated with ``-nLV``\ , where n indicates the number of loci that disagree with the ST reported. So ``258-1LV`` indicates a single-locus variant (SLV) of ST258, i.e. 6/7 loci match ST258.


KpSC virulence modules
----------------------

Typing modules are available five key acquired virulence loci that are associated with invasive infections and are found at high prevalence among hypervirulent *K. pneumoniae* strains: the siderophores yersiniabactin (\ *ybt*\ ), aerobactin (\ *iuc*\ ) and salmochelin (\ *iro*\ ), the genotoxin colibactin (\ *clb*\ ), and the hypermucoidy locus *rmpADC*. Each of these loci comprises multiple genes and will only be reported if >50% of the genes are detected. 

There is also a module to screen for the alternative hypermucoidy marker gene *rmpA2*.

For each module, if the target locus is detected, the typer will:

* Call a sequence type using the same logic as for 7-gene MLST
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

Yersiniabactin and colibactin
+++++++++++++++++++++++++++++

.. code-block:: Python

   -m klebsiella_pneumo_complex__ybst, klebsiella_pneumo_complex__cbst

We previously explored the diversity of the *K. pneumoniae* integrative conjugative element (ICE *Kp*), which mobilises the yersiniabactin locus *ybt*, using genomic analysis of a diverse set of 2498 *Klebsiella* (see `this paper <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_\ ). Overall, we found *ybt* in about a third of all *K. pneumoniae* genomes (and *clb* in about 14%). We identified 17 distinct lineages of *ybt* (see figure) embedded within 14 structural variants of ICE *Kp* that can integrate at any of four tRNA-Asn sites in the chromosome. One type was found to be plasmid-borne. Based on this analysis, we developed a MLST-style approach for assigning yersiniabactin sequence types (YbST) and colibactin sequence types (CbST), which is implemented in KleborateModular. 

Note that while ICE *Kp1* is occasionally found in other species within the KpSC, and even in other genera of Enterobacteriaceae (see `original paper <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_\ ), most of the known variation included in the database is derived from *K. pneumoniae*.

The allele databases and schemes were last updated in April 2024. 

Outputs
+++++++

Output of the ybst module is the following columns:

.. list-table::

   * - Yersiniabactin
     - Lineage (ICEKp prediction)

   * - YbST
     - Yersiniabactin sequence type

   * - ybtS, ybtX, ybtQ, ybtP, ybtA, irp2, irp1, ybtU, ybtT, ybtE, fyuA
     - allele number (ybt locus)

Output of the cbst module is the following columns:

.. list-table::

   * - Colibactin
     - Lineage

   * - CbST
     - Colibactin sequence type

   * - clbA, clbB, clbC, clbD, clbE, clbF, clbG, clbH, clbI, clbL, clbM, clbN, clbO, clbP, clbQ
     - allele number (clb / pks locus)

Aerobactin and salmochelin
--------------------------

.. code-block:: Python

   -m klebsiella_pneumo_complex__abst, klebsiella_pneumo_complex__smst

We further explored the genetic diversity of the aerobactin (\ *iuc*\ ) and salmochelin (\ *iro*\ ) loci among a dataset of 2733 *Klebsiella* genomes (see `this paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_\ ). We identified five *iro* and six *iuc* lineages (see figure), each of which was associated with a specific location within *K. pneumoniae* genomes (primarily virulence plasmids). Based on this analysis, we developed a MLST-style approach for assigning aerobactin sequence types (AbST) and salmochelin sequence types (SmST) which is implemented in Kleborate. 

* The most common lineages are *iuc1* and *iro1*\ , which are found together on the FIBk virulence plasmid KpVP-1 (typified by pK2044 or pLVPK common to the hypervirulent clones ST23, ST86, etc). 
* *iuc2* and *iro2* lineages were associated with the alternative FIBk virulence plasmid KpVP-2 (typified by Kp52.145 plasmid II from the K2 ST66 lab strain known as Kp52.145 or CIP 52.145 or B5055). 
* *iuc5* and *iro5* originate from *E. coli* and are carried (often together) on *E. coli* FII plasmids that can transfer to *K. pneumoniae*. 
* The lineages *iuc2A*\ , *iuc3* and *iro4* were associated with other novel FIBk plasmids that had not been previously described in *K. pneumoniae*\ , but sequences for which are included in `the paper <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_. 
* The salmochelin locus present in ICE *Kp1* constitutes its own lineage *iro3*\ , and the aerobactin locus present in the chromosome of ST67 *K. pneumoniae* subsp *rhinoscleromatis* strains constitutes its own lineage *iuc4*. 

Note on *iucA* sequence update:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Kleborate version 2.2.0 and earlier, the majority of *iucA* alleles had a sequence length of 1791 bp, with the exception being those associated with lineage *iuc 5* which have a length of 1725 bp. Related to this, *iucA* in genomes with *iuc 3* encoded a premature stop codon resulting in a significantly truncated and presumably non-functional IucA protein (i.e. at 2% length of the intact amino acid sequence), despite experimental evidence showing siderophore activity in *iuc 3*\ + isolates. In light of this evidence, the sequences of *iucA* genes with the longer ~1791 bp length were updated to ~1725 bp by removing the first 66 bp. These changes are captured in Kleborate version 2.3.0 onwards, and address the truncation issue in *iuc 3*\ + genomes. The following *iucA* alleles and AbST profiles have also been retired due to sequence redundancy following the update:

* alleles: _iucA\ *48*\ , _iucA\ *49*\ , _iucA\ *52*
* profiles: AbST 70, 82, 83

The allele databases and schemes were last updated in April 2024. 

Outputs
+++++++

Output of the abst module is the following columns:

.. list-table::

   * - Aerobactin
     - Lineage (plasmid prediction)

   * - AbST
     - Sequence type

   * - iucA, iucB, iucC, iucD, iutA
     - allele number (iuc locus)

Output of the smst module is the following columns:

.. list-table::

   * - Salmochelin
     - Lineage (plasmid prediction)

   * - SmST
     - Sequence type

   * - iroB, iroC, iroD, iroN
     - allele number (iro locus)


Hypermucoidy loci
------------------

.. code-block:: Python

   -m klebsiella__rmst

The *rmpA* locus is associated with the hypermucoidy phenotype that is a virulence feature that is often observed in hypervirulent *K. pneumoniae* strains. Recent work has revealed that *rmpA* serves as a transcriptional regulator for the *rmpD* and *rmpC* genes, and together these genes comprise the *rmpADC* (or *rmp*\ ) locus. *rmpC* is involved in the upregulation of capsule expression while *rmpD* drives hypermucoviscosity (see this paper on `rmpC <https://mbio.asm.org/content/10/2/e00089-19>`_ and this one on `rmpD <https://mbio.asm.org/content/11/5/e01750-20>`_ for more information.) 

In light of this information, we screened and extracted the *rmpA*\ , *rmpD* and *rmpC* sequences from the 2733 genomes included in the aerobactin and salmochelin study, and generated a RmST typing scheme. We observed four distinct *rmp* lineages, which were associated with the KpVP-1 (\ *rmp 1*\ ), KpVP-2 (\ *rmp 2*\ ), *iuc2A* virulence plasmids (\ *rmp 2A*\ ) and ICE *Kp1* (rmp 3). The details of this novel virulence typing scheme have not yet been published. 

The rmpA module screens for *rmpADC* and will report a sequence type, along with the associated lineage and mobile genetic element

Note:
~~~~~

* Alleles for each gene are sourced from the `BIGSdb <http://bigsdb.pasteur.fr/klebsiella/klebsiella.html>`_\ , while additional *rmpA* alleles have also been added to Kleborate.
* The *rmpA* and *rmpA2* genes share ~83% nucleotide identity so are easily distinguished.
* Unique (non-overlapping) nucleotide Minimap2 hits with >95% identity and >50% coverage are reported. Note multiple hits to the same gene are reported if found. E.g. the NTUH-K2044 genome carries *rmpA* in the virulence plasmid and also in ICE *Kp1* , which is reported in the *rmpA* column as ``rmpA_11(ICEKp1),rmpA_2(KpVP-1)``.
* As with the other virulence genes, truncations in the *rmpA* and *rmpA2* genes are expressed as a percentage of the amino acid length from the start codon, e.g. ``rmpA_5-54%`` indicates the RmpA protein is truncated after 54% length of the intact amino acid sequence. These truncations appear to be common, due to insertions and deletions within a poly-G tract, and almost certainly result in loss of protein function.

Outputs
+++++++

Output of the rmst module is the following columns:

.. list-table::

   * - RmpADC
     - Lineage

   * - RmST
     - Sequence type

   * - rmpA, rmpD, rmpC
     - allele number (rmp locus)
