# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:10:24 2019
@author: Muhammad Tedi Sopyan
"""
######confins#####
#from datetime import datetime,timedelta
import os
import fnmatch
import pyodbc 
import re
import glob, time
try:
    server ='192.168.138.133'
    db ='DRMON'
    tcon ='yes'
    usern ='drmonuser'
    pwd ='P@ssw0rd234'
    #cnxn = pyodbc.connect('DSN=TEST;UID=sa;PWD=Pa55w.rd')
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
    #sql = 'select A.[DRSystem] ,A.[ProcessCode] ,[Scheme] ,A.[LogDate] ,[StartTime] ,[Status] ,[EndTime] ,[ElapsedTime] ,[FileName] from'
    cursor = cnxn.cursor()
    #cursor.execute(sql)
    
    sql0 = "select [MJob].[job_id] from DRMON.dbo.[Master_Job_ID] AS [MJob] WHERE [MJob].[DRSystem] = 'CON' AND [MJob].ProcessCode = 'C' \
        	AND [MJob].Scheme = 'APPROVAL' "
    result_set0 = cursor.execute(sql0)
    for row0 in result_set0:
        print('CONFINS = %r' % (row0[0]))
    v_job_id = row0[0]
    #print(job_id)
    
    
    sql = "SELECT * FROM OPENQUERY (CONFINSDR, \'Select [DRSystem] ,[ProcessCode] ,[LogDate] ,[StartTime] ,[Status] ,[EndTime] ,[ElapsedTime],[Message] \
         		from (SELECT ''CON'' AS [DRSystem], ''C'' AS [ProcessCode] , ROW_NUMBER() OVER (PARTITION BY [sJOB].[job_id] ORDER BY [run_date], [run_time] ) AS [Seq] \
        , (select \
        CASE when convert(time,getdate()) > convert(time,''04:15:00'') then convert(datetime,convert(date,getdate())) \
        else \
        convert(datetime,convert(date,getdate()-1)) \
        end) AS [LogDate] \
        , convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + '' '' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 1, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 3, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 5, 2)) AS [StartTime] \
            , CASE [sJOBH].[run_status] \
                WHEN 0 THEN ''Failed'' \
                WHEN 1 THEN ''Succeeded'' \
                WHEN 2 THEN ''Retry'' \
                WHEN 3 THEN ''Canceled'' \
                WHEN 4 THEN ''Running'' \
              END AS [Status] \
        , DATEADD(ss,run_duration,convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + '' '' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 1, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 3, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 5, 2))) AS [EndTime] \
            , STUFF( \
                    STUFF(RIGHT(''000000'' + CAST([sJOBH].[run_duration] AS VARCHAR(6)),  6) \
                        , 3, 0, '':'') \
                    , 6, 0, '':'')\
                AS [ElapsedTime] \
            , [sJOBH].[message] AS [Message] \
        FROM [msdb].[dbo].[sysjobs] AS [sJOB] \
        LEFT JOIN ( SELECT [job_id] , [run_date] , [run_time] , [run_status] , [run_duration] , [message] \
                            , ROW_NUMBER() OVER (PARTITION BY [job_id] ORDER BY [run_date] DESC, [run_time] DESC ) AS RowNumber \
                        FROM [msdb].[dbo].[sysjobhistory] \
                        WHERE [step_id] = 0 \
        				           ) AS [sJOBH] \
                ON [sJOB].[job_id] = [sJOBH].[job_id] \
        WHERE [sJOB].job_id = \''%s\'' AND convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + '' '' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 1, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 3, 2) \
        + '':'' + substring(RIGHT(''000000'' + CONVERT(varchar,run_time),6), 5, 2)) > \
        DATEADD(mi,-60,getdate()) ) A ORDER BY [StartTime] \')" %(v_job_id)
    
    result_set = cursor.execute(sql)
    result_list = result_set.fetchall()   
    if result_set.rowcount == 0:
        print('ga ada data broo')
    else:
        """
        root = '\\\\172.24.2.21\\l$\\Backup_log_shipping\\APPROVAL\\' # one specific folder
        #root = 'D:\\Zz1\\*'          # all the subfolders too
        os.chdir(root)
        date_file_list = []
        for folder in glob.glob(root):
            print ("folder =", folder)
            # select the type of file, for instance *.jpg or all files *.*
            for file in glob.glob(folder + '/*.*'):
                stats = os.stat(file)
                lastmod_date = time.localtime(stats[8])
                date_file_tuple = lastmod_date, file
                date_file_list.append(date_file_tuple)
            
        #print date_file_list  # test
        date_file_list.sort()
        date_file_list.reverse()  # newest mod date now first
        """
        #insert Into MONITOR
        server ='172.17.30.77'
        db ='DRMONITORING'
        tcon ='yes'
        usern ='qlik'
        pwd ='P@ssw0rd23'
        monitor = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
        cur = monitor.cursor()
        
        for row in result_list:
            #print('row = %r' % (row,))
            DRSystem    = row[0]
            print(r'DRSystem    : {}'.format(DRSystem))
            ProcessCode = row[1]
            print(r'ProcessCode : {}'.format(ProcessCode))
            Seq         = 'next value for SeqCONBackup_APPROV'
            Scheme      = 'APPROVAL'
            print(r'Scheme      : {}'.format(Scheme))
            v_LogDate   = row[2]
            value_LogDate = re.search('\d{4}\-\d{2}\-\d{2}', str(v_LogDate))
            LogDate     = '{}'.format(value_LogDate.group())
            print(r'LogDate     : {}'.format(LogDate))
            StartTime   = row[3]
            print(r'StartTime   : {}'.format(StartTime))
            timestampStr1 = StartTime.strftime("%Y-%m-%d %H:%M")
            #print (r'timestampStr1', timestampStr1)
            Status      = row[4]
            print(r'Status      : {}'.format(Status))
            EndTime     = row[5]
            print(r'EndTime     : {}'.format(EndTime))
            ElapsedTime = row[6]
            print(r'ElapsedTime : {}'.format(ElapsedTime))
            Message     = row[7]
            print(r'Message     : {}'.format(Message))
            """
            for file in date_file_list:
                # extract just the filename
                folder, FileName = os.path.split(file[1])
                # convert date tuple to MM/DD/YYYY HH:MM:SS format
                file_date = time.strftime("%Y-%m-%d %H:%M", file[0])
                FileSize = os.stat(FileName).st_size/1024
                #print ("%-40s %-18s %.2f" % (file_name, file_date, size))
                if fnmatch.fnmatch(file_date, '%s'%(timestampStr1)):
                    if os.stat(FileName).st_size ==0 :
                        print ("%-40s %-18s %s" % ("No file exist", "Null", "Null"))
                        FileName1 = ''
                        FileSize1 = ''
                    else:
                        #print('-'*33 +'find' + '-'*33)
                        #print ("%-40s %-18s %.2f" % (FileName, file_date, FileSize))
                        FileName1 = FileName
                        FileSize1 = FileSize                       
                        #print(r'FileName    : {}'.format(FileName1))
                        #print(r'FileSize    : {}'.format(FileSize1))
            print(r'FileName    : {}'.format(FileName1))
            print(r'FileSize    : {}'.format(FileSize1))
            print('-'*33 +'find' + '-'*33)
            """
            
            """
            sql_insert = 'insert into [dbo].[Monitoring_SQL] ([DRSystem] ,[ProcessCode] ,[Seq] ,[Scheme], [LogDate], [StartTime], [Status] , [EndTime], [ElapsedTime] , [FileName] , [FileSize] , [Message]) values (\'{}\',\'{}\',{},\'{}\', convert(datetime,\'{}\'), convert(datetime,\'{}\'), \'{}\', convert(datetime,\'{}\'), convert(time,\'{}\'), \'{}\', {}, \'{}\')'.format(DRSystem,ProcessCode,Seq, Scheme, LogDate, StartTime, Status, EndTime, ElapsedTime, FileName1, FileSize1, Message)
            cur.execute(sql_insert)  
            monitor.commit()
            print(r'Inserting To Monitoring : Successfuly')
            """ 
        #monitor.close()
            
except pyodbc.Error as ex:
    print ('error', ex)
finally:
    if cnxn:
        cnxn.close()
