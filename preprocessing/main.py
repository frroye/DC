"""
Import CSV data to sql database
Cleaning
Export data to PostreSQL

"""

import pandas as pd
import psycopg2.extras
from preprocessing.DB import *
from preprocessing.import_export import *


file_name = "../data/stm/ID_31823_20181110_104529.csv"
file_name_test = "../data/test/test4.csv"


raw_data = import_csv2pd(file_name_test)

raw_data = clean(raw_data)
#print(raw_data.dtypes)

#print(raw_data.head())










