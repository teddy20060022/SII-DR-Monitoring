# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:10:24 2019

@author: Muhammad Tedi Sopyan
"""

######confins#####
import pyodbc 
try:
    """server ='172.16.2.200'
    db ='DRMON'
    tcon ='yes'
    usern ='sa'
    pwd ='Pa55w.rd'
    """
    cnxn = pyodbc.connect('DSN=TEST;UID=sa;PWD=Pa55w.rd')
    #cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
    #sql = 'SELECT @@version'
    cursor = cnxn.cursor()
    #cursor.execute(sql)
    sql = " select A.[DRSystem] ,A.[ProcessCode] ,[Scheme] ,A.[LogDate] ,[StartTime] ,[Status] ,[EndTime] ,[ElapsedTime] ,[FileName] ,[FileSize] ,[Message] \
         		from (SELECT 'CON' AS [DRSystem] \
                	, 'B' AS [ProcessCode] \
                	, ROW_NUMBER() OVER (PARTITION BY [sJOB].[job_id] ORDER BY [run_date], [run_time] ) AS [Seq] \
                	, SUBSTRING(name,16,100) [Scheme] \
        , (select \
        CASE when convert(time,getdate()) > convert(time,'08:00:00') then convert(datetime,convert(date,getdate())) \
        else \
        convert(datetime,convert(date,getdate()-1)) \
        end) AS [LogDate] \
        , convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + ' ' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 1, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 3, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 5, 2)) AS [StartTime] \
            , CASE [sJOBH].[run_status] \
                WHEN 0 THEN 'Failed' \
                WHEN 1 THEN 'Succeeded' \
                WHEN 2 THEN 'Retry' \
                WHEN 3 THEN 'Canceled' \
                WHEN 4 THEN 'Running' \
              END AS [Status] \
        , DATEADD(ss,run_duration,convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + ' ' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 1, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 3, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 5, 2))) AS [EndTime] \
            , STUFF( \
                    STUFF(RIGHT('000000' + CAST([sJOBH].[run_duration] AS VARCHAR(6)),  6) \
                        , 3, 0, ':') \
                    , 6, 0, ':')\
                AS [ElapsedTime] \
        	, NULL [FileName] \
        	, 999 [FileSize] \
            , [sJOBH].[message] AS [Message] \
        FROM [msdb].[dbo].[sysjobs] AS [sJOB] \
        LEFT JOIN ( SELECT [job_id] , [run_date] , [run_time] , [run_status] , [run_duration] , [message] \
                            , ROW_NUMBER() OVER (PARTITION BY [job_id] ORDER BY [run_date] DESC, [run_time] DESC ) AS RowNumber \
                        FROM [msdb].[dbo].[sysjobhistory] \
                        WHERE [step_id] = 0 \
        				           ) AS [sJOBH] \
                ON [sJOB].[job_id] = [sJOBH].[job_id] \
        WHERE [sJOB].job_id in ( \
        select [MJob].job_id from [Master_Job_ID] AS [MJob]\
        WHERE [MJob].[DRSystem] = 'CON' AND [MJob].ProcessCode = 'R' \
        	AND [MJob].Scheme = 'APPROV' ) \
        	AND convert(datetime,convert(varchar, convert(datetime, CONVERT(varchar,run_date)), 111) \
        + ' ' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 1, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 3, 2) \
        + ':' + substring(RIGHT('000000' + CONVERT(varchar,run_time),6), 5, 2)) > \
        DATEADD(mi,-60,getdate()) ) A"
    
    result_set = cursor.execute(sql)
    result_list = result_set.fetchall()
    
    
    if result_set.rowcount == 0:
        print('ga ada data broo')
    else:
        #insert Into MONITOR
        
        server ='172.17.30.77'
        db ='DRMONITORING'
        tcon ='yes'
        usern ='qlik'
        pwd ='P@ssw0rd23'
        monitor = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+db+';UID='+usern+';PWD='+pwd+'')
        cur = cnxn.cursor()
        
        for row in result_list:
            print('row = %r' % (row,))
            DRSystem    = row[0]
            ProcessCode = row[1]
            Scheme      = row[2]
            LogDate     = row[3]
            StartTime   = row[4]
            Status      = row[5]
            EndTime     = row[6]
            ElapsedTime = row[7]
            FileName    = row[8]
            FileSize    = row[9]
            Message     = row[10]
            Seq         = 'next value for SeqCONBackup_LBPP'
            
            print(r'DRSystem    : {}'.format(DRSystem))
            print(r'ProcessCode : {}'.format(ProcessCode))
            print(r'Scheme      : {}'.format(Scheme))
            print(r'LogDate     : {}'.format(LogDate))
            print(r'StartTime   : {}'.format(StartTime))
            print(r'Status      : {}'.format(Status))
            print(r'EndTime     : {}'.format(EndTime))
            print(r'ElapsedTime : {}'.format(ElapsedTime))
            print(r'FileName    : {}'.format(FileName))
            print(r'FileSize    : {}'.format(FileSize))
            print(r'Message     : {}'.format(Message))
                        
            #INSERT into [dbo].[Monitoring_SQL]
            #([DRSystem] ,[ProcessCode] ,[Seq] ,[Scheme] ,[LogDate],[StartTime],[Status] ,[EndTime] ,[ElapsedTime],[FileName],[FileSize] ,[Message])
            #.format(DRSystem ,ProcessCode ,Seq ,Scheme ,LogDate, StartTime, Status , EndTime , ElapsedTime, FileName , FileSize, Message )
            sql_insert = 'INSERT into [dbo].[Monitoring_SQL] VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\' )'.format(DRSystem ,ProcessCode ,Seq ,Scheme ,LogDate, StartTime, Status , EndTime , ElapsedTime, FileName , FileSize, Message )
            cur.execute(sql_insert)  
            monitor.commit()
            print(r'Inserting To Monitoring : Successfuly')
        
        #monitor.close()
            
except pyodbc.Error as ex:
    print ('error', ex)
finally:
    if cnxn:
        cnxn.close()
    
