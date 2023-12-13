#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 12:48:20 2023

@author: misno48
"""

'''
Create class 'DatabaseConnection' to handle query operation and
connection between python and MySQL database.
'''

import mysql.connector
from mysql.connector import errorcode

config = {
    'user' : 'root',
    'database' : 'quran'
    }

class DatabaseConnection():

        #Constructor
        def __init__(self):
            
            try:
                #Create database connection
                self.db_connect = mysql.connector.connect(**config)
                #Create a Cursor
                self.cursor = self.db_connect.cursor()
            
            except mysql.connector.Error as err:
                
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Something is wrong with your user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print("Database does not exist")
                else:
                    print(err)
                    
        def Select(self, query):
            self.cursor.execute(query)
            self.data = self.cursor.fetchall()
            return self.data
        
        #Destructor
        def __del__(self):
            #Close Cursor
            self.cursor.close()
            #Close DB Connection
            self.db_connect.close()
#==========================================================================End
'''
Ambil data nomor index, surat, ayat, dan teks ayat dari tabel id_indonesian
'''
def getData(sql_query):
    db = DatabaseConnection()
    query = (sql_query)
    data = db.Select(query)
    return data