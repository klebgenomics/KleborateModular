########################
Installation
########################

Dependencies
=============
Kleborate requires the following software and libraries to be installed and available in your path:


* `Python <https://www.python.org/>`_ v3.9 or later
* `Biopython <https://biopython.org/>`_ v1.75 or later

  * The ``Bio.pairwise2`` module will be replaced with Bio.Align.PairwiseAligner in the near future

* `Mash <https://github.com/marbl/Mash>`_ v2.0 or later
* `Minimap2 <https://github.com/lh3/minimap2>`_ 
* `DNA Features Viewer <https://edinburgh-genome-foundry.github.io/DnaFeaturesViewer/>`_


Run KleborateModular 
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   conda create -n klebsiella_analysis python=3.9 biopython minimap2 mash -y
   conda activate klebsiella_analysis
   git clone --recursive https://github.com/klebgenomics/KleborateModular.git

   cd KleborateModular
   ./kleborate-runner.py --list_modules
   ./kleborate-runner.py -h

