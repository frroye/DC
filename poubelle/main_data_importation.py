"""
Auteur: Frederique Roy
Date: 2019-10-03
Ce script permet d'importer les données GPS de différents fichiers csv dans une base de données PostgreSQL.
L'utilisateur doit fournir un nom de schema, un nom de table de donnee brute, le nom des file csv.
Le programme permet d'avoir dans la base de donnee PostgreSQL une table de donnees brutes contenant les champs:
 # |  id : int    |   file_id : int   |   course_id : int   |   time : timestamp    |   gps_lat : numeric   |
    gps_long : numeric  |   distance : numeric  |   speed : numeric | acc : numerci |
"""

import psycopg2.extras
#from pre_traitement import *
from DB import *


#connection à la BD
con = psycopg2.connect(user="postgres",
                        password="f1p2e3",
                        port="5432",
                        database="postgres")
cur = con.cursor()
#implementerFonctionSQL(cur) #implementation de fonctions sql necessaire aux prochaines manipulations

"""Indiquer le nom du schema sans majuscules"""
schema = "testupir"

"""Indiquer le nom de la table de données brutes sans majuscules"""
tableDBrutes = "donneesbrutes"

"""Indiquer le nom des fichier csv contenant les données"""
listFiles = ['test2.csv']
#listeFiles = ['marc_andre.csv', 'gabriel.csv', 'jean_simon.csv', 'navid.csv', 'yan.csv', 'pierre_leo.csv', 'kinam.csv', 'pegah.csv']
#listeFiles = ["autobus1.csv", "autobus2.csv", "autobus3.csv", "autobus4.csv"]

"""Indiquer les colonnes correspondant aux champs time, gps_lat, gps_long
    Si disponible, indiquer les colonnes correspondant aux champs speed et acc (acceleration).
    Les colonnes ayant un nom différent de time, gps_lat, gps_long, speed ou acc seront effacées"""
#columnName = ['a', 'b', 'c']
columnName = ['time','EngSpeed','speed','EngFuelRate','distance','Fuel', 'gps_lat','gps_long']

creerSchema(cur, schema) #creation du schema
create_table_db(cur, schema, tableDBrutes, columnName) #creation de la table de donnees brutes
extraction(cur, schema, tableDBrutes, columnName, listFiles) #extraction des donnees contenues dans listFiles

deleteExtraColumns(cur, schema, tableDBrutes, columnName) #delete les colonnes inutiles
comma2dot(cur, schema, tableDBrutes, columnName)
#print(columnName)

#print(cur.fetchall())

#cur.execute("Select * from {}.{};".format(schema, tableDBrutes))
#print(cur.fetchall())

