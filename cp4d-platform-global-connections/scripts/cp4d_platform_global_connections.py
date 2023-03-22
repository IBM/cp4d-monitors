import os
import requests
import json
from lib import cp4d_monitor
from kubernetes import client, config, watch
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def main():

    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #definition of monitor_type
    # Note: should only contain a-z, 0-9 and _ characters
    #monitor_type = cp4d_monitor.create_and_validate_type ("cp4d_platform_global_connections")
    monitor_type = "cp4d-platform-global-connections"

    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_number_of_connections = cp4d_monitor.create_and_validate_type ("global_connections_count")
    event_type_valid_connection = cp4d_monitor.create_and_validate_type ("global_connection_valid")
    #Array containing the monitor events
    events = []
    #Create the header section for the requests containing the bearer authentication token   
   
    cp4d_catalog_id = cp4d_monitor.get_asset_catalog_id()
    #Get all available connections    
    cp4d_platform_global_connections_request = cp4d_monitor.get_all_available_connections_response(cp4d_catalog_id)

    cp4d_number_of_global_connections = 0

    if (cp4d_platform_global_connections_request.status_code == 200):
        cp4d_platform_global_connections_response = json.loads (cp4d_platform_global_connections_request.content)

        #Get the number of connections
        cp4d_number_of_global_connections = len(cp4d_platform_global_connections_response["resources"])
        print ("Found {} Global Platform Connections.".format(str(cp4d_number_of_global_connections)))

        #Define metadata
        metadata_number_of_global_connections = "{}={}".format(event_type_number_of_connections, str(cp4d_number_of_global_connections))

        #Define the global connections count event
        data = {"monitor_type":monitor_type, "event_type":event_type_number_of_connections, "metadata": metadata_number_of_global_connections, "severity": "info", "reference": "Cloud Pak for Data Global Connections Count"}

        #Add the event to the list of events
        events.append(data)

    else:
        print ("Get Connections returned status code: {}. Response: {}".format(cp4d_platform_global_connections_request.status_code, cp4d_platform_global_connections_request.text))

        metadata_number_of_global_connections = "{}={}".format(event_type_number_of_connections, str(cp4d_number_of_global_connections))

        #Define the global connections count event
        data = {"monitor_type":monitor_type, "event_type":event_type_number_of_connections, "metadata": metadata_number_of_global_connections, "severity": "warning", "reference": "Cloud Pak for Data Global Connections Count"}

        #Add the event to the list of events
        events.append(data)
        
    if cp4d_number_of_global_connections > 0:

        #Loop through each connection
        for global_connection in cp4d_platform_global_connections_response["resources"]:

            resource_id = global_connection["metadata"]["asset_id"]
            resource_name = global_connection["entity"]["name"]
            print ("Testing Resource {} with asset_id: {}".format(resource_name, resource_id))
           
            cp4d_platform_test_connection_request = cp4d_monitor.test_connection_response(resource_id, cp4d_catalog_id)
            print ("Testing Result code: {}".format(cp4d_platform_test_connection_request.status_code))
            print ("Testing Result content: {}".format(cp4d_platform_test_connection_request.text))

            cp4d_platform_connection_valid = 0
            severity = "info"

            if cp4d_platform_test_connection_request.status_code==200:
                cp4d_platform_connection_valid = 1
            else:
                content = cp4d_platform_test_connection_request.text
                print (content)
                severity = "warning"
            
            metadata_valid_connection = "{}={}".format(event_type_valid_connection, str(cp4d_platform_connection_valid))
            data = {"monitor_type":monitor_type, "event_type":event_type_valid_connection, "metadata": metadata_valid_connection, "severity": severity, "reference": "Global Connection - {}".format(resource_name)}
            events.append(data)

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog    
    #print(events) 
    cp4d_monitor.post_events(events)
    

if __name__ == '__main__':
    main()
