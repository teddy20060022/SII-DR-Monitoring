# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:16:31 2019

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
file_name = '{}_impdp_OLSS_MFAPPL.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\RESTORE\\'
value='{}{}'.format(path_name,file_name)
#print(value.format(file_name))     

#Connection to oracle
con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')
#con = cx_Oracle.connect('monitor/monitor@172.17.30.77/XE')    
cur = con.cursor()

#---file name exists or doesn't exisist---
file = pathlib.Path("{}{}".format(path_name,file_name))
if file.exists ():
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
    #insert into table oracle
    try: 
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STC\',\'R\',3,\'OLSS_MFAPPL\',\'{}\',\'{}\',\'{} {}\',\'NULL\',\'{}\',\'NULL\',\'Process Complete\')'.format(start_time,status,timestampStr2,end_time,file_name)
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
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'STC\',\'R\',6,\'OLSS_MFAPPL\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
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

