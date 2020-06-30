"""
Import CSV data to sql database
Cleaning
Export data to PostreSQL

"""

import pandas as pd
import psycopg2.extras
from DB import *

file_name = "ID_31823_20181110_104529.csv"
file_name_test = "test2.csv"

user = "postgres"
password = "f1p2e3"
port = "5432"
database = "driving_cycles"

db_controller = DBController(user, password, port, database)



