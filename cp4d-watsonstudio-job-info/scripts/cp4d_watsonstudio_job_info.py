from lib import cp4d_monitor
import time
import calendar


def is_active_job(run):
    if run["entity"]["job_run"]["state"] == "Running":
        return True
    else:
        return False

def convert_last_job_result(status):
    if status=='Completed' or status=='CompletedWithWarning' or status=='CompletedWithWarning':
       return 0
    elif status=='Canceled' or status == 'Failed' or status == 'Paused':
       return 1
    else:
       return 2
        

def main():
 
    monitor_type="cp4d-watsonstudio-job-info"
    
    event_type_watsonstudio_jobs_overall_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_overall_count")    
    event_type_watsonstudio_active_jobs_overall_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_active_jobs_overall_count")    
    event_type_watsonstudio_jobs_project_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_project_count")     
    event_type_watsonstudio_active_jobs_project_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_active_jobs_project_count")    
    event_type_watsonstudio_job_last_status=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_last_status")
    
    metadata_watsonstudio_jobs_overall_count="cp4d_watsonstudio_jobs_overall_count={}"    
    metadata_watsonstudio_active_jobs_overall_count= "cp4d_watsonstudio_active_jobs_overall_count={}"    
    metadata_watsonstudio_jobs_project_count="cp4d_watsonstudio_jobs_project_count={}"    
    metadata_watsonstudio_active_jobs_project_count="cp4d_watsonstudio_active_jobs_project_count={}"    
    metadata_watsonstudio_job_last_status="cp4d_watsonstudio_job_last_status_success={},cp4d_watsonstudio_job_last_status_duration_in_seconds={},cp4d_watsonstudio_job_last_start_epoch_time={}"

    events=[]
    projects = cp4d_monitor.get_project_list()
    jobs = cp4d_monitor.get_jobs_list(projects)
    watsonstudio_jobs_overall_count = 0
    watsonstudio_active_jobs_overall_count = 0
 
    for project in projects:
        watsonstudio_active_jobs_project_count=0
        project_total_jobs=0
        project_id=project['metadata']['guid']
        if project_id not in jobs.keys():
            continue
        project_jobs=jobs[project_id]['results']
        if len(project_jobs)==0:
            continue
 
        project_jobs_count=len(project_jobs)
        watsonstudio_jobs_overall_count += project_jobs_count
        project_total_jobs = project_jobs_count

        for job in project_jobs:
            runs=cp4d_monitor.get_job_run_info(project_id=project_id,job_id=job['metadata']['asset_id'])           
            if len(runs)==0:
                continue
            run = runs[0]

            if is_active_job(run):
              watsonstudio_active_jobs_overall_count+=1
              watsonstudio_active_jobs_project_count+=1
            if run['entity']['job_run']['state']=='Running' or run['entity']['job_run']['state']=='None':
                duration_in_seconds=0
            else:              
                duration_in_seconds=run['entity']['job_run']['duration']            
         
            last_start_epoch_time = calendar.timegm(time.strptime(run['entity']['job_run']['last_state_change_timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
            events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_watsonstudio_job_last_status, 
                "metadata": metadata_watsonstudio_job_last_status.format
                (convert_last_job_result(run['entity']['job_run']['state']),
                duration_in_seconds,last_start_epoch_time), 
                "severity": "info", 
                "reference": project['entity']['name']+'_'+job['metadata']['name']})
        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_watsonstudio_active_jobs_project_count, 
                "metadata": metadata_watsonstudio_active_jobs_project_count.format(watsonstudio_active_jobs_project_count), 
                "severity": "info", 
                "reference": project['entity']['name']})
        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_watsonstudio_jobs_project_count, 
                "metadata": metadata_watsonstudio_jobs_project_count.format(project_total_jobs), 
                "severity": "info", 
                "reference": project['entity']['name']})
    events.append({
            "monitor_type":monitor_type, 
            "event_type":event_type_watsonstudio_active_jobs_overall_count, 
            "metadata": metadata_watsonstudio_active_jobs_overall_count.format(watsonstudio_active_jobs_overall_count), 
            "severity": "info", 
            "reference": "All Watson Studio Projects"})
    events.append({
            "monitor_type":monitor_type, 
            "event_type":event_type_watsonstudio_jobs_overall_count, 
            "metadata": metadata_watsonstudio_jobs_overall_count.format(watsonstudio_jobs_overall_count), 
            "severity": "info", 
            "reference": "All Watson Studio Projects"})
    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog  
    #print(events)
    cp4d_monitor.post_events(events)


if __name__ == '__main__':
    main()