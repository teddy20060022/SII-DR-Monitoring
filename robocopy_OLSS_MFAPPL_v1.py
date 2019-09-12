# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:14:07 2019

@author: MuhammadSoSis
"""
import pathlib
import cx_Oracle
import os
from datetime import date
from datetime import datetime
import re
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

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
#print(path_name)

#---file name exists or doesn't exisist---
file = pathlib.Path("{}{}".format(path_name,file_name))
if file.exists ():
    #reading file
    with open('{}'.format(value), 'r') as f:
       data = f.readlines()
       #print(data)

    start_string = 'start data transfer C:\\symscripts\\1_4_1_Transfer.bat OLSS_MFAPPL'
    end_string = 'completed C:\\symscripts\\1_4_1_Transfer.bat OLSS_MFAPPL'
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
    x1 = re.search('\d\d\.\d\d\sm|\sg', matchedLine1)
    ukuran=(x1.group())
    #search_byte = matchedLine1.split('Bytes :  ')[1].split(' m   ')[0]
    print('Bytes : {}'.format(ukuran))
    
    stringToMatch2 = 'Times :   '
    matchedLine2 = ''
    for line2 in data1:
    	if stringToMatch2 in line2:
    		matchedLine2 = line2
    		break
    #print(matchedLine)
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
    
    #Close File
    f.close()
    fh.close()
    
    #insert into table oracle
    try: 
        con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STC\',\'C\',1,\'OLSS_MFAPPL\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'NULL\')'.format(start_time,status,end_time,search_times,file_name,ukuran)
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
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STB\',\'C\',1,\'OLSS_MFAPPL\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
        cur.execute(sql_command)                          
        con.commit()       

    except cx_Oracle.DatabaseError as e: 
        print("There is a problem with Oracle", e) 
    
    finally: 
        if cur: 
            cur.close() 
        if con: 
            con.close()

    