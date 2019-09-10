--ACA
=========================================================================
--Connection:
sqlplus USER_DEMO/oracle

--User:
show user;

SELECT * FROM dba_sys_privs WHERE grantee IN (&user_role, 'PUBLIC');

SELECT grantee, owner||'.'||table_name object, privilege, grantable 
FROM dba_tab_privs WHERE grantee IN (&user_role)
ORDER BY grantee, owner||'.'||table_name, privilege;

select owner from all_objects where object_type in ('TABLE','VIEW')
and object_name = 'USER_DEMO.aca_table';



col table_name for a15
col owner for a10
select table_name, owner from dba_tables where owner='USER_DEMO';
=========================================================================
drop table USER_DEMO.TABLE_PROSES PURGE;
drop table USER_DEMO.TRANSAKSI_ACA PURGE; 

TRUNCATE TABLE [schema_name.]table_name
[ PRESERVE MATERIALIZED VIEW LOG | PURGE MATERIALIZED VIEW LOG ]
  [ DROP STORAGE | REUSE STORAGE ] ;
  
TRUNCATE TABLE USER_DEMO.MONITORING REUSE STORAGE;
=========================================================================
CREATE TABLE USER_DEMO.aca_table (
    acaID varchar(255) NOT NULL,
    start_time varchar2(255) not null,
    status varchar2(255) not null,
    end_time varchar2(255) not null,
	elapsed varchar2(255) not null,
    file_name varchar2(255) not null,
    file_size varchar2(255) not null,
    Message varchar2(255),
    CONSTRAINT PK_aca_table PRIMARY KEY (acaID)
);

desc USER_DEMO.aca_table;

ALTER TABLE USER_DEMO.TABLE_ACA ADD elapsed time;

alter table USER_DEMO.MONITORING MODIFY ELAPSEDTIME VARCHAR2(30);

  
CREATE TABLE USER_DEMO.Monitoring(       
	   DRSystem varchar2(50) NULL,
       ProcessCode varchar2(5) NULL,
       Seq number(10) NULL,
       Scheme varchar2(59) NULL,
       StartTime varchar2(30) NULL,
       Status varchar2(50) NULL,
       EndTime varchar2(30) NULL,
       ElapsedTime VARCHAR2(10) NULL,
       FileName varchar2(50) NULL,
       FileSize VARCHAR2(50) NULL,
       Message varchar(250) NULL
);

'insert into USER_DEMO.Monitoring VALUES(\'ACA\',\'B\',1,\'pdbaca02\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'NULL\')'.format(start_time,status,end_time,elapsed_time,file_name,total_size)


SET LINESIZE 200
col DRSystem for a8
col ProcessCode for a11
COL seq for a3
col Scheme for a20
COL StartTime for a24
COL Status for a22
COL EndTime for a24
COL ElapsedTime for a8
COL FileName for a25
COL FileSize for a8
COL Message for a10

SELECT * FROM USER_DEMO.MONITORING;

=========================================================================
begin
   for i in 1 .. 20
   loop
		insert into USER_DEMO.aca_table values ( 'AB0'||i, 'Mon Aug 5 00:22:04 2019', 'successfully completed','Mon Aug 5 01:42:48 2019','abc','100Mb','aaaa', '01:20:42');
   end loop;
commit;
end;
/

if (i=0) OR (i>=1) then
	i:=i+1;
	insert into USER_DEMO.aca_table(acaID,start_time, status, end_time, file_name, file_size, Message) 
	values('AB0'||i, Mon Aug 5 00:22:04 2019,value,value);
endif	

===================================================================================================
v$log_history
set linesize 200
col RECID for a3
col STAMP for a10
col THREAD# for a15
col SEQUENCE# for a5
col FIRST_CHANGE# for a15
col FIRST_TIME for a15
col NEXT_CHANGE# for a15
col RESETLOGS_CHANGE# for a10
col RESETLOGS_TIME for a10