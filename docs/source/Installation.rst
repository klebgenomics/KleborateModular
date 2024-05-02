########################
Installation
########################

Software requirements
---------------------

Make sure you have these installed first:


* `Python <https://www.python.org/>`_ v3.9 or later
* `Biopython <https://biopython.org/>`_ v1.75 or later

  * The ``Bio.pairwise2`` module will be replaced with Bio.Align.PairwiseAligner in the near future

* `Mash <https://github.com/marbl/Mash>`_ v2.0 or later
* `Minimap2 <https://github.com/lh3/minimap2>`_ 

To verify that you're ready to go, try running these commands from a terminal:

.. code-block:: bash

   python3 --version
   python3 -c "import Bio; print(Bio.__version__)"
   minimap2 -version
   mash --version

Each of these should print a version number message. If not, troubleshoot that tool's installation before continuing!

Run KleborateModular directly from its source directory

.. code-block:: bash

   conda create -n klebsiella_analysis python=3.9 biopython minimap2  mash -y
   conda activate klebsiella_analysis
   git clone --recursive https://github.com/klebgenomics/KleborateModular.git
   cd KleborateModular
   usage: ./kleborate-runner.py [-a ASSEMBLIES [ASSEMBLIES ...]] [-o OUTFILE] [--list_modules] [-p PRESET] [-m MODULES] [-h] [--help_all] [--version]

The ``/kleborate``  directory contains:


* ``/modules``  directory - available modules
* ``/shared``  directory - scripts shared by different modules

List modules

.. code-block:: bash

   ./kleborate-runner.py --list_modules
