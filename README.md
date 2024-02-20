<p align="center"><picture><source srcset="images/logo-dark.png" media="(prefers-color-scheme: dark)"><img src="images/logo.png" alt="Kleborate logo" width="400"></picture></p>

This repo contains an experimental rewrite of [Kleborate](https://github.com/klebgenomics/kleborate). It aims to:
* Modularise the code for easier extensibility and maintenance
* Provide functionality for other species, e.g. _Klebsiella oxytoca_ and _Escherichia coli_
* Replace the BLAST dependency with [minimap2](https://lh3.github.io/minimap2/minimap2.html)

This version of Kleborate is **not yet complete**, so most users will probably want the [main Kleborate repo](https://github.com/klebgenomics/kleborate) instead.


## How to use KleborateModular
## Software requirements
Before using KleborateModular, make sure you have these installed:

* [Python](https://www.python.org/) v3.9 or later
* [Biopython](https://biopython.org/) v1.75 or later
	*  The `Bio.pairwise2` module will be replaced with Bio.Align.PairwiseAligner in the near future
* [Mash](https://github.com/marbl/Mash) v2.0 or later
* [Minimap2](https://github.com/lh3/minimap2) 

To verify that you're ready to go, try running these commands from a terminal:
```bash
python3 --version
python3 -c "import Bio; print(Bio.__version__)"
minimap2 -version
mash --version
```

Each of these should print a version number message. If not, troubleshoot that tool's installation before continuing!


Run KleborateModular directly from its source directory

```bash
conda create -n klebsiella_analysis python=3.9 biopython minimap2  mash -y
conda activate klebsiella_analysis
git clone --recursive https://github.com/klebgenomics/KleborateModular.git
cd KleborateModular
usage: ./kleborate-runner.py [-a ASSEMBLIES [ASSEMBLIES ...]] [-o OUTFILE] [--list_modules] [-p PRESET] [-m MODULES] [-h] [--help_all] [--version]

```

Kleborate directory contains:
* Modules directory - available modules for Kleborate
* Shared directory - scripts shared by different modules

List modules
```bash
./kleborate-runner.py --list_modules
```

Available modules for Kleborate
* Basic stats on the assembly's contigs
* Mash-based species detection for Klebsiella and closely-related genera
* MLST on the KpSC aerobactin locus (iuc genes)
* MLST on the KpSC colibactin locus (clb genes
* MLST on the KpSC Rmp locus (rmp genes)
* MLST on the KpSC salmochelin locus (iro genes)
* MLST on the KpSC yersiniabactin locus (ybt and irp genes)
* Chromosomal MLST for Escherichia coli using the Achtman scheme
* Chromosomal MLST for Escherichia coli using the Pasteur scheme
* Chromosomal MLST for the Klebsiella oxytoca species complex
* Chromosomal MLST for the Klebsiella pneumoniae species complex
* Virulence score (0-5) for the Klebsiella pneumoniae species complex, based on the results of the abst, cbst and ybst modules
* Genotyping acquired genes and mutations for the Klebsiella pneumoniae species complex
* Resistance score (0-3) for the Klebsiella pneumoniae species complex, based on the results of the kpsc_amr module
* Resistance gene classes count
* Resistance genes count




