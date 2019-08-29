# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:15:42 2019

@author: MuhammadSoSis
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 16:33:45 2019

@author: MuhammadSoSis
"""
import cx_Oracle 
import re
import os
os.chdir("C:\\Program Files\\Oracle\\instantclient_19_3")

"""parsing Start Time"""
file_open =open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log','r')
searchfile = file_open.readlines()
string_start = re.search('Export: ', str(searchfile))
flag = index = 0
 
for baris in searchfile:
    baris.strip().split('\n')
    #print(baris)
    index+=1
    if string_start.group() in baris:
       flag = 1
       break

fa = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx = fa.readlines()
for x, lines in enumerate(fx):
    if x == index-1 :
        start_time = lines.split('Production on ')[1]
        print(start_time)

"""parsing Status"""
import re
fp1 = 'D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log'
f1 = open(fp1)
searchfile = f1.readlines()   
flag1 = index1 = 0
string_status = re.search('successfully completed|Failed', str(searchfile))
#print(string_status.group())

for baris1 in f1:
    baris1.strip().split('\n')
    #print(baris)
    index+=1
    if string_status.group() in baris1:
       flag1 = 1
       break

fa1 = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx1 = fa1.readlines()
for x1, lines1 in enumerate(fx1):
    if x1 == index-1 :
        status = lines.split('01" ')[1].split('at ')[0]
        #print (status)


"""parsing End Time"""
string_end = "Job "
fp2 = 'D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log'
f2 = open(fp2)   
flag2 = index2 = 0
 
for baris2 in f2:
    baris2.strip().split('\n')
    #print(baris)
    index2+=1
    if string_end in baris2:
       flag2 = 1
       break

fa2 = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx2 = fa2.readlines()
for x2, lines2 in enumerate(fx2):
    if x2 == index2-1 :
        end_time = lines2.split('successfully completed at ')[1].split(' elapsed')[0]
        #print (end_time)


"""parsing Elapsed"""
s3 = "elapsed"
fp3 = 'D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log'
f3 = open(fp3)   
flag3 = index3 = 0
 
for baris3 in f3:
    baris3.strip().split('\n')
    #print(baris)
    index3+=1
    if s3 in baris3:
       flag3 = 1
       break

fa3 = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx3 = fa3.readlines()
for x3, lines3 in enumerate(fx3):
    if x3 == index3-1 :
        elapsed_time = lines.split('elapsed 0 ')[1]
        #print (elapsed_time)

"""file_name"""
keyword_file_name = "Dump file"
open_file4 = 'D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log'
f4 = open(open_file4)   
flag4 = index4 = 0
 
for baris4 in f4:
    baris4.strip().split('\n')
    #print(baris)
    index4+=1
    if keyword_file_name in baris4:
       flag4 = 1
       break

fa4 = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx4 = fa4.readlines()
for x4, lines4 in enumerate(fx4):
    if x4 == index4 :
        file_name = lines4.split('/dbdumps/')[1]
        #print (file_name)

"""file_size"""
keyword_total_size = "Total estimation"
open_file5 = 'D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log'
f5 = open(open_file5)   
flag5 = index5 = 0
 
for baris5 in f5:
    baris5.strip().split('\n')
    #print(baris)
    index5+=1
    if keyword_total_size in baris5:
       flag5 = 1
       break

fa5 = open('D:\\Project\\BSI\\BACKUP\\20190805_expdp_OLSS_MFAPPL.log')
fx5 = fa5.readlines()
for x5, lines5 in enumerate(fx5):
    if x5 == index5-1 :
        total_size = lines5.split('BLOCKS method: ')[1]
        #print (total_size)

"""insert into table oracle"""  
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
try: 
    con = cx_Oracle.connect('USER_DEMO/oracle@192.168.0.101/DB11G')    
    # Now execute the sqlquery 
    cur = con.cursor()
    sql_command = 'INSERT INTO USER_DEMO.ACA_TABLE VALUES (\'2\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'Null\')'.format(start_time,status,end_time,elapsed_time,file_name,total_size)
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
        
"""close"""
file_open.close()
fa.close()
f1.close()
fa1.close()
f2.close()
fa2.close()
f3.close()
fa3.close()
f4.close()
fa4.close()
f5.close()
fa5.close()
