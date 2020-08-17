""" Description: """


from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import csv


class AssessmentCriteriaCalculator:

    def __init__(self, raw_data=None, clean_data_path="../data/clean_data/", id=0):
        self.id = id
        if raw_data is not None:
            self.raw_data = raw_data

        if raw_data is None:
            files = self.get_file(clean_data_path)
            self.raw_data = []
            if len(files) is not 0:
                for file in files:
                    df = pd.read_csv(clean_data_path + file, sep=';', encoding='latin-1')
                    df = df.drop(columns=["DateTime", "gps_Lat", "gps_Long", "DayOfWeek"])
                    self.raw_data.append(df)

        self.raw_data = pd.concat(self.raw_data, axis=0, join='outer', ignore_index=False, keys=None,
                           levels=None, names=None, verify_integrity=False, copy=True)
        self.AC = self.summarize_AC()


    def get_parameters(self):
        return self.AC
    def get_file(self, path="../data/clean_data/"):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    def summarize_AC(self):
        total_time = self.compute_duration()
        p_v = {'id': self.id,
               'V': self.compute_V(),
               'Vr': self.compute_Vr(),
               'Vm': self.compute_Vm(),
               'V_std': self.compute_V_std(),
               'FuelR': self.compute_FuelR(),
               'FuelR_r': self.compute_FuelR_r(),
               'FuelR_std': self.compute_FuelR_std(),
               'Acc': self.compute_acc(),
               'Dcc': self.compute_dcc(),
               'Acc2': self.compute_a2(),
               'Acc_std': self.compute_Acc_std(),
               'Idle_p': self.compute_idle_p() / total_time,
               'Acc_p': self.compute_acc_p() / total_time,
               'Dcc_p': self.compute_dcc_p() / total_time,
               'Cru_p': self.compute_cru_p() / total_time,
               'Cre_p': self.compute_cre_p() / total_time,
               #'SAFD': self.compute_SAFD()
               }
        return p_v

    def get_AC(self):
        return self.AC

    def save_csv(self):
        file_name = "../data/assessment_criteria/" + 'assessment_criteria' + ".csv"
        #pd.DataFrame.from_dict(self.AC).to_csv(file_name, sep=";")
        with open(file_name, 'w') as f:
            for key in self.AC.keys():
                f.write("%s,%s\n" % (key, self.AC[key]))

    def compute_SAFD(self):
        """Compute the SAFD (speed and acceleration distribution) of the database"""
        self.raw_data['AccCluster'] = self.raw_data['Acc'].apply(lambda x: findAcluster(x))
        self.raw_data['VCluster'] = self.raw_data['Speed'].apply(lambda x: findVcluster(x))
        SAFD = np.zeros((6, 7))
        df = self.raw_data[['AccCluster', 'VCluster', 'Duration']].groupby(['AccCluster', 'VCluster']).sum()
        df['P'] = df['Duration']/df['Duration'].sum()
        df = df.drop(columns=['Duration'])
        df = df['P'].to_dict()
        for cluster in df:
            a = int(cluster[0])
            v = int(cluster[1])
            SAFD[v, a] = df[a, v]
        return SAFD

    def compute_V(self):
        """Compute the average speed of the database"""
        return self.raw_data[['Speed']].mean()[0]

    def compute_Vr(self):
        """Compute the average running speed of the database"""
        return self.raw_data[['Speed']][self.raw_data['Speed'] > 0].mean()[0]

    def compute_Vm(self):
        """Compute the maximum speed of the database"""
        return self.raw_data[['Speed']].max()[0]

    def compute_V_std(self):
        """Compute the standard deviation of speed of the database"""
        return self.raw_data[['Speed']].std()[0]

    def compute_FuelR(self):
        """Compute the average fuel rate of the database"""
        return self.raw_data[['FuelRate']].mean()[0]

    def compute_FuelR_r(self):
        """Compute the average running fuel rate of the database"""
        return self.raw_data[['FuelRate']][self.raw_data['Speed'] > 0].mean()[0]

    def compute_FuelR_std(self):
        """Compute the standard deviation of average fuel rate of the database"""
        return self.raw_data[['FuelRate']].std()[0]

    def compute_acc(self):
        """Compute the average positive acceleration of the database"""
        return self.raw_data[['Acc']][self.raw_data['Acc'] > 0].mean()[0]

    def compute_dcc(self):
        """Compute the average deceleration of the database"""
        return self.raw_data[['Acc']][self.raw_data['Acc'] < 0].mean()[0]

    def compute_a2(self):
        """Compute the average square acceleration of the database"""
        df = self.raw_data
        df['Acc2'] = df['Acc']**2
        return self.raw_data[['Acc2']].mean()[0]

    def compute_Acc_std(self):
        """Compute the standard deviation of acceleration of the database"""
        return self.raw_data[['Acc']].std()[0]

    def compute_duration(self):
        return self.raw_data[['Duration']].sum()[0]

    def compute_idle_p(self):
        """Compute the % of idle time of the database"""
        return self.raw_data[['Duration']][self.raw_data['Speed'] < 1].sum()[0]

    def compute_acc_p(self):
        """Compute the % of acceleration time of the database"""
        return self.raw_data[['Duration']][self.raw_data['Acc'] > 0.1].sum()[0]

    def compute_cru_p(self):
        """Compute the % of crusing time of the database"""
        return self.raw_data[['Duration']][(self.raw_data['Acc'] > -0.1) & (self.raw_data['Acc'] < 0.1) & (self.raw_data['Speed'] > 20)].sum()[0]

    def compute_cre_p(self):
        """Compute the % of creeping time of the database"""
        return self.raw_data[['Duration']][(self.raw_data['Acc'] > -0.1) & (self.raw_data['Acc'] < 0.1) & (self.raw_data['Speed'] < 20)].sum()[0]

    def compute_dcc_p(self):
        """Compute the % of deceleration time of the database"""
        return self.raw_data[['Duration']][self.raw_data['Acc'] < -0.1].sum()[0]

def findAcluster(a):
    if a < -1.4:
        return 0
    if a >= -1.4 and a < -0.6:
        return 1
    if a >= -0.6 and a < -0.2:
        return 2
    if a >= -0.2 and a < 0.2:
        return 3
    if a >= 0.2 and a < 0.6:
        return 4
    if a >= 0.6 and a < 1.4:
        return 5
    if a >= 1.4:
        return 6
    # gestion d'erreur


def findVcluster(v):
    if v >= 0 and v < 20:
        return 0
    if v >= 20 and v < 40:
        return 1
    if v >= 40 and v < 60:
        return 2
    if v >= 60 and v < 80:
        return 3
    if v >= 80 and v < 100:
        return 4
    if v >= 100:
        return 5




