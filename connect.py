# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:30:49 2019

@author: MuhammadSoSis
"""

import os
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")
import cx_Oracle
# con = cx_Oracle.connect('username/password@[ipaddress]/SID')
con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')
print ("Connected To " + con.version)

cur = con.cursor()
cur.execute('select count(*) from USER_DEMO.message_user')
for result in cur:
    print (result)


cur.close()

con.close()