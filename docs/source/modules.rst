**************************************
Modules
**************************************


Kleborate v3 includes a range of modules for typing bacterial genomes, most of which are specific to a particular species or complex (*Klebsiella pneumoniae SC*, *Klebsiella oxytoca SC*, *Escherichia coli*). We therefore recommend specifying ``-p`` (*kpsc*, *kosc*, *escherichia*) or ``-m`` (list of modules to run based on the organism). This will run the species detection module first, and if the species matches that specified in --preset, the preset modules for that species will be run (if not, the species will be reported and the remaining fields will be blank). 


Summary of availabe modules and their output columns
----------------------------------------------------

.. list-table:: 
   :header-rows: 1
   :widths: 30 70
   :class: colwidths-given

   * - **Module Name**
     - **Columns**
   * - :ref:`enterobacterales__species <species_detection>`
     - species, species_match
   * - :ref:`general__contig_stats <contig_stats>`
     - contig_count, N50, largest_contig, total_size, ambiguous_bases, QC_warnings
   * - klebsiella_pneumo_complex__mlst 
     - ST, gapA, infB, mdh, pgi, phoE, rpoB, tonB
   * - klebsiella__ybst 
     - YbST, Yersiniabactin, ybtS, ybtX, ybtQ, ybtP, ybtA, irp2, irp1, ybtU, ybtT, ybtE, fyuA
   * - klebsiella__cbst 
     - CbST, Colibactin, clbA, clbB, clbC, clbD, clbE, clbF, clbG, clbH, clbI, clbL, clbM, clbN, clbO, clbP, clbQ
   * - klebsiella__abst 
     - AbST, Aerobactin, iucA, iucB, iucC, iucD, iutA
   * - klebsiella__smst 
     - Salmochelin, SmST, iroB, iroC, iroD, iroN
   * - klebsiella__rmst 
     - RmST, RmpADC, rmpA, rmpD, rmpC
   * - klebsiella__rmpa2 
     - rmpA2
   * - klebsiella_pneumo_complex__virulence_score 
     - virulence_score (Score of 0-5)
   * - klebsiella_pneumo_complex__amr 
     - AGly_acquired, Col_acquired, Fcyn_acquired, Flq_acquired, Gly_acquired, MLS_acquired, Phe_acquired, Rif_acquired, Sul_acquired, Tet_acquired, Tgc_acquired, Tmt_acquired, Bla_acquired, Bla_ESBL_acquired, Bla_ESBL_inhR_acquired, Bla_Carb_acquired, Bla_chr, SHV_mutations, Omp_mutations, Col_mutations, Flq_mutations, truncated_resistance_hits, spurious_resistance_hits
   * - klebsiella_pneumo_complex__resistance_score 
     - resistance_score (Score of 0-3)
   * - klebsiella_pneumo_complex__resistance_gene_count 
     - num_resistance_genes
   * - klebsiella_pneumo_complex__resistance_class_count
     - num_resistance_classes
   * - klebsiella_pneumo_complex__wzi 
     - wzi allele
   * - klebsiella_pneumo_complex__kaptive 
     - Best match locus, Best match type, Match confidence, Problems, Identity, Coverage, Length discrepancy, Expected genes in locus, details, Missing expected gene
   * - klebsiella_oxytoca_complex__mlst 
     - ST, gapA, infB, mdh, pgi, phoE, rpoB, tonB
   * - escherichia__mlst_pasteur 
     - ST, dinB, icdA, pabB, polB, putP, trpA, trpB, uidA
   * - escherichia__mlst_achtman 
     - ST, adk, fumC, gyrB, icd, mdh, purA, recA

**Kleborate modules are divided into:**

1. General Modules
2. Modules for *Klebsiella pneumoniae* species complex
3. Modules for *Klebsiella oxytoca* species complex
4. Modules for *Escherichia* species complex

Details of how the modules work, and how to interpret the outputs, are given below.

General modules
===============

.. _species_detection:

Species detection
-----------------

``-m enterobacterales__species``


This module will attempt to identify the species of each input assembly. It does this by comparing the assembly using `Mash <https://mash.readthedocs.io/>`_ to a curated set of *Klebsiella* and other *Enterobacteriaceae* assemblies from NCBI, and reporting the species of the closest match. 

Parameters
++++++++++++++++++

``--enterobacterales__species_strong``

Mash distance threshold for a strong species match (default: 0.02)

``--enterobacterales__species_weak``

Mash distance threshold for a weak species match (default: 0.04)

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

.. _contig_stats:

.. code-block:: Python

   -m general__contig_stats

This module takes ``enterobacterales__species`` as a prerequisite and  generates some basic assembly statistics to help users understand their typing results in the context of assembly quality, although we recommend users conduct more comprehensive QC themselves before typing genomes (e.g. screen for contamination, etc).

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
