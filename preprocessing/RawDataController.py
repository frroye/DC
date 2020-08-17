
from preprocessing.RawData import RawData
from preprocessing.MicrotripData import MicrotripData
import pandas as pd

from os import listdir
from os.path import isfile, join
"""Control the preprosessing step. """


class RawDataController:
    def __init__(self, raw_data_file,):
        """ Control the preprocessing of the data.
        Create a list of RawData object with the method cleanData().
        Initialize an empty list microtrip_data that will contain the MicrotripData object."""
        self.raw_data_file = raw_data_file
        self.clean_data = self.cleanData()
        self.microtrip_data = []

    def cleanData(self):
        """ For every raw data file in self.raw_data_file, initialize a RawData() object, clean it, prepare it
        and add it to the clean data list clean_data. Return the clean data list. """
        clean_data = []
        for file in self.raw_data_file:
            data = RawData(file)
            data.clean()
            data.prepare()
            clean_data.append(data)
        return clean_data

    def build_microtrips(self, segment_lenght):
        """Segment the clean data contained in the self.clean_data list using the segment_all method.
         Create a MicrotripData object for every RawData object and append it to the list self.microtrip_data."""
        seg_count = 0
        for data in self.clean_data:
            seg_count = data.segment_all(segment_lenght, seg_count)
            self.microtrip_data.append(MicrotripData(data))

    def save_clean_data(self):
        """Save the every cleaned RawData object in csv format in the clean_data directory, under the same name as
        its raw data parents."""
        for data in self.clean_data:
            file_name = "../data/clean_data/" + data.file.name + data.file.extension
            data.save_csv(file_name)

    def save_combined_clean_data(self):
        """Combine the clean data of the clean_data list into one big dataframe and save it in csv format in the
        clean_data directory."""
        df = []
        for data in self.clean_data:
            df.append(data.df)
        df = pd.concat(df, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)
        file_name = "../data/clean_data/" + "combined_clean_data + " + '.csv'
        df.to_csv(file_name, sep=";", index=False)

        return(df)

    def save_microtrips(self):
        """Save every MicrotripData object contained in the self.microtrip_data list in .csv format in the
        microtrips directory."""
        for data in self.microtrip_data:
            file_name = "../data/microtrips/" + data.file.name + "_m" + ".csv"
            data.save_csv(file_name)

    def save_combine_microtrips(self):
        """Combine the microtrip data of the microtrip_data list into one big dataframe and save it in csv format in the
        microtrips directory."""
        df = []
        for data in self.microtrip_data:
            df_ = data.df
            df_['File'] = data.file.name
            df.append(df_)
        df = pd.concat(df, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)

        file_name = "../data/microtrips/" + "combined_microtrips" + ".csv"
        df.to_csv(file_name, sep=";")
        return df


def find_files(main_path, column_names = []):
    """Look into a directory and return a list of files objects"""
    main_path = main_path
    files = []
    onlyfiles = [f for f in listdir(main_path) if isfile(join(main_path, f))]
    for file in onlyfiles:
        files.append(File(main_path, file[:-4], ".csv", column_names))
    return files


class File:
    def __init__(self, path, name, extension, column_name=[]):
        self.path = path
        self.name = name
        self.extension = extension
        self.column_name = column_name

    def get_full_path(self):
        return self.path + self.name + self.extension







