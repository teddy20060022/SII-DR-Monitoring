# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:52:44 2019

@author: Muhammad Tedi Sopyan
"""
from datetime import date 
#import re
#import cx_Oracle
import os
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)

file_name = '{}_backup.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\BACKUP\\{}'.format(file_name)
print(path_name)

#print('Files : *PDBSTGACACON01*.*')
start_string = 'start data transfer C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'
end_string = 'completed C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'
flag = index = 0
with open(path_name) as files:
    for baris in (files.readlines()):
        baris.strip().split('\n')
        #print(baris)
        index+=1
        if '{}'.format(start_string) in baris:
           flag = 1
           break
files.close()
flag1 = index1 = 0
with open(path_name) as file:
    for baris1 in (file.readlines()):
        baris1.strip().split('\n')
        #print(baris1)
        index1+=1
        if '{}'.format(end_string) in baris1:
            flag1 = 1
            break
file.close()
with open(path_name) as fh:
    data = fh.readlines()[index-1:index1]
    #print(data)
    for x in data:
        print (x)
print('====================================================================')
print('Tanggal hari ini : {}'.format(tanggal))

print('File_name : {}'.format(path_name))
print('====================================================================')
stringToMatch = 'Started : '
matchedLine = ''
for line in data:
	if stringToMatch in line:
		matchedLine = line
		break
#print(matchedLine)
start_time = matchedLine.split('Started : ')[1]
print('Started : {}'.format(start_time))

stringToMatch1 = 'Bytes :   '
matchedLine1 = ''
for line1 in data:
	if stringToMatch1 in line1:
		matchedLine1 = line1
		break
#print(matchedLine)
search_byte = matchedLine1.split('Bytes :   ')[1].split(' ')[0]
print('Bytes : {}'.format(search_byte))

stringToMatch2 = 'Times :   '
matchedLine2 = ''
for line2 in data:
	if stringToMatch2 in line2:
		matchedLine2 = line2
		break
#print(matchedLine)
search_times = matchedLine2.split('Times :   ')[1].split(' ')[0]
print('Times : {}'.format(search_times))

stringToMatch3 = 'Ended : '
matchedLine3 = ''
for line3 in data:
	if stringToMatch3 in line3:
		matchedLine3 = line3
		break
#print(matchedLine3)
end_time = matchedLine3.split('Ended : ')[1]
print('Ended : {}'.format(end_time))

stringToMatch4 = 'Files : '
matchedLine4 = ''
for line4 in data:
	if stringToMatch4 in line4:
		matchedLine4 = line4
		break
#print(matchedLine4)
file_name = matchedLine4.split('Files : ')[1]
print('File Name : {}'.format(file_name))

stringToMatch5 = 'completed'
matchedLine5 = ''
for line5 in data:
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