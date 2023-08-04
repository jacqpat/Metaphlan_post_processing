# Metaphlan_post_processing
A pipeline to produce composition bargraphs and cluster dendrograms from Metaphlan results

This pipeline, as its name implies, aims to offer a couple of tools to help in the interpretation of Metaphlan results.
It assumes that you have already run Metaphlan (https://github.com/biobakery/MetaPhlAn) over your data (fastq of your samples)
and that you've already used it to produce a text file summarizing the results. An example of such file produced by metaphlan is
given at 0_original_data/merged_abundance_table_test.txt.

It also assume that you have prepared two other dataframes. One rougthly summarizing everything about your samples (the exact number
of column doesn't matter but the general format is given by 0_original_data/merged_abundance_table_test.txt) and another one with the
information about the number of processed reads and total reads (it may not necessarily have the contamination, paleomix_endogene, and
total columns. Once again, general format given by 0_original_data/samples_read.csv).

TO BE CONTINUED
