import sys
import pandas as pd
import colorcet as cc
import optparse as op
from matplotlib import pyplot as plt

def mk_plot(df,options,i="0"):
    df.plot(x = options.index, kind = 'barh', stacked = True, title = "Contamination by CLade", width=1.0, color=cc.glasbey)
    plt.title("Preponderance of contaminant in each site (%)")
    plt.yticks(fontsize = 4)
    plt.legend(fontsize= 4)
    plt.tight_layout()
    if i == "0":
        plt.savefig(f"{options.output}.png", format="png", dpi=300, bbox_inches='tight')
    else:
        plt.savefig(f"{options.output}-{i}.png", format="png", dpi=300, bbox_inches='tight')

def mk_work_df(df,options):
    '''
    INPUT:
    df: Dataframe with the contamination data
    options: options given to the parser, including:
        - data_colum: the index (int) of the column contamination data start at
        - index: the name (string) of the column used to call the samples (rows)
    '''
    contadf = df.iloc[:,int(options.data_column):]
    contadf = pd.concat([contadf,df[options.index]], axis = 1)
    return contadf

def main():
    # Parse Command Line
    parser = op.OptionParser()
    parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input Dataset with contaminants abundances' )
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='The name of the output png' )
    parser.add_option('-d', '--data', dest='data_column', default=0, action='store', help='Starting column of the contamination data. WARNING: every column after this index will be considered part of the dataset')
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-x', '--index', dest='index', default='', action='store', help='Name of the column to use as an index')
    parser.add_option('-c', '--category', dest='category', default='', action='store', help='Name of the column with the categories')
    ( options, spillover ) = parser.parse_args()
     # Error handling
    if not options.input:
        parser.print_help()
        sys.exit()
    # Import the dataset
    df = pd.read_csv(options.input, sep = options.separator, header = 0)
    if options.category != "":
        categories = df[options.category].unique()
        # For idx the current iteration n° and item the current item on the list,
        for idx, item in enumerate(categories):
            # Prepare the data
            df2 = df.loc[df[options.category] == item]
            df3 = mk_work_df(df2,options)
            # Plot the dataset
            mk_plot(df3,options,idx)
    else:
        df2 = mk_work_df(df,options)
        mk_plot(df2,options)

if __name__ == '__main__':
    main()