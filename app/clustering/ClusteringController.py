import pandas as pd
from numpy import unique
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from preprocessing.RawDataController import find_files


class ClusteringController:

    def __init__(self, files=[], path="../data/microtrips/"):
        self.path = path  # directory containing microtrip files
        if not files:
            self.microtrips_files = find_files(self.path)
        else:
            self.microtrips_files = files
        self.df = self.import_all()
        self.clustered_df = None
        self.clusters = None

    def import_csv2pd(self, file):
        """Import csv to pandas dataframe.
        The first row of the data need to be the column name."""
        df = pd.read_csv(file.path + file.name + file.extension,
                         sep=';', encoding='latin-1')
        return df

    def import_all(self):
        df = []
        for file in self.microtrips_files:
            df_ = self.import_csv2pd(file)
            #df_['File'] = file.name
            #df_.set_index(['File', 'Seg'])
            df.append(df_)
            print(file.name)
        df = pd.concat(df, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)

        #df = df.reset_index()
        df = df.drop(columns='Seg')
        return df

    def get_microtrips_number(self):
        """ calculate the number of microtrips"""
        return len(self.df.index)

    def PCA(self, n_component, columns):
        """ n_component : number of component of the PCA.
        columns: columns used to execute the PCA
        Transform the data into principal components using PCA.
        Return a dataframe df containing the microtrips described by their new (n_component) component."""
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
        return df

    def kmeans(self, nb_clusters):
        """Cluster the data using kmeans algorithm. """
        # define the model
        model = KMeans(n_clusters=nb_clusters)
        # fit the model
        model.fit(self.clustered_df)
        # assign a cluster to each example
        yhat = model.predict(self.clustered_df)
        self.clusters = unique(yhat)
        # retrieve unique clusters
        self.df["cluster"] = yhat
        self.clustered_df["cluster"] = yhat

    def select_clustering_columns(self, col, PCA=False, n_component=0.80):
        """Select the columns that will be use in the clustering"""
        if PCA:
            self.clustered_df = self.PCA(n_component, col)
        else:
            df = self.df[col]
            df = StandardScaler().fit_transform(df)  # Standardized the features
            df = pd.DataFrame(df)
            df.columns = col
            self.clustered_df = df

    def visualize_cluster2D(self, xlabel=None, ylabel=None, titre="Clustering"):
        """ Plot the clusters in 2D according do xlabel and ylabel dimensions/columns"""
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
        """ Plot the clusters in 3D according to xlabel, ylabel, zlabel dimensions/columns"""
        # nbCluster = getNbCluster(df_segment)
        if xlabel is None:
            xlabel = self.clustered_df.columns[0]

        if ylabel is None:
            ylabel = self.clustered_df.columns[1]

        if zlabel is None:
            zlabel = self.clustered_df.columns[2]

        color = ['0.75', 'b', 'g', 'r', 'c', 'm', '0.75', 'y', 'k', '0.45', 'b', 'g', 'r', 'c', 'm', '0.75', 'y',
                 'k']
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        for i in self.clusters:
            x = self.clustered_df[self.clustered_df['cluster'] == i][xlabel]
            y = self.clustered_df[self.clustered_df['cluster'] == i][ylabel]
            z = self.clustered_df[self.clustered_df['cluster'] == i][zlabel]
            ax.scatter3D(x, y, z, c=color[i])
        pyplot.show()


    def save_csv(self, file_name, path = "../data/clustered_microtrips/"):
        """ Save the df containing the clusters in csv file"""
        if 'cluster' in self.df.columns:
            file_name = path + file_name + ".csv"
            self.df.to_csv(file_name, sep=";")

