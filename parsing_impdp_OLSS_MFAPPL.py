# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:33:45 2019

@author: MuhammadSoSis
"""
#import cx_Oracle 
import os
import fnmatch
from datetime import date 
import re
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)


file_name = '{}_impdp_OLSS_MFAPPL.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\RESTORE\\'
#print(path_name)

#Simple Filename Pattern Matching Using fnmatch
for file_name1 in os.listdir('{}'.format(path_name)):
    if fnmatch.fnmatch(file_name1, '{}'.format(file_name)):
        value='{}{}'.format(path_name,file_name1)
        #print(value.format(file_name))
        #print(value)
   
#reading file
with open('{}'.format(value), 'r') as f:
   data = f.readlines()
   #print(data)

#parsing Start Time
string_start = re.search('Import: ', str(data))
flag = index = 0
 
for baris in data:
    index+=1
    if string_start.group() in baris:
       flag = 1
       break

for x, lines in enumerate(data):
    if x == index-1 :
        start_time = lines.split('Production on ')[1]
        print(start_time)

#parsing Status
flag1 = index1 = 0
string_status = re.search('completed|Failed', str(data))

for baris1 in data:
    index1+=1
    if string_status.group() in baris1:
        flag1=1
        break

for x1, lines1 in enumerate(data):
    if x1 == index1-1 :
        status = lines.split('SYS\_IMPORT\_FULL\_[0-9][0-9]\" ')[0].split(' at')[0]
        print(status)
"""
#message
string_message = 'Starting '
flag2 = index2 = 0
for baris2 in data:
    index2+=1
    if string_message in baris2:
       flag2 = 1
       break
#print(index2)
with open('{}'.format(value), 'r') as fb:
    message = fb.readlines()[index2:index2+5]
for z in message:
    print (z)
fb.close()
"""
#parsing end_time
s3 = "Job"
flag3 = index3 = 0
 
for baris3 in data:
    index3+=1
    if s3 in baris3:
       flag3 = 1
       break

for x3, lines3 in enumerate(data):
    if x3 == index3-1 :
        end_time = lines.split(' at ')[1]
        print(end_time)

#file_name
keyword_file_name = "Starting "
flag4 = index4 = 0
 
for baris4 in data:
    index4+=1
    if keyword_file_name in baris4:
       flag4 = 1
       break

for x4, lines4 in enumerate(data):
    if x4 == index4-1 :
        file_name = lines4.split(' system/********@STG03P directory=dbdumps ')[1].split(' ' )[0]
        print (file_name)
"""
#file_size
keyword_total_size = "Total estimation"
flag5 = index5 = 0
 
for baris5 in data:
    index5+=1
    if keyword_total_size in baris5:
       flag5 = 1
       break

for x5, lines5 in enumerate(data):
    if x5 == index5-1 :
        total_size = lines5.split('BLOCKS method: ')[1]
        print (total_size)
        """

"""
#insert into table oracle
try: 
    con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
    
    # Now execute the sqlquery 
    cur = con.cursor()
    sql_command = 'INSERT INTO USER_DEMO.ACA_TABLE VALUES (\'3\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Null\')'.format(start_time,status,end_time,elapsed_time,file_name,total_size)
    #cur.execute('INSERT INTO USER_DEMO.ACA_TABLE(acaID, start_time, status, end_time, elapsed, file_name, file_size, Message ) VALUES ("1","Mon Aug 5 00:22:04 2019","successfully completed","","01:20:42","pdbaca02_20190805.dmp","50.97 GB","","")'
    cur.execute(sql_command)          
    #cur.execute("select table_name, owner from dba_tables where owner='USER_DEMO'")
    
    # commit that insert the provided data 
    con.commit()       
    print("value inserted successful") 
    
    #myresult = cur.fetchall()
    #for x in myresult:
    #    print(x)
  
except cx_Oracle.DatabaseError as e: 
    print("There is a problem with Oracle", e) 
  
# by writing finally if any error occurs 
# then also we can close the all database operation 

finally: 
    if cur: 
        cur.close() 
    if con: 
        con.close() 
"""    
#Close File
f.close()