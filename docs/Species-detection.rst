.. role:: raw-html-m2r(raw)
   :format: html


Kleborate will attempt to identify the species of each input assembly. It does this by comparing the assembly using `Mash <https://mash.readthedocs.io/>`_ to a curated set of *Klebsiella* and other Enterobacteriaceae assemblies from NCBI, and reporting the species of the closest match. Kleborate considers a Mash distance ≤ 0.02 to be a strong species match. A distance of > 0.02 and ≤ 0.04 is a weak match and might indicate that your sample is a novel lineage or a hybrid between multiple *Klebsiella* species.

Here is an annotated tree of the reference assemblies, made by applying the `FastME <https://academic.oup.com/mbe/article/32/10/2798/1212138>`_ algorithm to pairwise Mash distances:

.. figure:: https://github.com/katholt/Kleborate/blob/main/images/species_tree.png
   :align: center
   :width: 90%
   :alt: Klebsiella species tree



*K. pneumoniae* species complex (KpSC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kleborate is designed for detailed genotyping of the well-studied *K. pneumoniae* species complex (KpSC) labelled on the tree, which includes the seven species listed in the table below. These were previously considered as phylogroups within *K. pneumoniae*. We've included the phylogroup numbers in the table below for backwards compatibility with older literature, but these names are not used in the Kleborate output. 

See `this review <https://www.nature.com/articles/s41579-019-0315-1>`_ for an overview of the species complex.

Note that the [[MLST]] scheme applies across the entire species complex.

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

Rhinoscleromatis and Ozaenae
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two clonal lineages of *K. pneumoniae* also have subspecies names, due to their association with specific disease syndromes: *K. pneumoniae* subsp. *rhinoscleromatis* (cause of 'rhinoscleroma', a chronic granulomatous infection of the nose and upper airways of humans, typically K3 capsule carrying *iuc2a* and ICE *Kp* and *K. pneumoniae* subsp. *ozaenae* (cause of atrophic rhinitis or 'ozena', but also found colonising or infecting other sites, typically K5 or K4 capsule carrying *iuc4* and ICE *Kp*. However phylogenetically, these sit squarely within the general population of *K. pneumoniae*\ , and are best thought of as hypervirulent `clonal groups within this species <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2656620/>`_.

Kleborate therefore reports these as *K. pneumoniae* in the species column (on the basis of mash distances to the tree above), but will identify them based on MLST and annotate the subspecies in the 'MLST' column, see `MLST page <https://github.com/katholt/Kleborate/wiki/MLST#rhinoscleromatis-and-ozaenae>`_ for details.

Other *Klebsiella* and Enterobacteriaceae
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

More distant *Klebsiella* species (\ *oxytoca*\ , *michiganensis*\ , *grimontii* and *aerogenes* etc.) will be accurately identified by Kleborate, although please note that the diversity and relevance of *K. pneumoniae* virulence factors in these species is not yet well understood. 

Kleborate will also yield reliable species identifications across the family Enterobacteriaceae, as different species sometimes end up in *Klebsiella* collections. These names are again assigned based on the clades in a Mash-based tree, but were not as carefully curated as the *Klebsiella* species (so take them with a grain of salt).
