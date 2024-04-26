import pandas as pd
import optparse as op
from matplotlib import pyplot as plt

# Parse Command Line
parser = op.OptionParser(conflict_handler="resolve")
parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input file is a csv table with all the data' )
parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
parser.add_option('-h', '--header', dest='header', default=0, action='store', help='Does the input file have a header or not? Must be int, list of int, or None.')
( options, spillover ) = parser.parse_args()
# Import data
df1 = pd.read_csv(options.input, sep = options.separator, header = int(options.header)).dropna().reset_index(drop=True)