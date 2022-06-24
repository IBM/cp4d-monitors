import requests
import calendar
import time
import re
from lib import cp4d_monitor
from lib import db2
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def main():
    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    #definition of monitor_type
    # Note: should only contain a-z, 0-9 and _ characters
    monitor_type = cp4d_monitor.create_and_validate_type ("cp4d_cognos_task_info")    
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_cp4d_cognos_task_last_status = cp4d_monitor.create_and_validate_type("cp4d_cognos_task_last_status")

    metadata_cognos_task_last_status="cp4d_cognos_task_last_status_success={},cp4d_cognos_task_last_status_duration_in_seconds={},cp4d_cognos_task_last_status_start_epoch_time={}"

    events=[]

    for cognos_analytics_app in cp4d_monitor.get_cognos_analytics_instances():
        cognos_analytic_db_information=cp4d_monitor.get_cognos_analytic_db_information(cognos_analytics_app)

        cp4d_cognos_task_last_status = db2.get_cp4d_cognos_task_last_status(cognos_analytic_db_information)
        
        if cp4d_cognos_task_last_status is None:
            print("No Cognos Analytic Tasks.")
            return 

        if cp4d_cognos_task_last_status['COGIPF_STATUS'].lower() == 'success':
            cognos_task_last_status_success = 1
        else:
            cognos_task_last_status_success = 0

        start_epoch_time=calendar.timegm(time.strptime(str(cp4d_cognos_task_last_status['COGIPF_LOCALTIMESTAMP']).split('.')[0], '%Y-%m-%d %H:%M:%S'))
        task_name=re.findall('jobDefinition\[@name=\'(.*)\'\]',cp4d_cognos_task_last_status['COGIPF_JOBPATH'])
        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_cp4d_cognos_task_last_status, 
                "metadata": metadata_cognos_task_last_status.format
                (cognos_task_last_status_success,
                cp4d_cognos_task_last_status['COGIPF_RUNTIME'], start_epoch_time), 
                "severity": "info", 
                "reference": f"Cognos Task_{cognos_analytics_app['id']}_{task_name[0]}"})       
        ##Only fetch the first cognos analytics instance
        break 

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog
    #print(events)   
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
    main()
