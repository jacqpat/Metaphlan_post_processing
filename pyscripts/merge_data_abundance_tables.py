import sys
import pandas as pd
import optparse as op

# ============================================================================== 
# merge two .csv, one with the data of our samples and the other with the 
# metaphlan results for each sample
#
# Version 1.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# laste Update : June 09 2023
#
# HOW TO LAUNCH:
# python3 .\merge_data_and_abundance_tables.py -i METAPHAN_CSV_TABLE -d DATA_CSV_TABLE -o OUTPUT_MERGED_TABLE -s SEPARATOR -h HEADER_INDEX
#
# INPUT EXAMPLES:
# - ./examples/merged_abundance_tables.csv ./examples/Data1_paleofish_abundance_April2023.csv
# OUTPUT EXAMPLES:
# - ./examples/Data2_paleofish_abundance_April2023.csv
#
# NOTE:
# Make sure the samples in both tables have the SAME NAMES
# ==============================================================================

def main():
    # Parse Command Line
    parser = op.OptionParser(conflict_handler="resolve")
    parser.add_option( '-i', '--input1', dest='input_conta', default='', action='store', help='The input file is a csv table with contaminants data' )
    parser.add_option( '-d', '--input2', dest='input_data', default='', action='store', help='The input file is a csv table with general samples data' )
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='the output file is the merged csv table' )
    parser.add_option('-h', '--header', dest='header', default=0, action='store', help='Does the input file have a header or not? Must be int, list of int, or None.')
    parser.add_option('-c', '--samples1', dest='samples_conta', default='', action='store', help='The name of the column with the samples names for the first input file')
    parser.add_option('-k', '--samples2', dest='samples_data', default='', action='store', help='The name of the column with the samples names for the second input file')
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    ( options, spillover ) = parser.parse_args()
    # Error handling
    if not options.input_conta or not options.input_data or not options.output:
        parser.print_help()
        sys.exit()
    # create dataframes
    df1 = pd.read_csv(options.input_conta, sep = options.separator, header = int(options.header)).dropna().reset_index(drop=True)
    print("Left Dataframe: Contamination")
    print(df1)
    df1[options.samples_conta] = df1[options.samples_conta].str.replace('_','-')
    df1[options.samples_conta] = df1[options.samples_conta].str.replace('-S\d+$','',regex=True)
    df2 = pd.read_csv(options.input_data, sep = options.separator)
    print("Right Dataframe: Dataset")
    print(df2)
    df2[options.samples_data] = df2[options.samples_data].str.replace('_','-')
    if set(df1[options.samples_conta]) == set(df2[options.samples_data]):
        # merge the two dataframes
        df3 = pd.merge(df2, df1, how = 'inner', on = 'Sample')
        df3.to_csv(options.output, header = True, index = False, sep = options.separator)
    else:
        print("ERROR: the two dataframes 'samples' columns are different!")
        print(df1[options.samples_conta].to_list())
        print(df2[options.samples_data].to_list())

if __name__ == '__main__':
    main()