import sys
import pandas as pd
import optparse as op
import seaborn as sns
from matplotlib import pyplot as plt

# Parse Command Line
parser = op.OptionParser(conflict_handler="resolve")
parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input file is a csv table with all the data' )
parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
parser.add_option('-h', '--header', dest='header', default=0, action='store', help='Does the input file have a header or not? Must be int, list of int, or None.')
parser.add_option('-x', '--idx', dest='index', default='', action='store', help='Column to use as row index for the data (ex: samples names)')
parser.add_option('-d', '--colstart', dest='colstart', default='UNCLASSIFIED', action='store', help='Starting column of the contamination data.')
parser.add_option('-b', '--box', dest='categories', default='', action='store', help='One heatmap for each value in this column')
( options, spillover ) = parser.parse_args()
if not options.input:
        parser.print_help()
        sys.exit()
# Import data
df1 = pd.read_csv(options.input, sep = options.separator, header = int(options.header))
df1 = df1.set_index(options.index)

# Check species
categories = []
if isinstance(options.categories, str):
        print(options.categories)
        categories = df1[options.categories].unique()
elif isinstance(options.categories, int):
        print(options.categories)
        categories = df1.iloc[:,options.categories].unique()
else:
        parser.print_help()
        sys.exit()
# Create a heatmap for each category
categories = categories.tolist()
for i in categories:
        # Keep only row in the category i
        df2 = df1.loc[df1[options.categories] == i]
        # Keep only data values
        df_data = df1.loc[:,options.colstart:]
        # Drop columns with only 0
        df_data = df_data.loc[(df_data!=0).any(axis=1)]
        ax = sns.heatmap(df_data)
        ax.set_title(i,fontsize=6)
        ax.set_xlabel()
        plt.show()