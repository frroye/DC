import pandas as pd
import random


class DrivingCycleConstructor:

    def __init__(self, file, transition_matrix, dc_len):
        self.df_segment = self.import_csv2pd(file)
        self.transition_matrix = transition_matrix
        self.len = dc_len

    def import_csv2pd(self, file):
        """Import csv to pandas dataframe.
        The first row of the data need to be the column name."""
        df = pd.read_csv(file.path + file.name + file.extension, sep=';', encoding='latin-1')
        return df

    def select_first_segment(self):
        return random.randint(1, len(self.df_segment))

    def select_next_cluster(self, cluster):
        clusters = range(0, len(self.transition_matrix))
        next_cluster = random.choices(clusters, self.transition_matrix[int(cluster)])
        return next_cluster[0]

    def get_cluster(self, seg):
        return self.df_segment.iloc[seg]["cluster"]

    def select_seg(self, cluster):
        return self.df_segment[self.df_segment['cluster'] == cluster].sample(n=1).index

    def get_seg_length(self, seg):
        return float(self.df_segment.iloc[seg]["cluster"])

    def generate_DC(self):
        seg_i = self.select_first_segment()
        cluster_i = self.get_cluster(seg_i)
        dc_ = [int(cluster_i)]
        dc_len = self.get_seg_length(seg_i)
        while dc_len < self.len:
            next_cluster = self.select_next_cluster(cluster_i)
            next_seg = self.select_seg(next_cluster)
            dc_.append(int(next_seg[0]))
            cluster_i = next_cluster
            dc_len += self.get_seg_length(next_seg)
        return dc_


class DrivingCycle:
    def __init__(self, dc_, df_segment):
        self.dc_ = dc_
        self.df = df_segment

    def compute_parameters(self):
        return 0

    def save(self):
        return 0

class DrivingCyclesController:
    def __init__(self, df_segment, assessment_criteria):
        self.df_segment = df_segment
        self.assessment_criteria = assessment_criteria







