#!/bin/bash

# PARAMETERS
# 1: The output of merge_metaphlan_tables.py, one of the scripts in Metaphlan itself.
metaphlan_txt="..\examples\merged_abundance_table_test.txt"
# 2: The name you want to give to the first step' output which is just [1] but in the .csv format.
metaphlan_csv="..\examples\1_metamerged2csv_output\merged_abundance_table_test.csv"
# 3: The separator. For simplicity's sake, there's one separator for the entire pipeline.
#    So make sure your input files are all using the correct separator.
sep=";"
# 4: (OPTIONAL) The taxonomic level you want to study. Keep this string empty if you want everything.
#    The taxons are the ones used by Metaphlan. In order we have:
#    'Kingdom','Phylum','Clade','Order','Family','Genus','Species','Taxon'. Other strings will lead to errors.
taxon=""
# 5: The main dataframe with all the informations needed for each sample. See in examples: Data1_samples.csv.
df1="..\examples\0_original_data\Data1_samples.csv"
# 6: The main dataframe + contamination data from [2].
df2="..\examples\2_merge_data_abundance_table_output\Data2_samples_with_conta_abundance.csv"
# 7: The name of the dendrogram png file printed by the pipeline.
dendrogram="..\examples\4_dendrogram_output\dendro.png"
# 8: The column index at which the contamination data start in df2. It is 23 for the pipeline' examples but be sure
#    to check yourself for your own dataframes.
col_start="23"
# 9: Name of the column used for coloring the dendrogram. For example: "Site" will color the samples following the sites they were found at.
#    NOTE: It is also used by bar_w_reads to know how many .png to print and what name to give them.
col_col="Site"
# 10: Name of the column used for indexing. i.e: which name will be given to your samples on the Dendrogram.
col_idx="Sample"
# 11: Secondary database with at least two columns: the number of reads in each sample and the number of reads processed by Metaphlan.
df3="..\examples\0_original_data\samples_read.csv"
# 12: Name of the (horizontal) bargraph output of barh_taxa.py
barh="..\examples\3_barh_taxa_output\barh_test.png"
# 13: Name of the repertory in which bar_w_reads.py results will be stocked
barv='..\examples\5_bar_W_reads_output\'
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# THE PIPELINE
# STEP 1: Convert txt into csv
python3 ..\pyscripts\metamerged2csv.py -i ${metaphlan_txt} -o ${metaphlan_csv} -s ${sep} -t ${taxon}
# STEP 2: Append df2 to df1
python3 ..\pyscripts\merge_data_abundance_tables.py -i ${metaphlan_csv} -d ${df1} -o ${df2} -s ${sep} -h 0
if [ -z "$taxon" ]
then
# STEP 3.a: Observe relationship and proximity between every samples in the shape of a Dendrogram.
    python3 ..\pyscripts\dendrogram.py -i ${df2} -o ${dendrogram} -s ${sep} -d ${col_start} -z ${col_col} -x ${col_idx}
else
# STEP 3.b: Observe contamination at specified taxonomic level for each sample in the shape of an horizontal bar graph.
    python3 ..\pyscripts\barh_taxa.py -i ${df2} -r ${df3} -o ${barh} -s ${sep} -d ${col_start}
# STEP 3.c: Observe contamination at specified taxonomic level with one vertical bar graph for each sample.
    python3 ..\pyscripts\bar_w_reads.py -i ${df2} -r ${df3} -o ${barv} -s ${sep} -d ${col_start} -x ${col_idx} -y ${col_col}
fi