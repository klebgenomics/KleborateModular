
########################
Usage
########################

Input files
-----------

Genome assemblies in FASTA format (can be gzipped). 

Can be either draft or completed assemblies, though completed is better because it reduces the risk of fragmented genes/loci.

Basic usage
-----------

Run with preset modules for *K. pneumoniae* species complex (KpSC):

.. code-block:: Python

   ./kleborate-runner.py -a *.fasta -o results.txt -p kpsc

Run with specified modules only:

.. code-block:: Python

   ./kleborate-runner.py -a *.fasta -o results.txt -m 

Run with preset modules for *E. coli* or other *Escherichia*, on gzipped assemblies:

.. code-block:: Python

   ./kleborate-runner.py  -a *.fasta.gz -o results.txt -p escherichia

Check available modules, check version, print help:

.. code-block:: Python

   ./kleborate-runner.py [--list_modules] [--version] [-h]


Parameters
----------

Input/output:
  -a ASSEMBLIES [ASSEMBLIES ...], --assemblies ASSEMBLIES [ASSEMBLIES ...]
                                        FASTA file(s) for assemblies

  -o OUTFILE, --outfile OUTFILE         
                                        File for detailed output (default: Kleborate_results.txt)

Modules:
  --list_modules         
                                        Print a list of all available modules and then quit (default: False)

  -p PRESET, --preset PRESET         
                                        Module presets, choose from 

                                        - kpsc (*Klebsiella pnuemoniae* species complex)
                                        - kosc (*Klebsiella oxytoca* species complex)
                                        - escherichia  (*Escherichia*)


  -m MODULES, --modules MODULES         
                                        Comma-delimited list of Kleborate modules to use


Help:
     -h, --help         
                                        Show a help message and exit
     --help_all         
                                        Show a help message with all module options
     --version         
                                        Show program's version number and exit


**Module-specific parameters:** See Modules documentation
