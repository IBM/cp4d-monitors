import requests
from lib import cp4d_monitor
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def main():

    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #definition of monitor_type
    monitor_type="cp4d-wml-deployment-space-info"
    
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_wml_deployment_space_info_overall_count = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_info_overall_count")
    event_type_wml_deployment_space_deployed_count = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_deployed_count")
    event_type_wml_deployment_space_deployed_fail_count = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_deployed_fail_count")
    event_type_wml_deployment_space_deployed_count_online =cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_deployed_count_online")
    event_type_wml_deployment_space_deployed_count_batch = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_deployed_count_batch")
    
    metadata_wml_deployment_space_info_overall_count='cp4d_wml_deployment_space_info_overall_count={}'
    metadata_wml_deployment_space_deployed_count='cp4d_wml_deployment_space_deployed_count={}'
    metadata_wml_deployment_space_deployed_fail_count='cp4d_wml_deployment_space_deployed_fail_count={}'    
    metadata_wml_deployment_space_deployed_count_online = "cp4d_wml_deployment_space_deployed_count_online={}"
    metadata_wml_deployment_space_deployed_count_batch = "cp4d_wml_deployment_space_deployed_count_batch={}"
    #Array containing the monitor events
    events = []

    spaces = cp4d_monitor.get_spaces_list()    
    wml_deployment_space_info_overall_count=0
    for space in spaces:
      wml_deployment_space_deployed_count=0
      wml_deployment_space_deployed_count_online=0
      wml_deployment_space_deployed_fail_count=0
      wml_deployment_space_deployed_count_batch=0
      deployments = cp4d_monitor.get_deployments(space_id=space['metadata']['id'])

      #fix error when no deployment
      if len(deployments) == 0:
        continue
      
      for deployment in deployments['resources']:
          wml_deployment_space_info_overall_count+=1
          wml_deployment_space_deployed_count+=1
          if deployment['entity']['status']['state'] !='ready':
              wml_deployment_space_deployed_fail_count+=1
          if "batch" in deployment['entity']:
              wml_deployment_space_deployed_count_batch+=1
          if "online" in deployment['entity']:
              wml_deployment_space_deployed_count_online+=1          
    
      events.append(
        {
            "monitor_type":monitor_type, 
            "event_type":event_type_wml_deployment_space_deployed_fail_count, 
            "metadata": metadata_wml_deployment_space_deployed_fail_count.format
            (wml_deployment_space_deployed_fail_count), 
            "severity": "info", 
            "reference": space['entity']['name']
        })
      events.append(
        {
            "monitor_type":monitor_type, 
            "event_type":event_type_wml_deployment_space_deployed_count, 
            "metadata": metadata_wml_deployment_space_deployed_count.format
            (wml_deployment_space_deployed_count), 
            "severity": "info", 
            "reference": space['entity']['name']
        })
      events.append(
        {
            "monitor_type":monitor_type, 
            "event_type":event_type_wml_deployment_space_deployed_count_online, 
            "metadata": metadata_wml_deployment_space_deployed_count_online.format
            (wml_deployment_space_deployed_count_online), 
            "severity": "info", 
            "reference": space['entity']['name']
        })
      events.append(
        {
            "monitor_type":monitor_type, 
            "event_type":event_type_wml_deployment_space_deployed_count_batch, 
            "metadata": metadata_wml_deployment_space_deployed_count_batch.format
            (wml_deployment_space_deployed_count_batch), 
            "severity": "info", 
            "reference": space['entity']['name']
        })
    
    events.append(
    {
        "monitor_type":monitor_type, 
        "event_type":event_type_wml_deployment_space_info_overall_count, 
        "metadata": metadata_wml_deployment_space_info_overall_count.format
        (wml_deployment_space_info_overall_count), 
        "severity": "info", 
        "reference":"All Deployment Space"
    })    

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog
    #print(events)   
    cp4d_monitor.post_events (events)

if __name__ == '__main__':
    main()
