# ============================================================================== 
# Create dendrogram of proximity between samples based on their contaminants
#
# Version 2.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# laste Update : June 20 2023
#
# HOW TO LAUNCH:
# python3 dendrogram.py -i [Samples_data_and_conta_csv] -o [dendogram.png] -s [separator] -x [index_column_name] -z [colors_column_name] -h [header_row_index] -d [start_conta_column]
#
# EXAMPLE:
# (Windows pathing)
# python3 .\pyscripts\dendrogram.py -i .\examples\Data2_paleofish_June2023_no_unclassified.csv -o .\examples\Dendogram_test2.png -s ';' -d 23 -z Site
# ============================================================================== 
import sys
import pandas as pd
import seaborn as sns
import colorcet as cc
import optparse as op
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.cluster.hierarchy import dendrogram, linkage

def create_colors(df1,df2,colname):
    colors_repertory = {}
    # get the parameters column
    dfcol = df1[colname]
    # keep only elements that are in df2
    dfcol = dfcol[dfcol.index.isin(df2.index)]
    # keep unique values
    dfcol_unique = dfcol.unique()
    # generate a color palette with as many colors as there are unique values
    palette = sns.color_palette(cc.glasbey, len(dfcol_unique)).as_hex()
    # turn dfcol_unique from a series to a list
    list_of_elements = dfcol_unique.tolist()
    # associate the colors with the elements
    for i,v in dfcol.items():
        idx = list_of_elements.index(v)
        colors_repertory[i] = palette[idx]
    return colors_repertory,list_of_elements,palette

def extract_data(df,idx):
    vf = df.iloc[:,idx:]
    # keep only rows that have a non-0 value
    vf = vf[(vf > 0.0).any(1)]
    # keep only columns that appear at least once
    return vf[vf.columns[(vf > 0.0).any()]]

def main():
    # Parse Command Line
    parser = op.OptionParser(conflict_handler="resolve")
    parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input file is a csv table' )
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='the output png image' )
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-x', '--index', dest='index_column', default='Sample', action='store', help='Name of the column to use as an index')
    parser.add_option('-z', '--elements', dest='index_elements', default='Site', action='store', help='Name of the column to use to color the samples')
    parser.add_option('-h', '--header', dest='header', default=0, action='store', help='Does the input file have a header or not? Must be int, list of int, or None.')
    parser.add_option('-d', '--data', dest='data_columns', default=0, action='store', help='WARNING: every column after this index will be considered part of the dataset')
    ( options, spillover ) = parser.parse_args()
    # Error handling
    if not options.input or not options.output:
        parser.print_help()
        sys.exit()
    if not options.data_columns:
        parser.print_help()
        print("give the index of the first data column as a number, not a string or otherwise")
        sys.exit
    # create dataframe
    df1 = pd.read_csv(options.input,sep=options.separator,header=options.header,index_col=options.index_column)
    # extract dataset
    df2 = extract_data(df1, int(options.data_columns))
    # multidimensional scaling
    mds = MDS(random_state=0)
    mds = mds.fit_transform(df2)
    data = list(zip(mds[:,0],mds[:,1]))
    # list of colors for the xlabels
    colors_ticks, elements, palette = create_colors(df1,df2,options.index_elements)
    # creating the dendrogram
    linkage_data = linkage(mds, method='ward', metric='euclidean')
    dendrogram(linkage_data, labels=df2.index, leaf_font_size=3, leaf_rotation=90)
    # fine-tuning and plotting
    plt.title("Dendrogram by identified microbial contaminants")
    plt.xlabel(f'Samples (by {options.index_elements})')
    # get x ticks labels
    ax = plt.gca()
    xlbls = ax.get_xmajorticklabels()
    # change color of the x ticks
    for lbls in xlbls:
        lbls.set_color(colors_ticks[lbls.get_text()])
    # create the legend
    legend_elements = []
    for i in range(len(elements)):
        legend_elements.append(Patch(facecolor = palette[i], label = elements[i]))
    ax.legend(handles=legend_elements, ncols = 4, prop={'size': 4})
    # save dendrogram
    plt.savefig(options.output, format="png", dpi=300, bbox_inches='tight')
    
if __name__ == '__main__':
    main()