# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:16:07 2019

@author: MuhammadSoSis
"""

import os
import fnmatch
from datetime import date 
import re
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)

file_name = '{}_backup.log'.format(tanggal)
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

#print('Files : *OLSS_MFAPPL*.*')
start_string = 'start data transfer C:\\symscripts\\1_4_1_Transfer.bat pdbaca02'
end_string = 'completed C:\\symscripts\\1_4_1_Transfer.bat pdbaca02'
flag = index = 0
for baris in data:
    index+=1
    if start_string in baris:
       flag = 1
       break
#print(baris)
#print(index)

flag1 = index1 = 0
for baris1 in data:
    index1+=1
    if '{}'.format(end_string) in baris1:
        flag1 = 1
        break
#print(baris1)
#print(index1)

with open('{}'.format(value), 'r') as fh:
    data1 = fh.readlines()[index-1:index1]
    #print(data)
    #for x in data:
     #   print (x)
print('====================================================================')
print('Tanggal hari ini : {}'.format(tanggal))

print('File_name : {}'.format(value))
print('====================================================================')
stringToMatch = 'Started : '
matchedLine = ''
for line in data1:
	if stringToMatch in line:
		matchedLine = line
		break
#print(matchedLine)
start_time = matchedLine.split('Started : ')[1]
print('Started : {}'.format(start_time))

stringToMatch1 = 'Bytes : '
matchedLine1 = ''
for line1 in data1:
	if stringToMatch1 in line1:
		matchedLine1 = line1
		break
#print(matchedLine1)
x1 = re.search('[0-9][0-9]\.[0-9][0-9][0-9]\sg|m', matchedLine1)
ukuran=(x1.group())
#search_byte = matchedLine1.split('Bytes :  ')[1].split(' g|m   ')[0]
print('Bytes : {}'.format(ukuran))

stringToMatch2 = 'Times :   '
matchedLine2 = ''
for line2 in data1:
	if stringToMatch2 in line2:
		matchedLine2 = line2
		break
#print(matchedLine2)
search_times = matchedLine2.split('Times :   ')[1].split(' ')[0]
print('Times : {}'.format(search_times))

stringToMatch3 = 'Ended : '
matchedLine3 = ''
for line3 in data1:
	if stringToMatch3 in line3:
		matchedLine3 = line3
		break
#print(matchedLine3)
end_time = matchedLine3.split('Ended : ')[1]
print('Ended : {}'.format(end_time))

stringToMatch4 = 'Files : '
matchedLine4 = ''
for line4 in data1:
	if stringToMatch4 in line4:
		matchedLine4 = line4
		break
#print(matchedLine4)
file_name = matchedLine4.split('Files : ')[1]
print('File Name : {}'.format(file_name))

stringToMatch5 = 'completed'
matchedLine5 = ''
for line5 in data1:
	if stringToMatch5 in line5:
		matchedLine5 = line5
		break
#print(matchedLine5)
status = matchedLine5.split('-------------------- ')[1].split(' ')[0]
print('Status : {}'.format(status))

#insert into table oracle
"""  
try: 
    con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
    # Now execute the sqlquery 
    cur = con.cursor()
    sql_command = 'INSERT INTO USER_DEMO.ACA_TABLE VALUES (\'2\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Null\')'.format(start_time,status,end_time,search_times,file_name,search_byte)
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
print('====================================================================')


#Close File
f.close()
fh.close()