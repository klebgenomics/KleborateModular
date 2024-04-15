.. role:: raw-html-m2r(raw)
   :format: html


KleborateModular outputs a simple categorical virulence score, and antimicrobial resistance score. These scores provide a rough categorisation of the strains to facilitate monitoring resistance-virulence convergence.

Virulence score
^^^^^^^^^^^^^^^


* The virulence score ranges from 0 to 5:

  * 0 = negative for all of yersiniabactin (\ *ybt*\ ), colibactin (\ *clb*\ ), aerobactin (\ *iuc*\ )
  * 1 = yersiniabactin only
  * 2 = yersiniabactin and colibactin (or colibactin only)
  * 3 = aerobactin (without yersiniabactin or colibactin)
  * 4 = aerobactin with yersiniabactin (without colibactin)
  * 5 = yersiniabactin, colibactin and aerobactin

Note neither the salmochelin (\ *iro*\ ) locus nor *rmpADC* are explicitly considered in the virulence score, for simplicity. The *iro* and *rmpADC* loci typically appear alongside the aerobactin (\ *iuc*\ ) locus on the *Kp* virulence plasmids, and so presence of *iuc* (score of 3-5) generally implies presence of *iro* and *rmpADC*. However we prioritise *iuc* in the calculation of the score, as aerobactin is specifically associated with growth in blood and is a stronger predictor of the hypervirulence phenotype (see `this review <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6349525/>`_\ ). The *iro* and *rmpADC* loci are also occasionally present with *ybt*\ , in the ICE *Kp* variant - ICE *Kp1*, but this will still score 1.


Resistance score
^^^^^^^^^^^^^^^^


* The resistance score ranges from 0 to 3:

  * 0 = no ESBL, no carbapenemase (regardless of colistin resistance)
  * 1 = ESBL, no carbapenemase (regardless of colistin resistance)
  * 2 = Carbapenemase without colistin resistance (regardless of ESBL genes or OmpK mutations)
  * 3 = Carbapenemase with colistin resistance (regardless of ESBL genes or OmpK mutations)

Resistance gene counts and drug class counts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

KleborateModular quantifies how many acquired resistance genes are present and how many drug classes (in *addition* to the intrinsic Bla / ampicillin phenotype) have at least one resistance determinant detected. A few things to note:


* The presence of resistance *mutations*\ , and non-ESBL forms of core genes SHV/LEN/OKP, do not contribute to the resistance *gene* count.
* Mutations do contribute to the drug class count, e.g. fluoroquinolone resistance will be counted if a GyrA mutation is encountered regardless of whether or not an acquired quinolone resistance (\ *qnr*\ ) gene is also present. The exceptions are Omp mutations, which do not contribute to the drug class count as their effect depends on the strain background and the presence of acquired beta-lactamase enzymes; hence this information is provided in a separate column, and interpretation is left to the user (see the `Antimicrobial Resistance <https://github.com/katholt/Kleborate/wiki/Antimicrobial-resistance>`_ page).
* Genes reported in the ``truncated_resistance_genes`` and ``spurious_resistance_genes`` columns do not contribute to the counts.
* Note that since a drug class can have multiple resistance determinants, the gene count is typically higher than the class count.
