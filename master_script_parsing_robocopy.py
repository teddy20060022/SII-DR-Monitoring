# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 09:52:44 2019

@author: MuhammadSoSis
"""
#import re
import cx_Oracle
import os
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

file_name = '20190805_backup.log'
path_name = 'D:\\Project\\BSI\\BACKUP\\{}'.format(file_name)

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

"""
string_start = re.search('Files : *PDBSTGACACON01*.*', str(x))
print(string_start)
flag2 = index2 = 0
for baris3 in x:
    baris3.strip().split('\n')
    index2+=1
    if 'Started : ' in baris3:
       flag2 = 1
       break

if flag2 == 0:
   print(f"Sorry couldn't find {string_start}")
else:
   print(f'Found1 {string_start} in line {index2}')

for y, lines in enumerate(x):
    if y == index2 :
        start_time = lines.split('Started : ')[1]
        print(start_time)

"""





#===============================================================================================
"""log_file_path = 'D:\\Project\\BSI\\BACKUP\\20190805_backup.log'
start1 = 'start data transfer C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'
end1 = 'completed C:\\symscripts\\1_4_1_Transfer.bat PDBSTGACACON01'

block_of_lines = []
index=0
with open(log_file_path,'r') as input_data:
    # Skips text before the beginning of the interesting block:
    for baris in (input_data.readlines()):
        baris.strip().split('\n')
        #print(baris)
        index+=1
        print(index)
        if '{}'.format(start1) in baris:
           flag = 1
           break
              
    for i,line in enumerate(input_data.readlines()):
        line.strip().split('\n')
        if i > index: break
        print(line)
        #if '{}'.format(end1) in line:  # Or whatever test is needed
         #   break  
"""

"""
block_of_line = []
data_file = open(log_file_path, 'r')
block = ""
found = False
for line in data_file:
    if found:
        block += line
        if line.strip() == '{}'.format(end1): break
    else:
        if line.strip() == '{}'.format(start1):
            found = True
            block = "Start"

block_of_line.append(line)
print(line)
data_file.close()
"""

"""
started = False
collected_lines = []
with open(log_file_path, 'r') as fp:
     for i, line in enumerate(fp.readlines()):
         if '{}'.format(start1) in line.strip():
             started = True
             print ('started at line', i) # counts from zero !
             #print(line)
             continue
         if started and '{}'.format(end1) in line.strip() :
             #print(line)
             print ('end at line', i)
             break
             # process line 
             #collected_lines.append(line.rstrip())
             #print(collected_lines)
"""