# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 10:41:43 2019
@author: Muhammad Tedi Sopyan
"""
#import pandas as pd
import pyodbc

##########CONFINS##########
try:
    server ='192.168.138.133'
    db ='DRMON'
    tcon ='yes'
    usern ='drmonuser'
    pwd ='P@ssw0rd234'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
    sql = 'SELECT @@version'
    cursor = cnxn.cursor()
    cursor.execute(sql)
    for row in cursor:
        print('CONFINS = %r' % (row,))
except pyodbc.Error as ex:
    print("There is a problem with CONFINS:", ex)
    sqlstate = ex.args[0]


#######OLSS#######
try:
    server ='192.168.140.26'
    db ='drmon'
    tcon ='yes'
    usern ='drmonuser'
    pwd ='P@ssw0rd234'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
    sql = 'SELECT @@version'
    cursor = cnxn.cursor()
    cursor.execute(sql)
    for row in cursor:
        print('OLSS = %r' % (row,))
except pyodbc.Error as ex:
    print("There is a problem with OLSS:", ex)
    
    sqlstate = ex.args[0]
    if sqlstate == '08001':
        print(r'error')
        pass
    

##########MONITORING##########
try:
    server ='172.17.30.77'
    db ='DRMONITORING'
    tcon ='yes'
    usern ='qlik'
    pwd ='P@ssw0rd23'
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
    sql = 'SELECT @@version'
    cursor = cnxn.cursor()
    cursor.execute(sql)
    for row in cursor:
        print('MONITORING = %r' % (row,))
    
except pyodbc.Error as ex:
    #sqlstate = ex.args[0]
    print("There is a problem with MONITORING :", ex)
