"""
Description: The class MicrotripsData is used to create the microtrips from the raw data and to save it to a csv file.

"""

import pandas as pd
from functools import reduce

class MicrotripData:

    def __init__(self, rawData):
        if rawData:
            self.raw_df = rawData.df
            self.file = rawData.file
            self.df = self.summarize_rawData()

    def summarize_rawData(self):
        """Compute the parameters of the microtrips, incluing total time (T), total travel distance (S),
        average speed (V), maximal speed, average running speed, average fuel rate"""
        df_first_occurence = self.raw_df[['Seg', 'DateTime', 'gps_Lat', 'gps_Long', "DayOfWeek"]].\
            drop_duplicates(subset="Seg")
        df_first_occurence = df_first_occurence.set_index('Seg')
        df_first_occurence = df_first_occurence.dropna()
        df = [df_first_occurence,
              self.compute_T(),
              self.compute_S(),
              self.compute_V(),
              self.compute_Vm(),
              self.compute_Vr(),
              self.compute_FuelR(),
              self.compute_FuelRr(),
              self.compute_FuelRstd(),
              self.compute_Vstd(),
              self.compute_acc(),
              self.compute_dcc(),
              self.compute_acc_std(),
              self.compute_a2(),
              self.compute_idle_p(),
              self.compute_acc_p(),
              self.compute_cru_p(),
              self.compute_cre_p(),
              self.compute_dcc_p(),
              self.compute_initial_speed(),
              self.compute_final_speed()
              ]
        df = reduce(lambda left, right: pd.merge(left, right, on=['Seg'], how='outer'), df)
        df = df.dropna(subset=['T'])
        df = df.apply(lambda x: x.fillna(0))
        df[["Acc_p", "Idle_p", "Dcc_p", "Cru_p", "Cre_p"]] = df[["Acc_p", "Idle_p", "Dcc_p", "Cru_p", "Cre_p"]].apply(lambda x: x/df["T"])
        return df

    def save_csv(self, file_name):
        """Save the dataframe containing the microtrips to a .csv into the path given by file_name"""
        self.df.to_csv(file_name, sep=";")

    def compute_T(self):
        """Compute the total time of the microtrips"""
        df = self.raw_df[['Seg', 'Duration']].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'T'}, inplace=True)
        return df

    def compute_S(self):
        """Compute the total travelled distance of the microtrips"""
        df = self.raw_df[['Seg', 'DeltaDistance']].groupby(['Seg']).sum()
        df.rename(columns={'DeltaDistance': 'S'}, inplace=True)
        return df

    def compute_FuelR(self):
        """Compute the average fuel rate of the microtrip"""
        df = self.raw_df[['Seg', 'FuelRate']].groupby(['Seg']).mean()
        df.rename(columns={'FuelRate': 'FuelR'}, inplace=True)
        return df

    def compute_FuelRr(self):
        """Compute the average running fuel rate of the microtrip"""
        df = self.raw_df
        df = df[['Seg', 'FuelRate']][df['FuelRate'] > 0].groupby(['Seg']).mean()
        df.rename(columns={'FuelRate': 'FuelR_r'}, inplace=True)
        return df

    def compute_FuelRstd(self):
        """Compute the fuel rate standard deviation of the microtrips"""
        df = (self.raw_df[['Seg', 'FuelRate']]).groupby(['Seg']).std()
        df.rename(columns={'FuelRate': 'FuelRate_std'}, inplace=True)
        return df

    def compute_V(self):
        """Compute the average speed of the microtrips"""
        df = self.raw_df[['Seg', 'Speed']].groupby(['Seg']).mean()
        df.rename(columns={'Speed': 'V'}, inplace=True)
        return df

    def compute_Vr(self):
        """Compute the average running speed of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Speed']][df['Speed'] > 0].groupby(['Seg']).mean()
        df.rename(columns={'Speed': 'V_r'}, inplace=True)
        return df

    def compute_Vm(self):
        """Compute the maximum speed of the microtrips"""
        df = (self.raw_df[['Seg', 'Speed']]).groupby(['Seg']).max()
        df.rename(columns={'Speed': 'V_m'}, inplace=True)
        return df

    def compute_Vstd(self):
        """Compute the speed standard deviation of the microtrips"""
        df = (self.raw_df[['Seg', 'Speed']]).groupby(['Seg']).std()
        df.rename(columns={'Speed': 'V_std'}, inplace=True)
        return df

    def compute_acc(self):
        """Compute the average positive acceleration of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Acc']][df['Acc'] > 0].groupby(['Seg']).mean()
        return df

    def compute_dcc(self):
        """Compute the average deceleration of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Acc']][df['Acc'] < 0].groupby(['Seg']).mean()
        df.rename(columns={'Acc': 'Dcc'}, inplace=True)
        return df

    def compute_acc_std(self):
        """Compute the acceleration standard deviation of the microtrips"""
        df = self.raw_df
        df = (df[['Seg', 'Acc']]).groupby(['Seg']).std()
        df.rename(columns={'Acc': 'Acc_std'}, inplace=True)
        return df

    def compute_a2(self):
        """Compute the average square acceleration of the microtrips"""
        df = self.raw_df
        df['Acc2'] = df['Acc']**2
        df = (df[['Seg', 'Acc2']]).groupby(['Seg']).mean()
        df.rename(columns={'Acc2': 'Acc_2'}, inplace=True)
        return df

    def compute_idle_p(self):
        """Compute the % of idle time of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Duration']][df['Speed'] < 1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Idle_p'}, inplace=True)
        return df

    def compute_acc_p(self):
        """Compute the % of acceleration time of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Duration']][df['Acc'] > 0.1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Acc_p'}, inplace=True)
        return df

    def compute_cru_p(self):
        """Compute the % of crusing time of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] > 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cru_p'}, inplace=True)
        return df

    def compute_cre_p(self):
        """Compute the % of creeping time of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] < 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cre_p'}, inplace=True)
        return df

    def compute_dcc_p(self):
        """Compute the % of deceleration time of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Duration']][(df['Acc'] < -0.1)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Dcc_p'}, inplace=True)
        return df

    def compute_initial_speed(self):
        """ Compute the initial speed of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Speed']].groupby(['Seg']).first()
        df.rename(columns={'Speed': 'V_i'}, inplace=True)
        return df

    def compute_final_speed(self):
        """Compute the final speed of the microtrips"""
        df = self.raw_df
        df = df[['Seg', 'Speed']].groupby(['Seg']).last()
        df.rename(columns={'Speed': 'V_f'}, inplace=True)
        return df





