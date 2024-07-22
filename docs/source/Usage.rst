
########################
Usage
########################

Input files
-----------

Genome assemblies in FASTA format (can be gzipped). 

Can be either draft or completed assemblies, though completed is better because it reduces the risk of fragmented genes/loci.

**The Kleborate output results are split based on the species KpSC, Kosc, *Escherichia* **

Basic usage
-----------

Run with preset modules for *K. pneumoniae* species complex (KpSC):

.. code-block:: Python

   kleborate -a *.fasta -o kleborate_results -p kpsc

- ``-a *.fasta``: Specifies the input files (assemblies) to be analyzed.
- ``-o``: Specifies the directory where the output files will be saved.


The output headers consist of the module names. Users can provide the --trim_headers argument to trim off the module names, making the headers easier to read.

.. code-block:: bash

    kleborate -a *.fasta -o kleborate_results -p kpsc --trim_headers

**Alternatively, users can trim the headers using this script:**
`trim_headers.py <https://github.com/klebgenomics/KleborateModular/blob/main/kleborate/shared/trim_headers.py>`_


Run with specified modules only:

.. code-block:: Python

   kleborate -a *.fasta -o kleborate_results -m 

If the -m argument is used, the output file is suffixed with the module name.


Run with preset modules for *E. coli* or other *Escherichia*, on gzipped assemblies:

.. code-block:: Python

   kleborate  -a *.fasta.gz -o kleborate_results -p escherichia

Check available modules, check version, print help:

.. code-block:: Python

   kleborate [--list_modules] [--version] [-h]


Parameters
----------

**Input/output:**

``-a ASSEMBLIES [ASSEMBLIES ...], --assemblies ASSEMBLIES [ASSEMBLIES ...]``

FASTA file(s) for assemblies

``-o OUTDIR, --outfile --outdir OUTDIR ``

File for detailed output (default: Kleborate_results)

`` --trim_headers Trim headers in the output files ``

**Modules:**

``--list_modules``         

Print a list of all available modules and then quit (default: False)

``-p PRESET, --preset PRESET``         

Module presets, choose from:

.. list-table::

   * - kpsc
     - *Klebsiella pnuemoniae* species complex

   * - kosc
     - *Klebsiella oxytoca* species complex
                                        
   * - escherichia 
     - *Escherichia* genus


``-m MODULES, --modules MODULES``         

Comma-delimited list of Kleborate modules to use


**Help:**
     
``-h, --help``       

Show a help message and exit

``--help_all``         

Show a help message with all module options

``--version``         

Show program's version number and exit


**Module-specific parameters:** 

See Modules documentation

