"""
#################################################
File name : main_test.py
Author: Fred Roy
Date created: 2019-12-13
Date last modified:
Python Version: 3.?
Description: Objets relatifs à la gestion des bases
            de données, pour le projet mobilité

################################################
"""

import pandas as pd
import psycopg2.extras



class DBController:
    def __init__(self, user, password, port, database):
        self.con = psycopg2.connect(user=user,
                        password=password,
                        port=port,
                        database=database)
        self.cur = self.con.cursor()

        # conteneur de db_brute
        self.raw_db_s = []
        #pre_treaded_DB = Pre_treated_DB()
        #self.pre_treaded_DB = pre_treaded_DB()


    def create_schema(self):
        self.cur.execute("DROP SCHEMA IF EXISTS {} CASCADE ;".format(self.schema))
        self.cur.execute("CREATE SCHEMA {};".format(self.schema))

    def add_raw_db(self, rawDB):
        self.raw_db_s.append(rawDB)

    def extract_raw(self):
        for r_db in self.raw_db_s:
            r_db.extract()


class DBPostgresql:
    def __init__(self, cur, schema, table, column_name):
        self.column_name = column_name
        self.cur = cur
        self.schema = schema
        self.table = table
        self.create_table()

    def create_table(self):
        self.cur.execute("DROP TABLE IF EXISTS {}.{} CASCADE".format(self.schema, self.table))
        self.cur.execute("CREATE TABLE {}.{} (ID int);".format(self.schema, self.table))
        for col in self.column_name:
            self.cur.execute("ALTER TABLE {}.{} ADD COLUMN {} VARCHAR(50)".format(self.schema, self.table, col))
        self.cur.execute("ALTER TABLE {}.{} DROP COLUMN ID".format(self.schema, self.table))


class RawDB (DBPostgresql):
    def __init__(self, cur, schema, table, column_name, file_name):
        DBPostgresql.__init__(self, cur, schema, table, column_name)
        self.file = file_name

    def extract(self):
        with open(self.file, 'r', errors='ignore') as f:
            self.cur.copy_from(f, self.schema + '.' + self.table, sep=";", null='')

    # def __del__(self):
    #    self.cur.execute("DROP TABLE IF EXISTS {}.{} CASCADE".format(self.schema, self.table))



class PreTreatedDB (DBPostgresql):
    def __init__(self, cur, schema_name, table_name):
        DBPostgresql.__init__(self, cur, schema_name, table_name)


