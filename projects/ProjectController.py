import os
from preprocessing.RawDataController import *
from clustering.ClusteringController import ClusteringController
import time



class ProjectController:
    def __init__(self, project_name, path="../results/"):
        self.project_name = project_name + "/"
        self.path = path
        self.create_directory(self.project_name, self.path)
        self.create_directory('data/', self.path+self.project_name)
        data_sub_directory = ["raw_data", "microtrips", "clustered_microtrips", "clean_data", "results"]
        for directory in data_sub_directory:
            self.create_directory(directory, self.path+self.project_name+'data/')

    def create_directory(self, directory_name, parent_dir):
        directory = directory_name

        # Path
        path = os.path.join(parent_dir, directory)

        # Create the directory
        if not os.path.exists(path):
            os.makedirs(path)

    def preprocess(self, microtrip_len):
        column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
        fc = find_files(self.path + self.project_name + "data/raw_data/", column_names)
        microtrip_len = microtrip_len
        data_controler = RawDataController(fc)
        data_controler.build_microtrips(microtrip_len)
        data_controler.save_combine_microtrips(file_name="microtrips" + str(microtrip_len),
                                               path=self.path + self.project_name + "data/microtrips/")

    def cluster(self, columns, file_name,  PCA=True, number_of_cluster=7):

        clustering_controller = ClusteringController()
        clustering_controller.select_clustering_columns(columns, PCA)
        clustering_controller.kmeans(number_of_cluster)
        clustering_controller.save_csv(file_name, self.path + self.project_name + "data/clustered_microtrips/")


