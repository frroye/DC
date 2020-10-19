from projects.ProjectController import *

"""Initialization of the project parameters"""
project_name = "test_3"
microtrips_len = 250
PCA = True
number_of_cluster = 7
parameters = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
           'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
cycle_len = 600


"""Initialization of the project controller"""
project_controller = ProjectController(project_name, "../results/")

"""Creation of the sub directories"""
#project_controller.create_directories()

"""
**** Preprocessing of the data ****
Columns in raw_data subdirectory are expected to be as follow:
'DateTime' : date and time in format AAA-MM-JJ  HH:MM:SS,
'Speed' : speed,
'Acc' : acceleration,
'FuelRate' : fuel rate,
'gps_Lat' : gps latitude,
'gps_Long': gps longitude
"""

#project_controller.preprocess(microtrips_len)


"""Clustering of the data"""
project_controller.cluster(parameters, project_name, PCA, number_of_cluster)


""" """