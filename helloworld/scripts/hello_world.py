import os
import requests
import json
from kubernetes import client, config, watch


def main():
    # setup the namespace
    ns = os.environ.get('ICPD_CONTROLPLANE_NAMESPACE')
    if ns is None:
        ns = ""
    monitor_type = "helloworld"
    event_type = "hello_world_status"

    # configure client 
    config.load_incluster_config()
    api = client.CoreV1Api()

    # configure post request and set secret headers
    url = 'https://zen-watchdog-svc:4444/zen-watchdog/v1/monitoring/events'
    with open('/var/run/sharedsecrets/token', 'r') as file:
        secret_header = file.read().replace('\n', '')
    headers = {'Content-type': 'application/json', 'secret': secret_header}

    #build the events array
    events = []
    # When constructing events, the following items are mandatory:
    # - monitor_type
    # - event_type
    # - metadata (note the metadata must match the long_description of the event_types array in the custom monitor extension config map)
    # - severity
    # - reference
    metadata = "Available=1"  
    data = {"monitor_type":monitor_type, "event_type":event_type, "metadata": metadata, "hello_world":"1", "severity": "info", "reference": "helloworld"}

    events.append(data)
    json_string = json.dumps(events)
    
    # post call to zen-watchdog to record events
    r = requests.post(url, headers=headers, data=json_string, verify=False)
    #print the results
    print(r.status_code)
    print(r.text)
    
if __name__ == '__main__':
    main()
