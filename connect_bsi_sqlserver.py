# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:10:24 2019

@author: MuhammadSoSis
"""

import pandas as pd
import pyodbc 
"""
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=172.16.3.120;'
                      'Database=BSI;'
                      'Trusted_Connection=yes;'
                      'uid=user_bsi;'
                      'pwd=password')

cursor = conn.cursor()
cursor.execute('SELECT * FROM BSI.Table')

for row in cursor:
    print(row)
"""

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=172.16.3.120;"
                        "Database=BSI;"
                        "uid=user_bsi;pwd=password123")

df = pd.read_sql_query('create ', cnxn)

