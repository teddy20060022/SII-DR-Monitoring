# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:52:44 2019

@author: Muhammad Tedi Sopyan
"""
import pathlib
import cx_Oracle
import os
from datetime import date 
from datetime import datetime 
#import re

os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")
#os.chdir("C:\\instantclient_19_3")

dateTimeObj = datetime.now()
timestampStr1 = dateTimeObj.strftime("%a %b %d %H:%M:%S %Y")
timestampStr2 = dateTimeObj.strftime("%a %b %d %Y")
#print('Current Timestamp : ', timestampStr1)

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)

file_name = '{}_backup.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\BACKUP\\'
value='{}{}'.format(path_name,file_name)
#print(value)

#---file name exists or doesn't exisist---
file = pathlib.Path("{}{}".format(path_name,file_name))
if file.exists ():
    #reading file
    with open('{}'.format(value), 'r') as f:
       data = f.readlines()
       #print(data)
    start_string = 'start data transfer C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'
    end_string = 'completed C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'
    flag = index = 0
    for baris in data:
        baris.strip().split('\n')
        #print(baris)
        index+=1
        if '{}'.format(start_string) in baris:
           flag = 1
           break

    flag1 = index1 = 0
    for baris1 in data:
        baris1.strip().split('\n')
        #print(baris1)
        index1+=1
        if '{}'.format(end_string) in baris1:
            flag1 = 1
            break

    with open('{}'.format(value), 'r') as fh:
        data = fh.readlines()[index-1:index1]
        #print(data)
    
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
    
    f.close()
    fh.close()
    #insert into table oracle
    try: 
        con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STA\',\'C\',1,\'PDBSTGACACON01\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Process Completed\')'.format(start_time,status,end_time,search_times,file_name,search_byte)
        cur.execute(sql_command)          
        con.commit()       
        print("value inserted successful") 

    except cx_Oracle.DatabaseError as e: 
        print("There is a problem with Oracle", e) 

    finally: 
        if cur: 
            cur.close() 
        if con: 
            con.close()

else:
    print("File not exist")
    try:
        con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STA\',\'C\',1,\'PDBSTGACACON01\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
        cur.execute(sql_command)                          
        con.commit()       

    except cx_Oracle.DatabaseError as e: 
        print("There is a problem with Oracle", e) 
    
    finally: 
        if cur: 
            cur.close() 
        if con: 
            con.close()