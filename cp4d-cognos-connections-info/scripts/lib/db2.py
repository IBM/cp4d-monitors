import ibm_db
from lib import k8s
from lib import cp4d_monitor

def get_cp4d_cognos_connections_count(cognos_analytic_db_information):
    cp4d_cognos_connections_count_sql='''select count(*) as COUNT FROM CMOBJPROPS52 dconns
inner join CMOBJNAMES objnm on
dconns.CMID=objnm.CMID
inner join
(
select dconns.CMID, cmobj.CLASSID, cmobj.PCMID, objnm.NAME from
CMOBJPROPS52 dconns inner join CMOBJECTS cmobj
on dconns.CMID=cmobj.CMID and cmobj.CLASSID=9
inner join CMOBJNAMES objnm
on cmobj.PCMID=objnm.CMID) DataSources
on Datasources.CMID=dconns.CMID'''

    dsn = ("HOSTNAME={0};"
        "PORT={1};"
        "PROTOCOL={2};"
        "DATABASE={3};"
        "UID={4};"
        "PWD={5};"
        ).format(
        cognos_analytic_db_information[cp4d_monitor.cognos_analytic_db_host], 
        cognos_analytic_db_information[cp4d_monitor.cognos_analytic_db_port], 
        "TCPIP",
        cognos_analytic_db_information[cp4d_monitor.cognos_analytic_db_name], 
        cognos_analytic_db_information[cp4d_monitor.cognos_analytic_db_username], 
        cognos_analytic_db_information[cp4d_monitor.cognos_analytic_db_password])
    conn = ibm_db.connect(dsn, "", "")
    try:
        stmt = ibm_db.exec_immediate(conn, cp4d_cognos_connections_count_sql)        
        result = ibm_db.fetch_assoc(stmt)
        if result == False:
            print("There are no rows left in the result set.")
            return None
    except Exception as ex:
        print(f"Error querying cognos connection count - {ex}")
        exit(1)
    finally:
        if ibm_db.active(conn):
            ibm_db.close(conn)

    return result



