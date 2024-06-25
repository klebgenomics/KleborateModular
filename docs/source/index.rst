.. KleborateModular documentation master file, created by
   sphinx-quickstart on Thu Apr 25 06:02:56 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 1
   :hidden:

   Installation
   Usage
   modules
   Creating-New-Modules


########################
Introducing Kleborate v3
########################

Kleborate was primarily developed to screen genome assemblies of *Klebsiella pneumoniae* and the *Klebsiella pneumoniae* species complex (KpSC) for:

* Species (e.g. *K. pneumoniae*\ , *K. quasipneumoniae*\ , *K. variicola*\ , etc.)
* *K. pneumoniae* MLST sequence type
* *ICEKp* associated virulence loci: yersiniabactin (*ybt*), colibactin (*clb*), salmochelin (*iro*), hypermucoidy (*rmpA*)
* Virulence plasmid associated loci: salmochelin (\ *iro*\ ), aerobactin (\ *iuc*\ ), hypermucoidy (\ *rmpA*\ , *rmpA2*\ )
* Antimicrobial resistance determinants: acquired genes, SNPs, gene truncations and intrinsic β-lactamases
* K (capsule) and O antigen (LPS) serotype prediction, via *wzi* alleles and `Kaptive <https://github.com/klebgenomics/Kaptive>`_


`Kleborate v3 <https://github.com/klebgenomics/KleborateModular>`_ includes a rewrite of the code to (i) replace the use of BLAST with minimap (faster and less buggy); and (ii) introduce a modular structure making it easy to add new typing modules, including for other species.


**For** *K. pneumoniae* **species complex, Kleborate v3 can reproduce the outputs of Kleborate v2** by running the preset modules for KpSC via: 

.. code-block:: Python

   kleborate  -a *.fasta -o results.txt -p kpsc

(Note the command has changed from Kleborate v2, the above is equivalent to running ``kleborate --all -o results.txt -a *.fasta``  with Kleborate v2 and includes all resistance and Kaptive-based typing)

**New modules for other species are in development,** for now these include MLST schemes for *Klebsiella oxytoca* species complex and *Escherichia coli* (see the Modules page).

Summary of modules and their output columns
--------------------------------------------

Please refer to the module section for detailed explanations.

.. list-table:: 
   :header-rows: 1
   :widths: 30 70
   :class: colwidths-given

   * - **Module Name**
     - **Columns**
   * - `enterobacterales__species <#enterobacterales_species>`_
     - species, species_match
   * - `general__contig_stats <#general__contig_stats>`_
     - contig_count, N50, largest_contig, total_size, ambiguous_bases, QC_warnings
   * - `klebsiella_pneumo_complex__mlst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__mlst>`_
     - ST, gapA, infB, mdh, pgi, phoE, rpoB, tonB
   * - `klebsiella__ybst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__ybst>`_
     - YbST, Yersiniabactin, ybtS, ybtX, ybtQ, ybtP, ybtA, irp2, irp1, ybtU, ybtT, ybtE, fyuA
   * - `klebsiella__cbst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__cbst>`_
     - CbST, Colibactin, clbA, clbB, clbC, clbD, clbE, clbF, clbG, clbH, clbI, clbL, clbM, clbN, clbO, clbP, clbQ
   * - `klebsiella__abst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__abst>`_
     - AbST, Aerobactin, iucA, iucB, iucC, iucD, iutA
   * - `klebsiella__smst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__smst>`_
     - Salmochelin, SmST, iroB, iroC, iroD, iroN
   * - `klebsiella__rmst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__rmst>`_
     - RmST, RmpADC, rmpA, rmpD, rmpC
   * - `klebsiella__rmpa2 <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella__rmpa2>`_
     - rmpA2
   * - `Virulence score <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__virulence_score>`_
     - virulence_score (Score of 0-5)
   * - `klebsiella_pneumo_complex__amr <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__amr>`_
     - AGly_acquired, Col_acquired, Fcyn_acquired, Flq_acquired, Gly_acquired, MLS_acquired, Phe_acquired, Rif_acquired, Sul_acquired, Tet_acquired, Tgc_acquired, Tmt_acquired, Bla_acquired, Bla_ESBL_acquired, Bla_ESBL_inhR_acquired, Bla_Carb_acquired, Bla_chr, SHV_mutations, Omp_mutations, Col_mutations, Flq_mutations, truncated_resistance_hits, spurious_resistance_hits
   * - `klebsiella_pneumo_complex__resistance_score <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__resistance_score>`_
     - resistance_score (Score of 0-3), num_resistance_genes, num_resistance_classes
   * - `klebsiella_pneumo_complex__wzi <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__wzi>`_
     - wzi allele
   * - `klebsiella_pneumo_complex__kaptive <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_pneumo_complex__kaptive>`_
     - Best match locus, Best match type, Match confidence, Problems, Identity, Coverage, Length discrepancy, Expected genes in locus, details, Missing expected gene
   * - `klebsiella_oxytoca_complex__mlst <https://kleboratemodular.readthedocs.io/en/latest/modules.html#klebsiella_oxytoca_complex__mlst>`_
     - ST, gapA, infB, mdh, pgi, phoE, rpoB, tonB
   * - `escherichia__mlst_pasteur <https://kleboratemodular.readthedocs.io/en/latest/modules.html#escherichia__mlst_pasteur>`_
     - ST, dinB, icdA, pabB, polB, putP, trpA, trpB, uidA
   * - `escherichia__mlst_achtman <https://kleboratemodular.readthedocs.io/en/latest/modules.html#escherichia__mlst_achtman>`_
     - ST, adk, fumC, gyrB, icd, mdh, purA, recA

