import pandas as pd
import numpy as np


class DataController:
    def __init__(self, file_name, column_names):
        self.file_name = file_name
        self.datetime_column = column_names[0]
        self.column_names = column_names
        self.df = self.import_csv2pd()

    def import_csv2pd(self):
        """Import csv to pandas dataframe. Based on the stm data. The first row of the data need to be the column name."""
        self.column_names.remove('DateTime')
        dict_column_f = {i: lambda x: (x.replace(',', '.')) for i in self.column_names}
        df = pd.read_csv(self.file_name, sep=';', encoding='latin-1', converters=dict_column_f)
        self.column_names.append('DateTime')
        return df

    def clean(self):
        """Clean raw data"""

        self.df = self.set_data_type()
        self.drop_extra_columns()
        self.df = self.df.dropna()
        self.drop_extra_row()

    def prepare(self):
        self.add_distance()
        self.add_acc()
        return self.df

    def set_data_type(self):
        """Adjust the datatype of the column in the dataframe"""
        self.df = self.df.replace(',', '.')
        self.df[self.datetime_column] = pd.to_datetime(self.df[self.datetime_column], errors='coerce')
        column_list = (list(self.df.columns))
        column_list.remove(self.datetime_column)
        for c in column_list:
            self.df[c] = pd.to_numeric(self.df[c], errors='coerce')
        column_list.append(self.datetime_column)
        return self.df

    def drop_extra_columns(self):
        """Drop columns that are not listed in column_names"""
        extra_column = np.setdiff1d(list(self.df.columns), self.column_names)
        self.df = self.df.drop(columns=extra_column)

    def drop_extra_row(self):
        """Drop duplicated rows"""
        self.df = self.df.drop_duplicates(subset=self.datetime_column)

    def add_distance(self):
        """Compute the distance between the point and the next one and put it in the column DeltaDistance.
        If the column Distance already exists, we suppose it is the cumulative distance: hence the distance between a point
        and the previous is compute.
         If the column Distance doesn't alredy exist, the travelled distance is compute using the average speed.
         """
        if 'Distance' in list(self.df.columns):
            self.df["DeltaDistance"] = self.df["Distance"] - self.df.Distance.shift()
            self.df.drop(columns=["Distance"])
        else:
            self.calculate_distance()

    def add_acc(self):
        """Calculate the acceleration if it is not already in the df.
        Given that the speed is in km/h and that the time is in second, the computed acceleration is in m/s^2"""
        if 'Acc' not in list(self.df.columns):
            kmh2ms = 3.6
            self.df['Acc'] = (self.df["Speed"] - self.df.Speed.shift()) / \
                             (self.df["DateTime"].dt.second - self.df.DateTime.shift().dt.second)/kmh2ms

    def calculate_distance(self):
        """Calculate the distance between two point using the average speed and time"""
        kmh2ms = 3.6
        self.df["DeltaDistance"] = self.df["Speed"]/kmh2ms  # conversion of the speed from km/h to m/s
        self.df["DeltaDistance"] = self.df["DeltaDistance"] * (self.df["DateTime"].dt.second - self.df.DateTime.shift().dt.second)


def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two point using the haversine formula
    :param lat1: latitude of the initial position in degree
    :param lon1: longitude of the initial position in degree
    :param lat2: latitude of the final position in degree
    :param lon2: longitude of the final position in degree
    :return: distance between the two position in meter"""
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))) * 1000
    return res


