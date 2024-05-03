import sys
import pandas as pd
import colorcet as cc
import optparse as op
from matplotlib import pyplot as plt
def mk_plot(df,options):
    df.reset_index().plot(x = "index", kind = 'barh', stacked = True, title = "Relative abundance (%) of contaminants by species", width=0.6, color = cc.b_glasbey_category10)
    plt.ylabel("Species")
    plt.legend(fontsize= 4)
    plt.tight_layout()
    plt.savefig(f"{options.output}.png", format="png", dpi=300, bbox_inches='tight')
    df.to_csv(f"{options.output}.csv",sep=options.separator)

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
    # Import the dataset
    df = pd.read_csv(options.input, sep = options.separator, header = 0)
    if options.category != "":
        # We create an empty dataframe for later:
        dff = pd.DataFrame()
        categories = df[options.category].unique()
        # For idx the current iteration n° and item the current item on the list,
        for idx, item in enumerate(categories):
            # We create a sub-dataframe
            df2 = df.loc[df[options.category] == item]
            df2 = df2.iloc[:,int(options.data_column):]
            df2 = df2.reset_index().drop(["index"], axis=1)
            n_samples = df2.shape[0]
            # Create a new DataFrame with divided columns
            divided_df = df2.assign(**{col: df2[col] / n_samples for col in df2})
            sum_samples = divided_df.sum()
            sum_samples.name = item
            dff = dff.append(sum_samples)
        dff['Unknown'] = 100 - dff.sum(numeric_only=True, axis=1)
        print(dff)
        mk_plot(dff,options)
        

if __name__ == '__main__':
    main()