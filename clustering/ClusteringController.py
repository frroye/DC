import pandas as pd
from preprocessing.RawDataController import File
#import rpy2
#import rpy2.robjects as robjects
#from rpy2.robjects.packages import importr
import os
#from rpy2.robjects import pandas2ri
#pandas2ri.activate()

import numpy as np
# k-means clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D




class ClusteringController():

    def __init__(self, files, path="../data/microtrips/"):
        self.path = path  # directory containing microtrip files
        self.microtrips_files = files
        self.df = self.import_all()
        self.clusters = None
        self.cluster_center = None

    def import_csv2pd(self, file):
        """Import csv to pandas dataframe.
        The first row of the data need to be the column name."""
        df = pd.read_csv(file.path + file.name + file.extension,
                         sep=';', encoding='latin-1')
        return df

    def import_all(self):
        file_count = 0
        df = []
        for file in self.microtrips_files:
            df_ = self.import_csv2pd(file)
            df_['File'] = file_count
            file_count += 1
            df_.set_index(['File', 'Seg'])
            df.append(df_)
        df = pd.concat(df, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)
        df.set_index(['File', 'Seg'])
        return df

    def get_microtrips_number(self):
        return len(self.df.index)

    def PCA(self, n_component, columns):
        df = self.df[columns]  # select only columns required for PCA
        df = StandardScaler().fit_transform(df)  # Standardized the features
        pca = PCA(n_components=n_component)
        pca.fit(df)
        pca = pca.transform(df)

        columns = []
        for i in range(len(pca[0])):
            columns.append('Component' + str(i))
            i += 1
        df = pd.DataFrame(pca)
        df.columns = columns
        print(df)
        self.df = df
        return df

    def kmeans(self, nb_clusters):
        # define the model
        model = KMeans(n_clusters=nb_clusters)
        # fit the model
        model.fit(self.df)
        # assign a cluster to each example
        yhat = model.predict(self.df)
        self.clusters = unique(yhat)
        # retrieve unique clusters
        self.df["cluster"] = yhat
        self.cluster_center = model.cluster_centers_

    def select_clustering_columns(self, col):
        df = self.df[col]
        df = StandardScaler().fit_transform(df)  # Standardized the features
        df = pd.DataFrame(df)
        df.columns = col
        self.df = df

    def visualize_cluster2D(self, xlabel=None, ylabel=None, titre="Clustering"):
        # nbCluster = getNbCluster(df_segment)
        if xlabel is None:
            xlabel = self.df.columns[0]

        if ylabel is None:
            ylabel = self.df.columns[1]
        color = ['0.75', 'b', 'g', 'r', 'c', 'm', '0.75', 'y', 'k', '0.45', 'b', 'g', 'r', 'c', 'm', '0.75', 'y',
                 'k']
        for i in self.clusters:
            x = self.df[self.df['cluster'] == i][xlabel]
            y = self.df[self.df['cluster'] == i][ylabel]
            pyplot.xlabel(xlabel)
            pyplot.ylabel(ylabel)
            pyplot.title(titre)
            pyplot.plot(x, y, 'o', c=color[i], markersize=6)
        pyplot.show()

    def visualize_cluster3D(self, xlabel=None, ylabel=None, zlabel=None):
        # nbCluster = getNbCluster(df_segment)
        if xlabel is None:
            xlabel = self.df.columns[0]

        if ylabel is None:
            ylabel = self.df.columns[1]

        if zlabel is None:
            zlabel = self.df.columns[2]

        color = ['0.75', 'b', 'g', 'r', 'c', 'm', '0.75', 'y', 'k', '0.45', 'b', 'g', 'r', 'c', 'm', '0.75', 'y',
                 'k']
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        #ax.plot3D(self.df['V'], self.df['Acc'], zs=self.df['FuelR'], c=color[0])
        for i in self.clusters:
            x = self.df[self.df['cluster'] == i][xlabel]
            y = self.df[self.df['cluster'] == i][ylabel]
            z = self.df[self.df['cluster'] == i][zlabel]
            ax.scatter3D(x, y, z, c=color[i])
        pyplot.show()


    def save_csv(self, file_name):
        if 'cluster' in self.df.columns:
            file_name = "../data/clustered_microtrips/" + file_name + ".csv"
            self.df.to_csv(file_name, sep=";")

    """
def Rscale(self, df_c):
    R_scale = robjects.r['scale']
    R_matrix = robjects.r['as.matrix']
    R_df = robjects.r['as.data.frame']
    r_df = pandas2ri.py2ri(df_c)
    r_df = R_df(R_scale(R_matrix(r_df), True, True))
    return (pandas2ri.ri2py_dataframe(r_df))

def identifierCluster(self, cluster, df_segment):
    # inserer le numero de cluster de chaque segemnt dans la df
    cluster_v = cluster[2]
    df_segment['cluster'] = 0
    for i in range(0, len(cluster_v)):
        df_segment.at[i + 1, 'cluster'] = cluster_v[i]
    return df_segment


def pam(self, df, nbCluster, colonnes):
    df_n = self.Rscale(df[colonnes[0]])
    for colonne in colonnes[1:]:
        df_n[colonne] = self.Rscale(df[colonne])
    importr('cluster')
    R_data_frame = robjects.r['data.frame']
    r_df = R_data_frame(df_n)
    R_PAM = robjects.r['pam']
    r_cluster = R_PAM(r_df, nbCluster, diss=False, metric='euclidean')
    df = self.identifierCluster(r_cluster, df)
    return df


def PCA(self, df_segment, nbDim):
    R_PCA = robjects.r['prcomp']
    importr('FactoMineR')
    R_PCA = robjects.r['PCA']
    r_df = pandas2ri.py2ri(df_segment[df_segment.columns.difference(['typetroncon', 'nb_a_d_changement', 'journee', 'heuredepart'])])
    r_pca_df = R_PCA(r_df, True, nbDim)
    #print(r_pca_df[0])
    #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    #print(r_pca_df[1])
    #colonnes = []
    R_df = robjects.r['as.data.frame']
    #print(R_df)
    df = pandas2ri.ri2py_dataframe(R_df(r_pca_df[2][0]))
    df.index +=1
    df.index.name = 'nb'
    df.rename(columns={'Dim.1': 'dim1',
                     'Dim.2': 'dim2', 'Dim.3':'dim3', 'Dim.4':'dim4'}, inplace=True)
    return df
    """