from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np


class AssessmentCriteriaCalculator:

    def __init__(self, raw_data=None, clean_data_path="../data/clean_data/"):
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

    def get_file(self, path="../data/clean_data/"):
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        return onlyfiles

    def compute_SAFD(self):
        self.raw_data['AccCluster'] = self.raw_data['Acc'].apply(lambda x: findAcluster(x))
        self.raw_data['VCluster'] = self.raw_data['Speed'].apply(lambda x: findVcluster(x))
        SAFD = np.zeros((6, 7))
        df = self.raw_data[['AccCluster', 'VCluster', 'Duration']].groupby(['AccCluster', 'VCluster']).sum()
        df['P'] = df['Duration']/df['Duration'].sum()
        print(df)


    def compute_T(self):
        """Compute the total time of the microtrips"""
        df = self.rawData.get_df()[['Seg', 'Duration']].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'T'}, inplace=True)
        return df

    def compute_S(self):
        """Compute the total travelled distance of the microtrips"""
        df = self.rawData.get_df()[['Seg', 'DeltaDistance']].groupby(['Seg']).sum()
        df.rename(columns={'DeltaDistance': 'S'}, inplace=True)
        return df

    def compute_FuelR(self):
        """Compute the average fuel rate of the microtrip"""
        df = self.rawData.get_df()[['Seg', 'FuelRate']].groupby(['Seg']).mean()
        df.rename(columns={'FuelRate': 'FuelR'}, inplace=True)
        return df

    def compute_FuelRr(self):
        """Compute the average running fuel rate of the microtrip"""
        df = self.rawData.get_df()
        df = df[['Seg', 'FuelRate']][df['FuelRate'] > 0].groupby(['Seg']).mean()
        df.rename(columns={'FuelRate': 'FuelR_r'}, inplace=True)
        return df

    def compute_FuelRstd(self):
        """Compute the fuel rate standard deviation of the microtrips"""
        df = (self.rawData.get_df()[['Seg', 'FuelRate']]).groupby(['Seg']).std()
        df.rename(columns={'FuelRate': 'FuelRate_std'}, inplace=True)
        return df

    def compute_V(self):
        """Compute the average speed of the microtrips"""
        df = self.rawData.get_df()[['Seg', 'Speed']].groupby(['Seg']).mean()
        df.rename(columns={'Speed': 'V'}, inplace=True)
        return df

    def compute_Vr(self):
        """Compute the average running speed of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Speed']][df['Speed'] > 0].groupby(['Seg']).mean()
        df.rename(columns={'Speed': 'V_r'}, inplace=True)
        return df

    def compute_Vm(self):
        """Compute the maximum speed of the microtrips"""
        df = (self.rawData.get_df()[['Seg', 'Speed']]).groupby(['Seg']).max()
        df.rename(columns={'Speed': 'V_m'}, inplace=True)
        return df

    def compute_Vstd(self):
        """Compute the speed standard deviation of the microtrips"""
        df = (self.rawData.get_df()[['Seg', 'Speed']]).groupby(['Seg']).std()
        df.rename(columns={'Speed': 'V_std'}, inplace=True)
        return df

    def compute_acc(self):
        """Compute the average positive acceleration of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Acc']][df['Acc'] > 0].groupby(['Seg']).mean()
        return df

    def compute_dcc(self):
        """Compute the average deceleration of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Acc']][df['Acc'] < 0].groupby(['Seg']).mean()
        df.rename(columns={'Acc': 'Dcc'}, inplace=True)
        return df

    def compute_acc_std(self):
        """Compute the acceleration standard deviation of the microtrips"""
        df = self.rawData.get_df()
        df = (df[['Seg', 'Acc']]).groupby(['Seg']).std()
        df.rename(columns={'Acc': 'Acc_std'}, inplace=True)
        return df

    def compute_a2(self):
        """Compute the average square acceleration of the microtrips"""
        df = self.rawData.get_df()
        df['Acc2'] = df['Acc']**2
        df = (df[['Seg', 'Acc2']]).groupby(['Seg']).mean()
        df.rename(columns={'Acc2': 'Acc_2'}, inplace=True)
        return df

    def compute_idle_p(self):
        """Compute the % of idle time of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][df['Speed'] < 1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Idle_p'}, inplace=True)
        return df

    def compute_acc_p(self):
        """Compute the % of acceleration time of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][df['Acc'] > 0.1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Acc_p'}, inplace=True)
        return df

    def compute_cru_p(self):
        """Compute the % of crusing time of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] > 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cru_p'}, inplace=True)
        return df

    def compute_cre_p(self):
        """Compute the % of creeping time of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] < 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cre_p'}, inplace=True)
        return df

    def compute_dcc_p(self):
        """Compute the % of deceleration time of the microtrips"""
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] < -0.1)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Dcc_p'}, inplace=True)
        return df



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




