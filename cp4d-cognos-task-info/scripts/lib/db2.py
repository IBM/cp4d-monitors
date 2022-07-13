import ibm_db
from lib import k8s
from lib import cp4d_monitor


def get_cp4d_cognos_task_last_status(cognos_analytic_db_information):

    cp4d_cognos_task_last_status_sql ="select COGIPF_JOBPATH, COGIPF_STATUS, COGIPF_LOCALTIMESTAMP,COGIPF_RUNTIME from COGIPF_RUNJOB order by COGIPF_LOCALTIMESTAMP desc FETCH FIRST 1 ROWS ONLY;"   

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
        stmt = ibm_db.exec_immediate(conn, cp4d_cognos_task_last_status_sql)        
        result = ibm_db.fetch_assoc(stmt)
        if result == False:
            print("There are no rows left in the result set.")
            return None
    except Exception as ex:
        print(f"Error querying cognos task last status - {ex}")
        exit(1)
    finally:
        if ibm_db.active(conn):
            ibm_db.close(conn)

    return result

