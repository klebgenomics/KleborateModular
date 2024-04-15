.. role:: raw-html-m2r(raw)
   :format: html


Multi-locus sequence typing (MLST)
----------------------------------

Genomes identified by Kleborate as belonging to the *K. pneumoniae* species complex are subjected to MLST using the 7-locus scheme described at the  *K. pneumoniae* `\BIGSdb hosted at the Pasteur Institute <http://bigsdb.pasteur.fr/klebsiella/klebsiella.html>`_. Note that this scheme is not specific to *K. pneumoniae sensu stricto* but covers the whole  `\K. pneumoniae species complex <https://github.com/katholt/Kleborate/wiki/Species-detection#k-pneumoniae-species-complex-kpsc>`_. 

A copy of the MLST alleles and ST definitions is stored in the `data directory <https://github.com/katholt/Kleborate/tree/master/kleborate/data>`_ of this repository. See `here <https://github.com/katholt/Kleborate/wiki/Installation#updating-the-mlst-database>`_ for instructions on how to update the MLST database in your copy of Kleborate.

Notes on Kleborate's MLST calls:


* Kleborate makes an effort to report the closest matching ST if a precise match is not found.
* Imprecise allele matches are indicated with a ``*``.
* Imprecise ST calls are indicated with ``-nLV``\ , where n indicates the number of loci that disagree with the ST reported. So ``258-1LV`` indicates a single-locus variant (SLV) of ST258, i.e. 6/7 loci match ST258.

Rhinoscleromatis and Ozaenae
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *K. pneumoniae* clonal group CG67 is known as *K. pneumoniae* subsp. *rhinoscleromatis* because it causes rhinoscleroma (chronic granulomatous infection of the nose and upper airways), and clonal group CG91 is known as *K. pneumoniae* subsp. *ozaenae* as it can cause ozena (atrophic rhinitis). To alert users to this, when STs belonging to these clonal groups are detected by Kleborate this is flagged in the ST column, e.g. 'ST67 (subsp. rhinoscleromatis)' or 'ST97 (subsp. ozaenae)'. The relevant STs are:

.. list-table::
   :header-rows: 1

   * - ST
     - Species column
     - MLST column (e.g.)
   * - 67, 68, 69, 3772, 3819
     - *K. pneumoniae*
     - ST67 (subsp. rhinoscleromatis)
   * - 90, 91, 92, 93, 95, 96, 97, 381, 777, 3193
       3766, 3768, 3771, 3781, 3782, 3784, 3802, 3803
     - *K. pneumoniae*
     - ST91 (subsp. ozaenae)


Changes to ST definitions
~~~~~~~~~~~~~~~~~~~~~~~~~

*Note that allele definitions for ST1047 and ST1078 were changed in the MLST database in February 2018, and these new allele combinations are incorporated in Kleborate since v0.4.0. This is highly unusual and other allele and ST assignment should be stable across versions.*

.. list-table::
   :header-rows: 1

   * - allele
     - ST1047 old
     - ST1047 current
     - ST1078 old
     - ST1078 current
   * - *gapA*
     - 10
     - 2
     - 16
     - 4
   * - *infB*
     - 20
     - 1
     - 18
     - 5
   * - *mdh*
     - 1
     - 2
     - 1
     - 1
   * - *pgi*
     - 1
     - 20
     - 76
     - 3
   * - *phoE*
     - 9
     - 7
     - 47
     - 12
   * - *rpoB*
     - 11
     - 1
     - 1
     - 4
   * - *tonB*
     - 14
     - 4
     - 124
     - 46

