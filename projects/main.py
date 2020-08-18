from projects.ProjectController import *

"""Initialization of the project parameters"""
project_name = "test_2"
microtrips_len = 250
PCA = True
number_of_cluster = 7
columns = ['T', 'S', 'FuelR', 'FuelR_r', 'FuelRate_std', 'V', 'V_r', 'V_m', 'V_std', 'Acc', 'Dcc', 'Acc_2',
           'Acc_std', 'Idle_p', 'Acc_p', 'Cru_p', 'Cre_p', 'Dcc_p']
cycle_len = 600


"""Initialization of the project controller"""
project_controller = ProjectController(project_name, "")

"""Preprocessing of the data"""

#project_controller.preprocess(microtrips_len)


"""Clustering of the data"""
project_controller.cluster(columns, project_name, PCA, number_of_cluster)


""" """