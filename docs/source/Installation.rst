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
* `Kaptive <https://github.com/klebgenomics/Kaptive>`_ 
* `DNA Features Viewer <https://edinburgh-genome-foundry.github.io/DnaFeaturesViewer/>`_


Install Kleborate 
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a conda environment::

   conda create -n klebsiella_analysis python=3.9 minimap2 mash -y
   conda activate klebsiella_analysis

Install from PyPI::

   pip install kleborate
