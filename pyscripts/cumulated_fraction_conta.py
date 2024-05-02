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
    parser.add_option('-d', '--data', dest='data_column', default=0, action='store', help='Starting column of the contamination data. WARNING: every column after this index will be considered part of the dataset')
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-x', '--index', dest='index', default='', action='store', help='Name of the column to use as an index')
    parser.add_option('-c', '--category', dest='category', default='', action='store', help='Name of the column with the categories')
    ( options, spillover ) = parser.parse_args()
    # Import the dataset
    df = pd.read_csv(options.input, sep = options.separator, header = 0)
    if options.category != "":
        categories = df[options.category].unique()
        # For idx the current iteration n° and item the current item on the list,
        for idx, item in enumerate(categories):
            # We create a sub-dataframe
            df2 = df.loc[df[options.category] == item]
            df2 = df2.iloc[:,int(options.data_column):]
            df2 = df2.reset_index().drop(["index"], axis=1)
            print(df2)
            print(df2.sum())
        

if __name__ == '__main__':
    main()