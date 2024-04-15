.. role:: raw-html-m2r(raw)
   :format: html


Kleborate is a tool to screen genome assemblies of *Klebsiella pneumoniae*\ , the *Klebsiella pneumoniae* species complex (KpSC), *Klebsiella oxytoca* species complex, and *escherichia coli*

Kleborate screens genome assemblies of *Klebsiella pneumoniae* and the *Klebsiella pneumoniae* species complex (KpSC) for:


* MLST sequence type
* species (e.g. *K. pneumoniae*\ , *K. quasipneumoniae*\ , *K. variicola*\ , etc.)
* *ICE* : *Kp* associated virulence loci: yersiniabactin (*ybt*), colibactin (*clb*), salmochelin (*iro*), hypermucoidy (*rmpA*)
* virulence plasmid associated loci: salmochelin (\ *iro*\ ), aerobactin (\ *iuc*\ ), hypermucoidy (\ *rmpA*\ , *rmpA2*\ )
* antimicrobial resistance determinants: acquired genes, SNPs, gene truncations and intrinsic β-lactamases
* K (capsule) and O antigen (LPS) serotype prediction, via *wzi* alleles and `Kaptive <https://github.com/katholt/Kaptive>`_

For *Klebsiella oxytoca* species complex Kleborate will accurately determine the species and will report:


* MLST sequence type
* *ICE* : *Kp* associated virulence loci: yersiniabactin (*ybt*), colibactin (*clb*), salmochelin (*iro*), hypermucoidy (*rmpA*)
* virulence plasmid associated loci: salmochelin (\ *iro*\ ), aerobactin (\ *iuc*\ ), hypermucoidy (\ *rmpA*\ , *rmpA2*\ )

For *escherichia coli* will determine the species and report MLST sequence type using achtman and pasteur sequence types

Tutorial - Do we create a tutorial adapted to the modular?
----------------------------------------------------------

A step-by-step tutorial is available at `bit.ly/kleborate-workshop <bit.ly/kleborate-workshop>`_\ , covering: 


* Kleborate's features and their scientific rationale
* How to run Kleborate 
* Examples, illustrating how to run and interpret results
* How to visualise results using Kleborate-Viz
* Performance of Kleborate on nanopore data

Citing Kleborate and Kaptive
----------------------------

If you use Kleborate, please cite the paper: `Lam, MMC. et al. A genomic surveillance framework and genotyping tool for Klebsiella pneumoniae and its related species complex. *Nature Communications* (2021). <https://www.nature.com/articles/s41467-021-24448-3>`_

If you turned on Kaptive (\ ``--kaptive``\ ) for K and O locus typing please also cite `Wyres, KL. et al. Identification of *Klebsiella* capsule synthesis loci from whole genome data. *Microbial Genomics* (2016). <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000102>`_

The following papers provide more information on the component schemes and genotyping incorporated in Kleborate:

..
   
   Yersiniabactin and colibactin (ICE*Kp*):
   Lam, MMC. et al. Genetic diversity, mobilisation and spread of the yersiniabactin-encoding mobile element ICE*Kp* in *Klebsiella pneumoniae* populations. *Microbial Genomics* (2018). `Microbial Genomics <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000196>`_

   Aerobactin and salmochelin:
   Lam, MMC. et al. Tracking key virulence loci encoding aerobactin and salmochelin siderophore synthesis in *Klebsiella pneumoniae*. *Genome Medicine* (2018). `Genome Medicine <https://genomemedicine.biomedcentral.com/articles/10.1186/s13073-018-0587-5>`_

   Kaptive for capsule (K) serotyping:
   Wyres, KL. et al. Identification of *Klebsiella* capsule synthesis loci from whole genome data. *Microbial Genomics* (2016). `Microbial Genomics 2 <http://mgen.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000102>`_

   Kaptive for O antigen (LPS) serotyping:
   Wick, RR et. al. Kaptive Web: user-friendly capsule and lipopolysaccharide serotype prediction for *Klebsiella* genomes. *Journal of Clinical Microbiology* (2018). `Journal of Clinical Microbiology <http://jcm.asm.org/content/56/6/e00197-18>`_


Interactive Kleborate reports on public data sets
-------------------------------------------------

The `Kleborate paper <https://www.nature.com/articles/s41467-021-24448-3>`_ reports results of genotyping ~10,000 public genomes that have been filtered to remove redundant sequences (e.g. outbreak clusters, identified as small genome-wide mash distance with same year, location and genotypes). The results can be explored in `Microreact <https://bit.ly/klebMR>`_ (which shows the mash tree, Kleborate output & curated metadata) or `Kleborate-Viz <https://kleborate.erc.monash.edu/>`_ (R shiny app). Kleborate-Viz also has the EuSCAPE dataset preloaded, or you can view your own Kleborate results.

Kleborate is also included in `Klebsiella Pathogenwatch <https://pathogen.watch/>`_ which shows interactive trees, maps and line lists for Klebsiella pneumoniae and allows you to analyse your own data in context of the public collections. See `this preprint <https://www.biorxiv.org/content/10.1101/2021.06.22.448967v2>`_ for an example of how to use it.

Contact us
----------

Kleborate is under active development with many other Klebs genomic analysis tools and projects in progress. 

Please get in touch via the GitHub `issues tracker <https://github.com/katholt/Kleborate/issues>`_ if you have any issues, questions or ideas.

For more on our lab, including other software, see `http://holtlab.net <http://holtlab.net>`_

License
-------

`GNU General Public License, version 3 <https://www.gnu.org/licenses/gpl-3.0.html>`_

----

