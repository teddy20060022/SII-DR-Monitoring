# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:33:45 2019

@author: MuhammadSoSis
"""
import cx_Oracle 
import os
import fnmatch
from datetime import date 
import re
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)

file_name = '{}_expdp_OLSS_MFAPPL.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\BACKUP\\'
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
string_start = re.search('Export: ', str(data))
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
string_status = re.search('successfully completed|Failed', str(data))
status=(string_status.group())
print(status)

#parsing End Time
string_end = "Job "
flag2 = index2 = 0
 
for baris2 in data:
    index2+=1
    if string_end in baris2:
       flag2 = 1
       break

for x2, lines2 in enumerate(data):
    if x2 == index2-1 :
        end_time = lines2.split('successfully completed at ')[1].split(' elapsed')[0]
        print(end_time)

#parsing Elapsed
s3 = "elapsed"
flag3 = index3 = 0
 
for baris3 in data:
    index3+=1
    if s3 in baris3:
       flag3 = 1
       break

for x3, lines3 in enumerate(data):
    if x3 == index3-1 :
        elapsed_time = lines.split('elapsed 0 ')[1]
        print(elapsed_time)

#file_name
keyword_file_name = "Dump file"
flag4 = index4 = 0
 
for baris4 in data:
    index4+=1
    if keyword_file_name in baris4:
       flag4 = 1
       break

for x4, lines4 in enumerate(data):
    if x4 == index4 :
        file_name = lines4.split('/dbdumps/')[1]
        print (file_name)

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
value1 = "\'{}\'"
value2 = "\'{}\'"
value3 = "\'{}\'"
value4 = "\'{}\'"
value5 = "\'{}\'"
value6 = "\'{}\'"
#print(value.format(start_time, status, end_time, elapsed_time, file_name, total_size))
print(value1.format(start_time))
print(value2.format(status))
print(value3.format(end_time))
print(value4.format(elapsed_time))
print(value5.format(file_name))
print(value6.format(total_size))
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
      
#Close File
f.close()