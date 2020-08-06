
from preprocessing.RawData import RawData
from preprocessing.MicrotripsData import MicrotripsData
import pandas as pd

from os import listdir
from os.path import isfile, join


class RawDataController:
    def __init__(self, raw_data_file,):
        self.raw_data_file = raw_data_file
        self.clean_data = self.cleanData()
        self.microtrip_data = []

    def cleanData(self):
        clean_data = []
        for file in self.raw_data_file:
            data = RawData(file)
            data.clean()
            data.prepare()
            file_name = "../data/clean_data/" + file.name + "_c" + file.extension
            data.save_csv(file_name)
            clean_data.append(data)
        return clean_data

    def build_microtrips(self, segment_lenght):
        for data in self.clean_data:
            data.segment(segment_lenght)
            self.microtrip_data.append(MicrotripsData(data))

    def save_microtrips(self):
        for data in self.microtrip_data:
            file_name = "../data/microtrips/" + data.file.name + "_m" + ".csv"
            data.save_csv(file_name)

    def combine_microtrips(self):
        df = []
        for data in self.microtrip_data:
            df_ = data.df
            df_['File'] = data.file.name
            #df_.set_index(['File', 'Seg'])
            df.append(df_)
        df = pd.concat(df, axis=0, join='outer', ignore_index=False, keys=None,
                       levels=None, names=None, verify_integrity=False, copy=True)

        df = df.reset_index()
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







