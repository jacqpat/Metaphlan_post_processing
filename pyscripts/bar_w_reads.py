# ============================================================================== 
# Create a bargraph from the output of merge_data_abundance.py
# Version 1.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# Last update the : June 20 2023
#
# HOW TO LAUNCH:
# python3 
#
# ACCEPTED TAXONS:
# 
#
# INPUT EXAMPLE:
# -i C:\Users\pajacques\Documents\metaphlan_krona\data_merged_abundance_taxons\Data2_paleofish_clade_April2023.csv -r C:\Users\pajacques\Documents\metaphlan_krona\samples_read.csv
# OUTPUT EXAMPLE:
# -o C:\Users\pajacques\Documents\metaphlan_krona\graphs\par_site_clade_reads\Abbeville_clade_reads.png"
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
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='The path to the png output' )
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-r', '--reads', dest='reads', default='', action='store', help='The input Dataset with the number of reads treated by Metaphlan')
    parser.add_option('-x', '--index', dest='index_column', default='Sample', action='store', help='Name of the column to use as an index')
    parser.add_option('-y', '--print', dest='print_column', default='Site', action='store', help='Name of the column to show as png')
    ( options, spillover ) = parser.parse_args()
    # Error handling
    if not options.input or not options.output or not options.reads:
        parser.print_help()
        sys.exit()
    # The first dataframe, which has all the informations about the samples except the number of reads
    df1 = pd.read_csv(options.input, sep = options.separator, header = 0, index_col = options.index_column)
    # The second dataframe, which hold the number of reads processed for each sample
    df2 = pd.read_csv(options.reads, sep = options.separator, header = 0, index_col = options.index_column)
    # Extract all the sites in the dataframe into a list
    sites = list(set(df1[options.print_column].tolist()))
    for site in sites:
        # Create a dataframe keeping only the samples from site
        sf1 = df1[df1[options.print_column]==site]
        # We merge the subframe with the second dataframe
        df3 = pd.merge(sf1, df2, how='inner', on = options.index_column)
        # We convert the % into fractions
        df4 = (df3.iloc[:,23:-5]/100)
        # We multiply the fractions by the number of processed reads to get the number of reads of each contaminant for each sample
        df4 = df4.multiply(df3['Processed reads'],axis="index")
        # Get rid of contaminants with no read in any sample
        df5 = df4[(df4 > 0.0).any(1)]
        if not df5.empty:
            # plot the graph
            try:
                df5.plot.bar(stacked=True,color=cc.glasbey)
                plt.title(site)
                plt.rcParams["font.size"] = "8"
                plt.legend(ncols=5, prop={'size': 4})
                plt.xlabel('Samples')
                plt.xticks(rotation = 45)
                plt.ylabel('reads')
                plt.rcParams["font.size"] = "6"
                plt.xticks(rotation = 45)
                plt.savefig(f"{options.output}\{site}.png", format="png", dpi=300, bbox_inches='tight')
            except TypeError:
                print(f"{site} doesn't have enough data to plot")
        else:
            print(f"{site} has no value")
if __name__ == '__main__':
    main()