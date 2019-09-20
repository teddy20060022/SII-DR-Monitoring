# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:16:31 2019

@author: MuhammadSoSis
"""
import pathlib
import cx_Oracle 
import os
from datetime import datetime 
import re

os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")
#os.chdir("C:\\instantclient_19_3")

dateTimeObj = datetime.now()
timestampStr1 = dateTimeObj.strftime("%b %d %Y %H:%M:%S")
timestampStr2 = dateTimeObj.strftime("%b %d %Y")
timestampStr3 = dateTimeObj.strftime("%Y%m%d")
tanggal='{}'.format(timestampStr3)
print('Current Timestamp :',tanggal)

file_name = '{}_impdp_pdbaca02.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\RESTORE\\'
#path_name = '\\\\172.24.2.36\\c$\\syncscripts\\logs\\'
value='{}{}'.format(path_name,file_name)
print(r'Path File         :',value)     

#---file name exists or doesn't exisist---
file = pathlib.Path("{}{}".format(path_name,file_name))
if file.exists ():
    #reading file
    with open('{}'.format(value), 'r') as f:
       data = f.readlines()
       #print(data)
    
    #parsing Start Time
    index = 0
    string_start = re.search('Import: ', str(data))
    objstring_start = '{}'.format(string_start)
    #print(objstring_start)

    if objstring_start =='None':
        start_time = 'Null'
        print(r'Start Time        :' ,start_time)
    else:
        objstring_start1 = '{}'.format(string_start.group())
        for baris in data:
            index+=1
            if objstring_start1 in baris:
                break
        for x, lines in enumerate(data):
            if x == index-1 :
                objstar_time = re.search('(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d+\s',str(lines))
                objstar_time1 = re.search('(20)\d{2}',str(lines))
                tahun= '{}'.format(objstar_time1.group())
                start_time = lines.split('{}'.format(objstar_time.group()))[1].split('{}'.format(tahun))[0]
                print(r'Start Time        :' ,start_time)

    #parsing Status
    index1 = 0
    string_status = re.search('completed with|Failed', str(data))
    objstring_status = '{}'.format(string_status)
    #print(objstring_status)   
    if objstring_status =='None':
        status='Null'
        print(r'Status            :' ,status)
    else:
        objstring_status1 = '{}'.format(string_status.group())
        for baris1 in data:
            index1+=1
            if objstring_status1 in baris1:
                break
        for x1, lines1 in enumerate(data):
            if x1 == index1-1 :
                status = lines.split('SYS\_IMPORT\_FULL\_[0-9][0-9]\" ')[0].split(' at')[0]
                print(r'Status            :' ,status)   
     
    #parsing end_time
    index3 = 0
    stringend_time = re.search('Job', str(data))
    objstringend_time = '{}'.format(stringend_time)
    #print(stringend_time)
    if objstringend_time =='None':
        end_time='Null'
        print(r'End Time          :' ,end_time)
    else:
        objstringend_time1 = '{}'.format(stringend_time.group())
        for baris3 in data:
            index3+=1
            if objstringend_time1 in baris3:
                break
    for x3, lines3 in enumerate(data):
        if x3 == index3-1 :
            end_time = lines.split(' at ')[1]
            print(r'End Time          :' ,end_time)
    
    #file_name
    index4 = 0
    string_file_name = re.search('Starting', str(data))
    objstring_file_name = '{}'.format(string_file_name)
    #print(objstring_file_name)
    if objstring_file_name =='None':
        file_name = 'Null'
        print(r'File Name         :',file_name)
    else:
        objstring_file_name1 = '{}'.format(string_file_name.group())
        for baris4 in data:
            index4+=1
            if objstring_file_name1 in baris4:
               break
        for x4, lines4 in enumerate(data):
            if x4 == index4-1 :
                file_name = lines4.split(' system/********@ACAPROD directory=dbdumps ')[1].split(' ' )[0]
                print(r'File Name         :',file_name)

    f.close()
    
    #insert into table oracle
    if objstring_start=='None' or objstring_status=='None' or objstringend_time=='None' or objstring_file_name=='None':
        try: 
            con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')
            #con = cx_Oracle.connect('monitor/monitor@172.17.30.77/XE')    
            cur = con.cursor()
            sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'R\',1,\'pdbaca02\',\'{} {}\',\'{}\',\'{} {}\',\'NULL\',\'{}\',\'NULL\',\'Process Not Completed\')'.format(timestampStr2,start_time,status,end_time,file_name)
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
        try: 
            con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')
            #con = cx_Oracle.connect('monitor/monitor@172.17.30.77/XE')    
            cur = con.cursor()
            sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'R\',1,\'pdbaca02\',\'{} {}\',\'{}\',\'{} {}\',\'NULL\',\'{}\',\'NULL\',\'Process Completed\')'.format(timestampStr2,start_time,status,timestampStr2,end_time,file_name)
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
        #con = cx_Oracle.connect('monitor/monitor@172.17.30.77/XE')    
        cur = con.cursor()
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'R\',1,\'pdbaca02\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
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