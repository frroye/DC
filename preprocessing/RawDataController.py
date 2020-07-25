
from preprocessing.RawData import RawData
from preprocessing.MicrotripsData import MicrotripsData

from os import listdir
from os.path import isfile, join


class RawDataController:
    def __init__(self, raw_data_file,):
        self.raw_data_file = raw_data_file
        self.clean_data = self.cleanData()
        self.microtrip_files = self.build_microtrips(250)

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
        microtrip_files = []
        for data in self.clean_data:
            data.segment(segment_lenght)
            microtrip_data = MicrotripsData(data)
            file_name = "../data/microtrips/" + data.file.name + "_m" + data.file.extension
            microtrip_data.save_csv(file_name)
            microtrip_files.append(file_name)
        return microtrip_files


def find_files(main_path, column_names):
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







