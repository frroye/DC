"""
Import CSV data to sql database
Cleaning
Export data to csv

"""

from preprocessing.RawDataController import *

"""
#file_name = "../data/stm/ID_31823_20181110_104529.csv"
files = []
files.append(File("../data/raw_data/stm/", "ID_37060_20181112_112249", ".csv", column_names))
files.append(File("../data/raw_data/test/", "test_wo_Distance", ".csv", column_names))
files.append(File("../data/raw_data/pegah/", "gab", ".csv", column_names))
"""
column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
fc = find_files("../data/raw_data/stm/", column_names)

dataControler = RawDataController(fc)










