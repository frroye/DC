"""
Import CSV data to sql database
Cleaning
Export data to PostreSQL

"""

import pandas as pd
import psycopg2.extras
from preprocessing.DB import *
from preprocessing.import_export import *


#file_name = "../data/stm/ID_31823_20181110_104529.csv"
file_name = "../data/stm/ID_37060_20181112_112249.csv"
file_name_test = "../data/test/test_wo_Distance.csv"
file_name_gab = "../data/pegah/gab.csv"

column_names = ['DateTime', 'Speed', 'Acc', 'FuelRate', 'gps_Lat', 'gps_Long']
raw_data = RawData(file_name, column_names)
raw_data.clean()
raw_data.prepare()
raw_data.add_dayofweek()
#print(dc.df)
raw_data.segment(250)


microtrip_data = MicrotripsData(raw_data)

#print(raw_data.dtypes)

#print(raw_data.head())










