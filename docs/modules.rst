
KleborateModular is organized in modules for analyzing genome assemblies of Klebsiella, Klebsiella oxytoca and Escherichia coli species. The modules perform tasks such as species detection, MLST (Multi-Locus Sequence Typing), virulence scoring, genotyping acquired genes and mutations, and resistance scoring

List modules

.. code-block:: bash

   ./kleborate-runner.py --list_modules

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
* In silico serotyping of K and L locus for the Klebsiella pneumoniae species complex
