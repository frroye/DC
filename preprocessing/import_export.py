import pandas as pd
import numpy as np
from functools import reduce
from math import *
import os


class RawData:
    def __init__(self, path, file_name, extension, column_names):
        self.path = path
        self.file_name = file_name
        self.extension = extension
        self.column_names = column_names
        self.df = self.import_csv2pd()

    def get_file(self):
        return self.file_name

    def get_df(self):
        return self.df

    def import_csv2pd(self):
        """Import csv to pandas dataframe. Based on the stm data.
        The first row of the data need to be the column name."""
        self.column_names.remove('DateTime')
        dict_column_f = {i: lambda x: (x.replace(',', '.')) for i in self.column_names}
        df = pd.read_csv(self.path + self.file_name + self.extension, sep=';', encoding='latin-1', converters=dict_column_f)
        self.column_names.append('DateTime')
        return df

    def clean(self):
        """Clean raw data"""
        self.df = self.set_data_type()
        self.drop_extra_columns()
        self.df = self.df.dropna()
        self.drop_extra_row()

    def prepare(self):
        self.add_duration()
        self.add_distance()
        self.add_acc()
        self.add_dayofweek()
        return self.df

    def set_data_type(self):
        """Adjust the datatype of the column in the dataframe"""
        self.df = self.df.replace(',', '.')
        self.df["DateTime"] = pd.to_datetime(self.df["DateTime"], errors='coerce')
        column_list = (list(self.df.columns))
        column_list.remove("DateTime")
        for c in column_list:
            self.df[c] = pd.to_numeric(self.df[c], errors='coerce')
        column_list.append("DateTime")
        return self.df

    def drop_extra_columns(self):
        """Drop columns that are not listed in column_names"""
        extra_column = np.setdiff1d(list(self.df.columns), self.column_names)
        self.df = self.df.drop(columns=extra_column)

    def drop_extra_row(self):
        """Drop duplicated rows"""
        self.df = self.df.drop_duplicates(subset="DateTime")

    def add_duration(self):
        """Calculate the time between two point """
        self.df["Duration"] = (self.df["DateTime"] - self.df.DateTime.shift()).dt.total_seconds()

    def add_distance(self):
        """Compute the distance between the point and the next one and put it in the column DeltaDistance.
        If the column Distance already exists, we suppose it is the cumulative distance: hence the distance between a point
        and the previous is compute.
         If the column Distance doesn't alredy exist, the travelled distance is compute using the average speed.

        if 'Distance' in list(self.df.columns):
            self.df["DeltaDistance"] = self.df["Distance"] - self.df.Distance.shift()
            self.df.drop(columns=["Distance"])
        else:
        """
        self.calculate_distance()

    def add_acc(self):
        """Calculate the acceleration if it is not already in the df.
        Given that the speed is in km/h and that the time is in second, the computed acceleration is in m/s^2"""
        if 'Acc' not in list(self.df.columns):
            kmh2ms = 3.6
            self.df['Acc'] = (self.df["Speed"] - self.df.Speed.shift()) / self.df['Duration']/kmh2ms

    def calculate_distance(self):
        """Calculate the distance between two point using the average speed and time"""
        kmh2ms = 3.6
        self.df["DeltaDistance"] = self.df["Speed"]/kmh2ms  # conversion of the speed from km/h to m/s
        self.df["DeltaDistance"] = self.df["DeltaDistance"] * self.df['Duration']

    def add_dayofweek(self):
        self.df["DayOfWeek"] = self.df["DateTime"].dt.dayofweek

    def segment(self, len_segment):
        """ Divide the data into microtrips (or segment) of desire length.
        Add a column Seg that contains the microtrip identifier"""
        self.drop_extra_row()
        self.df["Seg"] = (self.df["DeltaDistance"].cumsum() / len_segment).apply(np.floor)


class MicrotripsData:

    def __init__(self, rawData):
        self.rawData = rawData
        self.df = self.summarize_rawData()

    def summarize_rawData(self):
        df_first_occurence = self.rawData.get_df()[['Seg', 'DateTime', 'gps_Lat', 'gps_Long', "DayOfWeek"]].\
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
              self.compute_dcc_p()
              ]
        df = reduce(lambda left, right: pd.merge(left, right, on=['Seg'], how='outer'), df)
        df = df.dropna(subset=['T'])
        df = df.apply(lambda x: x.fillna(0))
        df[["Acc_p", "Idle_p", "Dcc_p", "Cru_p", "Cre_p"]] = df[["Acc_p", "Idle_p", "Dcc_p", "Cru_p", "Cre_p"]].apply(lambda x: x/df["T"])
        pd.set_option('display.max_columns', 500)
        return df

    def save_csv(self, file_name):
        self.df.to_csv(file_name, sep=";")


    def compute_T2(self):
        """Compute the total time of the microtrips"""
        df = self.rawData.get_df()
        df_max = df[['Seg', 'DateTime']].groupby(['Seg']).max()
        df_max.rename(columns={'DateTime': 'time_max'}, inplace=True)
        df_min = df[['Seg', 'DateTime']].groupby(['Seg']).min()
        df_min.rename(columns={'DateTime': 'time_min'}, inplace=True)

        df = df_max.merge(df_min, left_on='Seg', right_on='Seg')
        df["T"] = (df["time_max"] - df["time_min"]).dt.total_seconds()
        return df["T"]

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
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][df['Speed'] < 1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Idle_p'}, inplace=True)
        return df

    def compute_acc_p(self):
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][df['Acc'] > 0.1].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Acc_p'}, inplace=True)
        return df

    def compute_cru_p(self):
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] > 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cru_p'}, inplace=True)
        return df

    def compute_cre_p(self):
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] > -0.1) & (df['Acc'] < 0.1) & (df['Speed'] < 20)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Cre_p'}, inplace=True)
        return df

    def compute_dcc_p(self):
        df = self.rawData.get_df()
        df = df[['Seg', 'Duration']][(df['Acc'] < -0.1)].groupby(['Seg']).sum()
        df.rename(columns={'Duration': 'Dcc_p'}, inplace=True)
        return df

    def compute_nb_small_big_microtrips(self):
        pd.set_option('display.max_columns', None)
        self.df_ = self.df[self.df['S'] < 240]
        print(len(self.df_.index))
        print('-')
        df_ = self.df[self.df['S'] > 260]
        print(len(df_.index))


class File:
    def __init__(self, path, name, extension, column_name="unknown"):
        self.path = path
        self.name = name
        self.extension = extension
        self.column_name = column_name


class DataController:
    def __init__(self, raw_data_file,):
        self.raw_data_file = raw_data_file
        self.microtrip_files = self.built_microtrips(250)

    def built_RawData(self, file):
        data = RawData(file.path, file.name, file.extension, file.column_name)
        data = data.clean()
        data = data.prepare()
        return data

    def built_microtrips(self, segment_lenght, ):
        microtrip_files = []
        for file in self.raw_data_file:
            data = RawData(file.path, file.name, file.extension, file.column_name)
            print(file.name)
            data.clean()
            data.prepare()
            data.segment(segment_lenght)
            microtrip_data = MicrotripsData(data)
            file_name = "../data/microtrips/" + file.name + "_m" + file.extension
            microtrip_data.save_csv(file_name)
            microtrip_files.append(file_name)

        return microtrip_files


from os import listdir
from os.path import isfile, join


def find_files(main_path, column_names):
    main_path = main_path
    files = []
    onlyfiles = [f for f in listdir(main_path) if isfile(join(main_path, f))]
    for file in onlyfiles:
        files.append(File(main_path, file[:-4], ".csv", column_names))
    return files









