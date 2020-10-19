import os
from preprocessing.RawDataController import *
from clustering.ClusteringController import ClusteringController
import time

class ProjectController:
    def __init__(self, project_name, path="../results/"):
        self.project_name = project_name + "/"
        self.create_directory(self.project_name, path)
        self.path = path + self.project_name

    def create_directories(self):
        """Create the require sub directories:
        raw_data, microtrips, clustered_microtrips, clean_data and results."""
        if self.directoryIsEmpty(""):
            self.create_directory('data/', self.path)
            data_sub_directory = ["raw_data", "microtrips", "clustered_microtrips", "clean_data", "results"]
            for directory in data_sub_directory:
                self.create_directory(directory, self.path + 'data/')
        else:
            print(str(self.path) + " is not empty")

    def create_directory(self, directory_name, parent_dir):
        path = os.path.join(parent_dir, directory_name)
        if not os.path.exists(path):
            os.makedirs(path)

    def preprocess(self, microtrip_len):
        """Preprocess the content of data/raw_data.
        Save the resulting clean and segmented data in data/microtrips"""
        if not self.directoryIsEmpty("data/raw_data"):
            column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
            fc = find_files(self.path + "data/raw_data/", column_names)
            microtrip_len = microtrip_len
            data_controler = RawDataController(fc)
            data_controler.build_microtrips(microtrip_len)
            data_controler.save_combine_microtrips(file_name="microtrips" + str(microtrip_len),
                                               path=self.path + "data/microtrips/")
        else:
            print("data/raw_data is empty.")

    def cluster(self, columns, file_name,  PCA=True, number_of_cluster=7):
        clustering_controller = ClusteringController()
        clustering_controller.select_clustering_columns(columns, PCA)
        clustering_controller.kmeans(number_of_cluster)
        clustering_controller.save_csv(file_name, self.path + "data/clustered_microtrips/")

    def directoryIsEmpty(self, sub_directory):
        directory = os.listdir(self.path + sub_directory)
        if len(directory) == 0:
            return 1
        else:
            return 0;



