'''
DEPRECIATED BECAUSE BASED AROUND DATA (Processed Reads) OF QUESTIONABLE MEANING
(Is it the n° of contaminant reads ? Or the n° of reads used as a subset by Metaphlan ? Is it how Metaphlan work ?)
'''
# Create a horizontal bargraph from the output of merge_data_abundance.py
# It'll be a summary of the number of taxa, of the chosen level (kingdom, phylum...)
# per site in number of reads.
# Version 2.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# Last update the : June 21 2023
#
# HOW TO LAUNCH:
# python3 
#
# ACCEPTED TAXONS:
#
# INPUT EXAMPLE:
# 
# OUTPUT EXAMPLE:
# 
# ==============================================================================
import sys
import pandas as pd
import colorcet as cc
import optparse as op
from matplotlib import pyplot as plt

def main():
    # Parse Command Line
    parser = op.OptionParser()
    parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input Dataset with contaminants abundances' )
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='The name of the output png' )
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-x', '--index', dest='index', default='Sample', action='store', help='Name of the column to use as an index')
    parser.add_option('-y', '--yaxis', dest='yaxis', default='Site', action='store', help='Name of the column to build the yaxis')
    parser.add_option('-d', '--data', dest='data_column', default=0, action='store', help='WARNING: every column after this index will be considered part of the dataset')
    parser.add_option('-r', '--reads', dest='reads', default='', action='store', help='The input Dataset with the number of reads treated by Metaphlan')
    ( options, spillover ) = parser.parse_args()
     # Error handling
    if not options.input or not options.output or not options.reads:
        parser.print_help()
        sys.exit()
    # The first dataframe, which has all the informations about the samples except the number of reads
    df1 = pd.read_csv(options.input, sep = options.separator, header = 0, index_col = options.index)
    # The second dataframe, which hold the number of reads processed for each sample
    df2 = pd.read_csv(options.reads, sep = options.separator, header = 0, index_col = options.index)
    # The third dataframe, where we keep only the contaminants fractions from the first dataframe
    df3 = df1.iloc[:,int(options.data_column):]
    df33 = df2.iloc[:,:1]
    # We convert the % into fractions
    df3 = (df3/100)
    # Then we add the reads information
    df3 = pd.merge(df3, df33, how='inner', on=options.index)
    # We multiply the fractions by the number of processed reads to get the number of reads of each contaminant for each sample
    df3 = df3.iloc[:,:-1].multiply(df3['Processed reads'],axis="index")
    # To this new dataframe, we add the site information
    df3 = pd.merge(df3, df1[options.yaxis], on='Sample')
    # We get rid of the index
    df3.reset_index(drop=True, inplace=True)
    # Aggregate
    column_map = {col: "sum" for col in df3.columns}
    column_map[options.yaxis] = "first"
    df4 = df3.groupby(df3[options.yaxis]).aggregate(column_map)
    df4 = df4.drop(options.yaxis, axis=1)

    df4.plot.barh(stacked=True,color=cc.glasbey)
    plt.title("Preponderance of contaminant in each site")
    plt.legend(ncols = 3, prop={'size': 5})
    plt.xlabel('reads')
    plt.ylabel(options.yaxis)
    plt.xticks(rotation = 45, fontsize = 8)
    plt.yticks(fontsize = 6)
    plt.tight_layout()
    plt.savefig(options.output, format="png", dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    main()