Citations
----------

If you use Kleborate, please cite the paper: Lam, MMC. et al. A genomic surveillance framework and genotyping tool for *Klebsiella pneumoniae* and its related species complex, *Nature Communications* (2021). `<https://www.nature.com/articles/s41467-021-24448-3>`_


If you use the Kaptive calls for K and O locus typing please also cite Wyres, KL. et al. Identification of *Klebsiella* capsule synthesis loci from whole genome data. *Microbial Genomics* (2016). `<http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000102>`_

The following papers provide more information on the component schemes and genotyping incorporated in Kleborate:

..
   
   Yersiniabactin and colibactin (*ICEKp*):
   Lam, MMC. et al. Genetic diversity, mobilisation and spread of the yersiniabactin-encoding mobile element *ICEKp* in *Klebsiella pneumoniae* populations. *Microbial Genomics* (2018). `Microbial Genomics <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_

   Aerobactin and salmochelin:
   Lam, MMC. et al. Tracking key virulence loci encoding aerobactin and salmochelin siderophore synthesis in *Klebsiella pneumoniae*. *Genome Medicine* (2018). `Genome Medicine <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_

   Kaptive for capsule (K) serotyping:
   Wyres, KL. et al. Identification of *Klebsiella* capsule synthesis loci from whole genome data. *Microbial Genomics* (2016). `Microbial Genomics 2 <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000102>`_

   Kaptive for O antigen (LPS) serotyping:
   Wick, RR et. al. Kaptive Web: user-friendly capsule and lipopolysaccharide serotype prediction for *Klebsiella* genomes. *Journal of Clinical Microbiology* (2018). `Journal of Clinical Microbiology <http://jcm.asm.org/content/56/6/e00197-18>`_


Changes from v2
----------------

When Kleborate v3 is run using the ``-p kpsc`` option to run preset modules for *K. pneumoniae* the same logic is implemented as Kleborate v2, plus the following changes/updates:

* MLST & virulence databases updated (April 2024)
* Column ``Chr_ST``  has been removed in v3, as it is redundant with ``ST`` 
* AMR database updated based on CARD v3.2.9 (June 2024)
* Added ``$`` to indicate when PmrB or MgrB have a mutation in the start codon that may disrupt translation (in ``Col_mutations`` column)
* Added check for synonymous mutation in ompK36 (25 C > T) associated with increased resistance to carbapenems (in ``Omp_mutations`` column)
* Updated to use Kaptive v3, which has some changes to the names of output variables:
  * ``K_locus_missing_genes``  has been renamed ``K_Missing_expected_genes`` 
  * ``O_locus_missing_genes``  has been renamed ``O_Missing_expected_genes`` 
  * New columns are included in Kleborate v3: ``K_Coverage`` , ``O_Coverage``


Tutorial
--------

A step-by-step tutorial for Kleborate v2 is available at `bit.ly/kleborate-workshop <bit.ly/kleborate-workshop>`_\ , covering: 

* Kleborate's features and their scientific rationale
* How to run Kleborate 
* Examples, illustrating how to run and interpret results
* How to visualise results using Kleborate-Viz
* Performance of Kleborate on nanopore data

This tutorial will be updated soon to Kleborate v3, however the functionality of Kleborate v3 remains the same if you add ``-preset kpsc`` to the run command.


Public reports
----------------

The `Kleborate paper <https://www.nature.com/articles/s41467-021-24448-3>`_ reports results of genotyping ~10,000 public genomes that have been filtered to remove redundant sequences (e.g. outbreak clusters, identified as small genome-wide mash distance with same year, location and genotypes), with Kleborate v2. The results can be explored in `Microreact <https://bit.ly/klebMR>`_ (which shows the mash tree, Kleborate output & curated metadata) or `Kleborate-Viz <https://kleborate.erc.monash.edu/>`_ (R shiny app). Kleborate-Viz also has the EuSCAPE dataset preloaded, or you can view your own Kleborate results.

Kleborate is also included in `Klebsiella Pathogenwatch <https://pathogen.watch/>`_ which shows interactive trees, maps and line lists for *Klebsiella pneumoniae* and allows you to analyse your own data in context of the public collections. See `this paper <https://doi.org/10.1093/cid/ciab784>`_ for an example of how to use it.

Contact us
----------

Kleborate is under active development with many other Klebs genomic analysis tools and projects in progress (see `github.com/klebgenomics <https://github.com/klebgenomics>`_). 

Please get in touch via the GitHub `issues tracker <https://github.com/klebgenomics/KleborateModular/issues>`_ if you have any issues, questions or ideas.

For more on our lab, including other software, see `http://holtlab.net <http://holtlab.net>`_

License
-------

`GNU General Public License, version 3 <https://www.gnu.org/licenses/gpl-3.0.html>`_



