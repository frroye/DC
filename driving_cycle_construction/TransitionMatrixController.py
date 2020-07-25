"""Description: """
import pandas as pd
import numpy as np


class TransitionMatrixController:

    def __init__(self, clustered_file):
        self.clustered_file = clustered_file
        self.df = self.import_csv2pd(self.clustered_file)
        self.cluster_df = self.df['cluster']
        self.states = self.cluster_df.unique()
        self.nb_cluster = len(self.states)

        self.transition_matrix = self.generate_transition_matrix()

    def import_csv2pd(self, file):
        """Import csv to pandas dataframe.
        The first row of the data need to be the column name."""
        df = pd.read_csv(file.path + file.name + file.extension,
                         sep=';', encoding='latin-1')
        return df

    def generate_transition_matrix(self):
        tm = np.zeros((self.nb_cluster, self.nb_cluster))
        chain = list(self.cluster_df)
        for (i, j) in zip(chain, chain[1:]):
            tm[int(i - 1)][int(j - 1)] += 1
        # now convert to probabilities:
        for row in tm:
            s = sum(row)
            if s > 0:
                row[:] = [f / s for f in row]

        return tm

    def get_transition_matrix(self):
        return self.transition_matrix

    def save_transition_matrix(self):
        print()
        #TODO: save transition matrice to csv



