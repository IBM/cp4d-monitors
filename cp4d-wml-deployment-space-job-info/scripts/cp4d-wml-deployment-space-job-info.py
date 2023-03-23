import requests
from lib import cp4d_monitor
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import calendar

def convert_last_job_result(status):
    if status=='Completed' or status=='CompletedWithWarning' or status=='CompletedWithWarning':
       return 0
    elif status=='Canceled' or status == 'Failed' or status == 'Paused':
       return 1
    else:
       return 2
   
def is_active_job(run):
    if run["entity"]["job_run"]["state"] == "Running":
        return True
    else:
        return False


def main():

    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #definition of monitor_type
    #monitor type should only contain a-z, 0-9 and should start with a-z
    monitor_type="cp4dwmldeploymentspacejobinfo"
    
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_wml_deployment_space_jobs_overall_count = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_jobs_overall_count")
    event_type_wml_deployment_space_jobs_active_count = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_jobs_active_count")
    event_type_wml_deployment_space_job_last_status = cp4d_monitor.create_and_validate_type("cp4d_wml_deployment_space_job_last_status")
     
    metadata_wml_deployment_space_jobs_overall_count='cp4d_wml_deployment_space_jobs_overall_count={}'
    metadata_wml_deployment_space_jobs_active_count='cp4d_wml_deployment_space_jobs_active_count={}'
    metadata_wml_deployment_space_job_last_status='cp4d_wml_deployment_space_job_last_status_success={},cp4d_wml_deployment_space_job_last_status_duration_in_seconds={},cp4d_wml_deployment_space_job_last_start_epoch_time={}'    

    #Array containing the monitor events
    events = []
    spaces = cp4d_monitor.get_spaces_list()    
    wml_deployment_space_jobs_overall_count=0
    
    for space in spaces:
        wml_deployment_space_jobs_active_count=0
        jobs = cp4d_monitor.get_deployment_jobs(space_id=space['metadata']['id'])
        if len(jobs['results'])==0:
           continue
        for job in jobs['results']:
          wml_deployment_space_jobs_overall_count+=1
          runs=cp4d_monitor.get_space_job_runs(space_id=space['metadata']['id'],job_id=job['metadata']['asset_id'])      
          if len(runs)==0:
            continue
          run = runs[0]
          if is_active_job(run):
             wml_deployment_space_jobs_active_count+=1
          if run['entity']['job_run']['state']=='Running' or run['entity']['job_run']['state']=='None':
                duration_in_seconds=0
          else:              
                duration_in_seconds=run['entity']['job_run']['duration']
          last_start_epoch_time = calendar.timegm(time.strptime(run['entity']['job_run']['last_state_change_timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
          events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_wml_deployment_space_job_last_status, 
                "metadata": metadata_wml_deployment_space_job_last_status.format
                (convert_last_job_result(run['entity']['job_run']['state']),
                duration_in_seconds,last_start_epoch_time), 
                "severity": "info", 
                "reference": space['entity']['name']+'_'+job['metadata']['name']})
        events.append({
            "monitor_type":monitor_type, 
            "event_type":event_type_wml_deployment_space_jobs_active_count, 
            "metadata": metadata_wml_deployment_space_jobs_active_count.format
            (wml_deployment_space_jobs_active_count), 
            "severity": "info", 
            "reference": space['entity']['name']
        })

    
    events.append({
        "monitor_type":monitor_type, 
        "event_type":event_type_wml_deployment_space_jobs_overall_count, 
        "metadata": metadata_wml_deployment_space_jobs_overall_count.format
        (wml_deployment_space_jobs_overall_count), 
        "severity": "info", 
        "reference":"All Deployment Space"
    })    

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog
    #print(events)   
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
    main()
