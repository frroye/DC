"""Description: """
import pandas as pd
import numpy as np


class TransitionMatrixController:

    def __init__(self, df):
        self.df = df
        self.cluster_df = self.df['cluster']
        self.states = self.cluster_df.unique()
        self.nb_cluster = len(self.states)

        self.transition_matrix = self.generate_transition_matrix()

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



