# ============================================================================== 
# Visualize proximity between samples based on their contaminants using kmean method
#
# Version 2.0 
# Author: Patrick Jacques (patrickjacques@laposte.net)
# laste Update : June 21 2023
#
# HOW TO LAUNCH:
# 
# EXAMPLE:
#
# ============================================================================== 
import sys
import pandas as pd
import seaborn as sns
import colorcet as cc
import optparse as op
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.manifold import MDS
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def extract_data(df,idx):
    vf = df.iloc[:,idx:]
    # keep only rows that have a non-0 value
    vf = vf[(vf > 0.0).any(1)]
    # keep only columns that appear at least once
    return vf[vf.columns[(vf > 0.0).any()]]

def plot_elbow(kmax, sse):
    plt.style.use("fivethirtyeight")
    plt.plot(range(1, kmax), sse)
    plt.xticks(range(1, kmax))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

def get_k_from_elbow(kmax,data,kmeans_kwargs):
    sse = []                            # A list holds the SSE values for each k
    for k in range(1, kmax):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        sse.append(kmeans.inertia_)
    plot_elbow(kmax, sse)
    return KneeLocator(range(1, kmax), sse, curve="convex", direction="decreasing")

def plot_silhouettes_coeff(silhouette_coeffs):
    l = len(silhouette_coeffs)+2
    plt.style.use("fivethirtyeight")
    plt.plot(range(2,l), silhouette_coeffs)
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Coefficient")
    plt.show()

def get_k_from_silhouette(kmax, data, kmeans_kwargs):
    silhouette_coeffs = []              # silhouette coefficients for each k
    for k in range(2, kmax):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(data)
        score = silhouette_score(data, kmeans.labels_)
        silhouette_coeffs.append(score)
    plot_silhouettes_coeff(silhouette_coeffs)
    return silhouette_coeffs.index(max(silhouette_coeffs))

def plot_kmean(mds,kmeans,df,k):
    # generate a color palette with as many colors as there are unique values
    palette = sns.color_palette(cc.glasbey, k).as_hex()
    km_colors = [palette[label] for label in kmeans.labels_]
    plt.scatter(mds[:,0], mds[:,1], c=km_colors)
    plt.xlabel("Coordinate 1")
    plt.ylabel("Coordinate 2")
    for i, txt in enumerate(df.index):
        plt.annotate(txt, (mds[:,0][i]+.3, mds[:,1][i]), fontsize=5)
    plt.show()

def main():
    # Parse Command Line
    parser = op.OptionParser(conflict_handler="resolve")
    parser.add_option( '-i', '--input', dest='input', default='', action='store', help='The input csv table')
    parser.add_option( '-o', '--output', dest='output', default='', action='store', help='the output png image')
    parser.add_option('-s', '--sep', dest='separator', default=',', action='store', help='By default, the output separator is a standard ","')
    parser.add_option('-x', '--index', dest='index_column', default='Sample', action='store', help='Name of the column to use as an index')
    parser.add_option('-h', '--header', dest='header', default=0, action='store', help='Does the input file have a header or not? Must be int, list of int, or None.')
    parser.add_option('-d', '--data', dest='data_columns', default=0, action='store', help='WARNING: every column after this index will be considered part of the dataset')
    parser.add_option('-k', '--kmax', dest='k_maximum', default=40, action='store', help='The maximum number of clusters to consider')
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
    df1 = pd.read_csv(options.input, sep = options.separator, header = options.header, index_col = options.index_column)
    # extract dataset
    df2 = extract_data(df1, int(options.data_columns))
    # multidimensional scaling
    mds = MDS(random_state=0)
    mds = mds.fit_transform(df2)
    data = list(zip(mds[:,0],mds[:,1]))
    # initiate kmean object
    kmeans_kwargs = {"init": "random",
                "n_init": 10,
                "max_iter": 300,
                "random_state": 42}
    '''
    There’s a sweet spot where the SSE (Sum of Square Error) curve starts to bend known as the elbow point.
    The x-value of this point is thought to be a reasonable trade-off between error and number of clusters.
    '''
    k1 = get_k_from_elbow(options.k_maximum, mds, kmeans_kwargs).elbow
    '''
    The silhouette coefficient is a measure of cluster cohesion and separation.
    It quantifies how well a data point fits into its assigned cluster based on two factors:

        How close the data point is to other points in the cluster
        How far away the data point is from points in other clusters

    Silhouette coefficient values range between -1 and 1.
    Larger numbers indicate that samples are closer to their clusters than they are to other clusters. 
    '''
    k2 = get_k_from_silhouette(options.k_maximum, mds, kmeans_kwargs)
    print('The elbow point of the SSE curve is at k = ',k1,' clusters')
    print('The silhouette coefficient is at highest at k = ',k2,' clusters')
    # Choose which K you prefer
    k_name = input('Would you rather use the Elbow or Silhouette result ? (Write either "Elbow" or "Silhouette")')
    k3 = 0
    while k_name != "Elbow" and k_name != "Silhouette":
        k_name = input('Please write either "Elbow" or "Silhouette" with no variation and nothing else')
    if k_name == "Elbow":
        k3 = k1
    elif k_name == "Silhouette":
        k3 = k2
    # final K-mean
    kmeans = KMeans(
        init="random",
        n_clusters= k3,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    kmeans.fit(mds)
    plot_kmean(mds,kmeans,df2,k3)
if __name__ == '__main__':
    main()