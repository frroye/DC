"""
Import CSV data to sql database
Cleaning
Export data to csv

"""

import pandas as pd
import psycopg2.extras
from preprocessing.DB import *
from preprocessing.import_export import *


#file_name = "../data/stm/ID_31823_20181110_104529.csv"
files = []
column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
files.append(File("../data/raw_data/stm/", "ID_37060_20181112_112249", ".csv", column_names))
files.append(File("../data/raw_data/test/", "test_wo_Distance", ".csv", column_names))
files.append(File("../data/raw_data/pegah/", "gab", ".csv", column_names))

fc = find_files("../data/raw_data/stm/", column_names)

dataControler = DataController(fc)


#print(raw_data.dtypes)

#print(raw_data.head())










