# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:33:45 2019

@author: MuhammadSoSis
"""
import pathlib
import cx_Oracle 
import os
from datetime import date 
from datetime import datetime 
import re

os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")
#os.chdir("C:\\instantclient_19_3")

dateTimeObj = datetime.now()
timestampStr1 = dateTimeObj.strftime("%a %b %d %H:%M:%S %Y")
timestampStr2 = dateTimeObj.strftime("%a %b %d %Y")
#print('Current Timestamp : ', timestampStr1)

myDate = date.today()
tanggal='{:%Y%m%d}'.format(myDate)
#print(tanggal)

#path_name = '\\\\172.24.2.36\\c$\\syncscripts\\logs\\'
file_name = '{}_expdp_pdbaca02.log'.format(tanggal)
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

    #insert into table oracle
    try: 
        con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'B\',1,\'pdbaca02\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Process Completed\')'.format(start_time,status,end_time,elapsed_time,file_name,total_size)
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

    f.close()
else:
    print("File not exist")
    try:
        con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'B\',1,\'pdbaca02\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
        cur.execute(sql_command)                          
        con.commit()       

    except cx_Oracle.DatabaseError as e: 
        print("There is a problem with Oracle", e) 
    
    finally: 
        if cur: 
            cur.close() 
        if con: 
            con.close()
    