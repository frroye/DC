import pandas as pd
from preprocessing.import_export import File
#import rpy2
#import rpy2.robjects as robjects
#from rpy2.robjects.packages import importr
import os
#from rpy2.robjects import pandas2ri
#pandas2ri.activate()

import numpy as np
from sklearn.decomposition import PCA



class ClusteringController():

    def __init__(self, files, path="../data/microtrips/"):
        self.path = path  # directory containing microtrip files
        self.microtrips_files = files
        self.df = self.import_all()
        print(self.df)
        #self.df = self.import_csv2pd()

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

    def PCA(self, n_components, columns):
        pca = PCA(n_components)
        df_selected_columns = self.df[columns]
        pca.fit(df_selected_columns)
        print(pca.components_)

    def PCA_(self, n_components):
        pca = PCA(n_components)
        df_PCA = pd.DataFrame(pca.transform(self.df), columns=['PCA%i' % i for i in range(n_components)], index=self.df.index)
        print(df_PCA)


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