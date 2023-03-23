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
    #monitor type should only contain a-z, 0-9 and should start with a-z
    monitor_type="cp4dcognosconnectionsinfo"
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_cp4d_cognos_connections_count = cp4d_monitor.create_and_validate_type("cp4d_cognos_connections_count")

    metadata_cognos_connections_count="cp4d_cognos_connections_count={}"
    events=[]

    for cognos_analytics_app in cp4d_monitor.get_cognos_analytics_instances():
        cognos_analytic_db_information=cp4d_monitor.get_cognos_analytic_db_information(cognos_analytics_app)
        cp4d_cognos_connection_count = db2.get_cp4d_cognos_connections_count(cognos_analytic_db_information)
        
        if cp4d_cognos_connection_count is None:
            cp4d_cognos_connection_count = {}
            cp4d_cognos_connection_count['COUNT']=0

        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_cp4d_cognos_connections_count, 
                "metadata": metadata_cognos_connections_count.format
                (cp4d_cognos_connection_count['COUNT']), 
                "severity": "info", 
                "reference": f"cognos_{cognos_analytics_app['id']}_connections"})       
        ##Only fetch the first cognos analytics instance
        break 

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog
    #print(events)   
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
    main()
