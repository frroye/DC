"""
Description: The class RawData is used to handle raw GPS and consumption data coming from a unique csv file.

"""

import pandas as pd
import numpy as np


class RawData:
    def __init__(self, file):
        self.file = file  # File object
        self.pace = 1
        self.column_names = file.column_name
        self.df = self.import_csv()

    def get_file(self):
        return self.file

    def get_df(self):
        return self.df

    def import_csv(self):
        """Import csv to pandas dataframe. Based on the stm data.
        The first row of the csv data need to be the column name.
        """
        self.column_names.remove('DateTime')
        print(self.file.name)
        dict_column_f = {i: lambda x: (x.replace(',', '.')) for i in self.column_names}
        df = pd.read_csv(self.file.get_full_path(), sep=';', encoding='latin-1', converters=dict_column_f)
        self.column_names.append('DateTime')
        return df

    def clean(self):
        """Clean raw data"""
        self.df = self.set_data_type()
        self.drop_extra_columns()
        self.df = self.df.dropna()
        self.drop_extra_row()

    def prepare(self):
        """ Prepare the raw data to be divided into microtrips by adding information as
        time between two points, travelled distance between two points, acceleration and day of the week."""
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

    def add_acc(self):
        """Calculate the acceleration if it is not already in the df.
        Given that the speed is in km/h and that the time is in second, the computed acceleration is in m/s^2"""
        if 'Acc' not in list(self.df.columns):
            kmh2ms = 3.6
            self.df['Acc'] = (self.df["Speed"] - self.df.Speed.shift()) / self.df['Duration']/kmh2ms

    def add_distance(self):
        """Calculate the distance between two point using the average speed and time"""
        kmh2ms = 3.6
        self.df["DeltaDistance"] = self.df["Speed"]/kmh2ms  # conversion of the speed from km/h to m/s
        self.df["DeltaDistance"] = self.df["DeltaDistance"] * self.df['Duration']

    def add_dayofweek(self):
        """Add the day of the week to the df."""
        self.df["DayOfWeek"] = self.df["DateTime"].dt.dayofweek

    def separate_races(self):
        """ Separate the self.df according to the races. The races are separated base on the Duration of a row.
        If the duration is bigger than the pace, than a new dataframe is created. It return a list of dataframe, with
        a dataframe per race."""
        self.drop_extra_row()
        self.df['cut'] = False
        self.df.loc[(self.df.Duration > self.pace), 'cut'] = True
        cut_index = self.df.index[self.df.cut == True].tolist()
        cut_index.insert(0, self.df.first_valid_index())
        cut_index.append(self.df.last_valid_index())
        df_ = []
        for i, j in zip(cut_index[0:-1], cut_index[1:]):
            df = self.df.iloc[i:j, :]
            if len(df) > 0:
                df = df.drop(df[df["Duration"] > self.pace].index)
                df = df.drop(columns="cut")
                df_.append(df)
        return df_

    def segment(self, len_segment):
        """ Divide the data into microtrips (or segment) of desire length.
        Add a column Seg that contains the microtrip identifier"""
        self.drop_extra_row()
        self.df["Seg"] = (self.df["DeltaDistance"].cumsum() / len_segment).apply(np.floor)

    def segment_all(self, len_segment, seg_count):
        """Segment the raw data into smaller segment (microtrips) of equal length. Separate the different races
        contained in the df, and taking into consideration the segment count."""
        df_ = self.separate_races()
        for df in df_:
            df["Seg"] = (df["DeltaDistance"].cumsum() / len_segment + seg_count).apply(np.floor)
            seg_count = df['Seg'].max()
        self.df = pd.concat(df_, axis=0, join='outer', ignore_index=False, keys=None,
                                  levels=None, names=None, verify_integrity=False, copy=True)
        return seg_count+1

    def save_csv(self, file_name):
        """Save the dataframe in csv file following file_name path."""
        self.df.to_csv(file_name, sep=";", index=False)
