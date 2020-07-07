"""
#################################################
File name : main_test.py
Author: Fred Roy
Date created: 2019-12-13
Date last modified:
Python Version: 3.?
Description: Classes related to database management 

################################################
"""

import pandas as pd
import psycopg2.extras
import psycopg2_addition.exception


class DBController:
    def __init__(self, user, password, port, database):
        #try:
        self.con = psycopg2.connect(user=user,
                                        password=password,
                                        port=port,
                                        database=database)
        #except psycopg2.OperationalError as err:
            #psycopg2_addition.exception.print_psycopg2_exception(err)

        self.cur = self.con.cursor()
        self.schema_set = set()
        self.create_existing_schema()

    def __del__(self):
        """Close the cursor and connection to so the server can allocate bandwidth to other requests"""
        self.cur.close()
        self.con.close()

    def create_schema(self, schema_name):
        """Create a schema in the database if it doesn't already exist """
        self.schema_set.add(Schema(self.cur, schema_name))

    def delete_schema(self, schema_name):
        """Delete a schema if it exists"""
        self.cur.execute("DROP SCHEMA IF EXISTS {} CASCADE;".format(schema_name))

    def create_existing_schema(self):
        """ Instantiate existing schema names"""
        self.cur.execute("SELECT schema_name FROM information_schema.schemata;")
        basic_schema = ["pg_temp_1", "pg_toast_temp_1", "public", "information_schema", "pg_toast", "pg_catalog"]
        for schema in self.cur.fetchall():
            if schema[0] not in basic_schema:
                self.schema_set.add(Schema(self.cur, schema[0]))

    def get_schemas(self):
        schema_names = []
        for schema in self.schema_set:
            schema_names.append(schema.get_name());
        return schema_names

"""
  def add_raw_db(self, rawDB ):
        self.raw_db_s.append(rawDB)

    def extract_raw(self):
        for r_db in self.raw_db_s:
            r_db.extract()
"""


class Schema:
    def __init__(self, cur, name):
        self.cur = cur
        self.name = name
        self.tables_set = set()
        self.create_existing_tables()

    def create(self):
        """Create the schema in the database if it doesn't already exist """
        self.cur.execute("CREATE SCHEMA IF NOT EXISTS {};".format(self.name))

    def delete(self, schema_name):
        """Delete the schema if it exists"""
        self.cur.execute("DROP SCHEMA IF EXISTS {} CASCADE;".format(schema_name))

    def create_existing_tables(self):
        self.cur.execute("SELECT table_schema||'.'||table_name AS full_rel_name FROM information_schema.tables "
                         "WHERE table_schema = {};")

    def get_name(self):
        return self.name

class Table:
    def __init__(self, cur, name, schema, column_name):
        self.cur = cur
        self.name = name
        self.schema = schema
        self.column_name = column_name

    def create(self, overwrite=True):
        """Create a table. Overwrite if already exists or """
        if overwrite:
            self.cur.execute("DROP TABLE IF EXISTS {}.{} CASCADE".format(self.schema, self.name))
            self.cur.execute("CREATE TABLE {}.{} (ID int);".format(self.schema, self.name))
            for col in self.column_name:
                self.cur.execute("ALTER TABLE {}.{} ADD COLUMN {} VARCHAR(50)".format(self.schema, self.name, col))
            self.cur.execute("ALTER TABLE {}.{} DROP COLUMN ID".format(self.schema, self.name))
        else:
            self.cur.execute("CREATE TABLE IF NOT EXISTS {}.{}(id integer)".format(self.schema, self.name))






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


