# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:33:45 2019

@author: Muhammad Tedi Sopyan
"""
import pathlib
import cx_Oracle 
import os
from datetime import datetime 
import re
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")
dateTimeObj = datetime.now()
timestampStr1 = dateTimeObj.strftime("%b %d %Y %H:%M:%S")
timestampStr2 = dateTimeObj.strftime("%a %b %d %Y")
timestampStr3 = dateTimeObj.strftime("%Y%m%d")
tanggal='{}'.format(timestampStr3)
#print('Current Timestamp : ', timestampStr1)

file_name = '{}_expdp_PDBSTGACACON01.log'.format(tanggal)
path_name = 'D:\\Project\\BSI\\BACKUP\\'
#path_name = 'C:\\symscripts\\logs\\'
value='{}{}'.format(path_name,file_name)
print(r'Path File :' ,value)

#---file name exists or doesn't exisist---
file = pathlib.Path("{}{}".format(path_name,file_name))
if file.exists ():
    #reading file
    with open('{}'.format(value), 'r') as f:
       data = f.readlines()
           
    #parsing Start Time
    index = 0
	string_start = re.search('Export: ', str(data))
	objstring_start = '{}'.format(string_start)
	#print(objstring_start) 
	if objstring_start == 'None':
		start_time ='No Data Start Time'
        print(r'Start Time :' ,start_time)
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
				start_time = lines.split('{}'.format(objstar_time.group()))[1].split(tahun)[0]
				print(start_time)
    
    #parsing Status
    index1 = 0
    string_status = re.search('successfully completed|Failed', str(data))
    objstring_status = '{}'.format(string_status)
    #print(objstring_status)   
    if objstring_status =='None':
        status='No Data Status'
        print(r'Status :' ,status)
    else:
        objstring_status1 = '{}'.format(string_status.group())
        status = objstring_status1
        print(r'Status :' ,status)
    
    #parsing End Time
    index2 = 0
	string_end = re.search('Job', str(data))
    objstring_end = '{}'.format(string_end)
    if objstring_end =='None':
        end_time ='No Data End Time'
        print(r'End Time :' ,end_time)
    else:
        objstring_end2 = '{}'.format(string_end.group())
		for baris2 in data:
			index2+=1
			if string_end2 in baris2:
			   break
		for x2, lines2 in enumerate(data):
			if x2 == index2-1 :
				objend_time = re.search('(Mon|Tue|Wed|Thus|Sat|Sun)\s(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d+\s',str(lines2))
                objend_time1 = re.search('(20)\d{2}\selapsed\s\d\s\d{2}\:\d{2}\:\d{2}',str(lines2))
                value1 = '{}'.format(objend_time.group())
                value2 = '{}'.format(objend_time1.group())
                #print(value1)
                #print(value2)
                end_time = lines2.split('{}'.format(value1))[1].split('{}'.format(value2))[0]
                print(r'End Time :' ,end_time)
    
    #parsing Elapsed
    index3 = 0
    string_elapsed = re.search('elapsed', str(data))
    objstring_elapsed = '{}'.format(string_elapsed)
    #print(objstring_elapsed)
    if objstring_elapsed == 'None':
        elapsed_time='No Data Elepsed Time'
        print(r'Elapsed Time :' ,elapsed_time)
    else:
        objstring_elapsed2 = '{}'.format(string_elapsed.group())
        for baris3 in data:
            index3+=1
            if objstring_elapsed2 in baris3:
                break
        for x3, lines3 in enumerate(data):
            if x3 == index3-1 :
                elapsed_time = lines.split('elapsed 0 ')[1]
                print(r'Elapsed Time :' ,elapsed_time)
    
    #file_name
    index4 = 0
    stringfile_name = re.search('Dump file', str(data))
    objstringfile_name = '{}'.format(stringfile_name)
    #print(objstringfile_name)
    if objstringfile_name == 'None':
        file_name='No Data File Name'
        print(r'File Name :' ,file_name)
    else:
        objstringfile_name1 = '{}'.format(stringfile_name.group())
        for baris4 in data:
            index4+=1
            if objstringfile_name1 in baris4:
               break
        for x4, lines4 in enumerate(data):
            if x4 == index4 :
                file_name = lines4.split('/dbdumps/')[1]
                print (r'File Name :' ,file_name)
    
    #file_size
    index5 = 0
    stringtotal_size = re.search('Total estimation', str(data))
    objtotal_size = '{}'.format(stringtotal_size)
    #print(objtotal_size)
    if objtotal_size == 'None':
        total_size = 'No Data Total Size'
        print(r'Total Size :' ,total_size)
    else:
        objtotal_size1 = '{}'.format(stringtotal_size.group())
        for baris5 in data:
            index5+=1
            if objtotal_size1 in baris5:
                break
    for x5, lines5 in enumerate(data):
        if x5 == index5-1 :
            total_size = lines5.split('BLOCKS method: ')[1]
            print (r'Total Size :' ,total_size)
    
    f.close()
    
    #insert into table oracle
    if objstring_start=='None' or objstring_status=='None' or objstring_end=='None' or objstring_elapsed=='None' or objstringfile_name=='None' or objtotal_size=='None':
        try: 
            con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')
			#con = cx_Oracle.connect('monitor/monitor@172.17.30.77/XE')
            cur = con.cursor()
            sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ST1\',\'B\',SEQ_STAB.NEXTVAL,\'PDBSTGACACON01\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Process Not Complete\')'.format(timestampStr1,status,end_time,elapsed_time,file_name,total_size)
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
            sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ST1\',\'B\',SEQ_STAB.NEXTVAL,\'PDBSTGACACON01\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Process Complete\')'.format(start_time,status,end_time,elapsed_time,file_name,total_size)
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
        sql_command = 'insert into USER_DEMO.Monitoring VALUES(\'ST1\',\'B\',SEQ_STAB.NEXTVAL,\'PDBSTGACACON01\',\'{}\',\'FAILED\',\'NULL\',\'NULL\',\'NULL\',\'NULL\',\'File not found\')'.format(timestampStr1)
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
        