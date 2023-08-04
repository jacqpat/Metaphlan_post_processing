import pandas as pd
import optparse as op
import sys
import re

# ============================================================================== 
# Conversion script: from Metaphlan merged results table to a csv table
# Version 1.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# Last update the : June 08 2023
#
# HOW TO LAUNCH:
# python3 .\metamerged2csv.py -i METAPHLAN_TABLE -o OUTPUT_TABLE -s SEPARATOR -t TAXON
#
# ACCEPTED TAXONS:
# 'Kingdom','Phylum','Clade','Order','Family','Genus','Species','Taxon'
#
# INPUT EXAMPLE:
# ./examples/merged_abundance_table_175.txt
# OUTPUT EXAMPLE:
# ./examples/merged_abundance_table_175.csv
# ==============================================================================

def return_element_at_position(row,pos=-1):
    # If the row of the given column is list or a tuple, get the last element
    if isinstance(row, (list, tuple)):
        try:
            return row[int(pos)]
        except IndexError:
            return 'No parent'
    else:
        return row

def return_clade_rank(clade_name):
    # return the full name of the clade corresponding to the given shorthand
    ranks = ['k__','p__','c__','o__','f__','g__','s__','t__']
    names = ['Kingdom','Phylum','Clade','Order','Family','Genus','Species','Taxon']
    for i in range(len(ranks)):
        if clade_name.startswith(ranks[i]):
            return names[i]
    return 'Undetermined'

def clean_clade_name(str):
    # get rid of the clade' ranks shorthands in the given clade name
    ranks = ['k__','p__','c__','o__','f__','g__','s__','t__']
    for r in ranks:
        str = str.replace(r,'')
    return str

def clean_clade_ranks(dataframe,parent_clades):
    # Add a column stating the clade' ranks (kingdom, species, etc...)
    # Then clean the clade' name and returned the modified dataframe.
    clade_rank = []
    for i,j in dataframe.iterrows():
        clade_rank.append(return_clade_rank(dataframe['clade_name'][i]))
    dataframe.insert(0,"clade rank",clade_rank)
    dataframe['clade_name'] = dataframe['clade_name'].apply(clean_clade_name)
    parent_clades = parent_clades.apply(clean_clade_name)
    dataframe.insert(1,'clade parent',parent_clades)
    return dataframe

def create_dataframe(filename,stringer):
    # open file
    with open(filename,'r') as raw:
        data = raw.readlines()
    # get rid of comments
    data[:] = [x for x in data if not x.startswith('#')]
    # change samples' names
    data[0] = data[0].replace(stringer,'')
    data[0] = re.sub(stringer, '', data[0])
    # prepare the list of list to be turned into a dataframe
    data1 = []
    for d in data:
        d = d.rstrip('\n')
        d = d.split('\t')
        data1.append(d)
    return pd.DataFrame(data1[1:],columns=data1[0])

def main():
    # Parse Command Line
    parser = op.OptionParser()
    parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input file is a Metaphlan merged table' )
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='The output file is a csv format file' )
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-r', '--remove', dest='remove', default=',', action='store', help='If a substring reoccur in every column name (original files names), use this option to remove it')
    parser.add_option('-t', '--taxon', dest='taxon', default='', action='store', help='The taxon level we want to keep. If none is given, all levels are preserved')
    ( options, spillover ) = parser.parse_args()
    # Error handling
    if not options.input or not options.output:
        parser.print_help()
        sys.exit()
    # Create Dataframe
    df = create_dataframe(options.input, options.remove)
    # Get parent clade' name then keep only last part of the name
    df['clade_name'] = df['clade_name'].str.split('|')
    df_parents = df['clade_name'].apply(lambda x: return_element_at_position(x, -2))
    df['clade_name'] = df['clade_name'].apply(return_element_at_position)
    df = clean_clade_ranks(df,df_parents)
    if options.taxon:
        # keep only the taxon level we want
        df = df.loc[df['clade rank'] == options.taxon]
        # remove column
    df = df.drop(['clade rank', 'clade parent'], axis=1)
    df = df.reset_index()
    df = df.drop(['index'], axis=1)
    df = df.rename(columns={'clade_name': 'Sample'})
    df = df.T
    df.to_csv(options.output,header=False,index=True,sep=options.separator)

if __name__ == '__main__':
    main()