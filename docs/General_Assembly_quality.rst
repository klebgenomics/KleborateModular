.. role:: raw-html-m2r(raw)
   :format: html


The quality and completeness of Kleborate results depends on the quality of the input genome assemblies. In general, you can expect good results from draft genomes assembled with tools like SPAdes from high-depth (>50x) Illumina data, however it is always possible that key genes subject to genotyping may be split across contigs, which can create problems for detecting and typing them accurately.

Assembly quality metrics
~~~~~~~~~~~~~~~~~~~~~~~~

We provide some basic assembly statistics to help users understand their Kleborate results in the context of assembly quality, but we recommend users conduct more comprehensive QC themselves before running Kleborate (e.g. screen for contamination, etc).

The following assembly quality metrics are reported by Kleborate:


* contig count
* N50 (bp)
* largest contig size (bp)
* total size (bp)
* detection of ambiguous bases (yes or no). If yes, the number of ambiguous bases is also provided in brackets.

Additionally, the following warnings that may be indicative of a poorly assembled and/or contaminated assembly are printed in the ``QC_warnings`` column:


* ``ambiguous_bases``\ : the detection of ambiguous bases
* ``total_size``\ : if the total length of the assembly falls under 4.5 Mbp or exceeds 7.5 Mbp (based on the distribution of assembly sizes observed for :raw-html-m2r:`<i>K. pneumoniae</i>` assemblies) 
* ``N50``\ : N50 < 10000bp
