from lib import cp4d_monitor
import calendar
import time


def main():
    
    monitor_type = cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_schedule_info")

    event_type_watsonstudio_jobs_schedule_overall_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_schedule_overall_count")    
    event_type_watsonstudio_jobs_schedule_project_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_schedule_project_count")    
    event_type_watsonstudio_jobs_schedule_user_overall_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_schedule_user_overall_count")     
    event_type_watsonstudio_job_schedule_last_run_fail=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_schedule_last_run_fail")
    event_type_watsonstudio_job_schedule_next_run_epoch_time=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_schedule_next_run_epoch_time")
    event_type_watsonstudio_job_schedule_last_run_duration_seconds=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_schedule_last_run_duration_seconds")
    event_type_watsonstudio_job_schedule_last_run_epoch_time=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_job_schedule_last_run_epoch_time")
    event_type_watsonstudio_jobs_schedule_user_notebook_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_schedule_user_notebook_count")
    event_type_watsonstudio_jobs_schedule_user_datastage_count=cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_jobs_schedule_user_datastage_count")
    
    metadata_watsonstudio_jobs_schedule_overall_count="cp4d_watsonstudio_jobs_schedule_overall_count={}"    
    metadata_watsonstudio_jobs_schedule_project_count= "cp4d_watsonstudio_jobs_schedule_project_count={}"    
    metadata_watsonstudio_jobs_schedule_user_overall_count="cp4d_watsonstudio_jobs_schedule_user_overall_count={}"    
    metadata_watsonstudio_job_schedule_last_run_fail="cp4d_watsonstudio_job_schedule_last_run_fail=1,cp4d_watsonstudio_job_schedule_last_start_epoch_time={}"
    metadata_watsonstudio_jobs_schedule_next_run_epoch_time="cp4d_watsonstudio_jobs_schedule_next_run_epoch_time={}"
    metadata_watsonstudio_job_schedule_last_run_duration_seconds="cp4d_watsonstudio_job_schedule_last_run_duration_seconds={}"
    metadata_watsonstudio_job_schedule_last_run_epoch_time="cp4d_watsonstudio_job_schedule_last_run_epoch_time={}"
    metadata_watsonstudio_jobs_schedule_user_notebook_count="cp4d_watsonstudio_jobs_schedule_user_notebook_count={}"
    metadata_watsonstudio_jobs_schedule_user_datastage_count="cp4d_watsonstudio_jobs_schedule_user_datastage_count={}"
    #get project ids
    events=[]
    projects = cp4d_monitor.get_project_list()
    jobs = cp4d_monitor.get_jobs_list(projects)
    users = cp4d_monitor.get_all_users()
    watsonstudio_jobs_schedule_overall_count = 0
    watsonstudio_jobs_schedule_user_count={}
    watsonstudio_jobs_schedule_user_notebook_count={}
    watsonstudio_jobs_schedule_user_datastage_count={}
    projects_names = {}
    for project in projects:
        watsonstudio_jobs_schedule_project_count=0
        #get the job schedule information per project
        jobs_info=cp4d_monitor.get_jobs_info(project['metadata']['guid'])
        project_id=project['metadata']['guid']
        projects_names[project_id] = project['entity']['name']
        if project_id not in jobs.keys():
            continue
        project_jobs=jobs[project_id]['results']
        if len(project_jobs)==0:
            continue
        for job in project_jobs:
          if 'schedule'in job['entity']['job']:
              watsonstudio_jobs_schedule_overall_count+=1
              watsonstudio_jobs_schedule_project_count+=1

              if job['entity']['job']['asset_ref_type']=='notebook':
                if project_id in watsonstudio_jobs_schedule_user_notebook_count and job['metadata']['owner_id'] in watsonstudio_jobs_schedule_user_notebook_count[project_id]:
                    watsonstudio_jobs_schedule_user_notebook_count[project_id][job['metadata']['owner_id']]+=1
                else:
                    if project_id in watsonstudio_jobs_schedule_user_notebook_count:
                        watsonstudio_jobs_schedule_user_notebook_count[project_id][job['metadata']['owner_id']]=1
                    else:
                        watsonstudio_jobs_schedule_user_notebook_count[project_id] = {}
                        watsonstudio_jobs_schedule_user_notebook_count[project_id][job['metadata']['owner_id']]=1
            
              if job['entity']['job']['asset_ref_type']=='data_intg_flow':
                if project_id in watsonstudio_jobs_schedule_user_datastage_count and job['metadata']['owner_id'] in watsonstudio_jobs_schedule_user_datastage_count[project_id]:
                    watsonstudio_jobs_schedule_user_datastage_count[project_id][job['metadata']['owner_id']]+=1
                else:
                    if project_id in watsonstudio_jobs_schedule_user_datastage_count:
                        watsonstudio_jobs_schedule_user_datastage_count[project_id][job['metadata']['owner_id']]=1
                    else:
                        watsonstudio_jobs_schedule_user_datastage_count[project_id] = {}
                        watsonstudio_jobs_schedule_user_datastage_count[project_id][job['metadata']['owner_id']]=1
              
              if job['metadata']['owner_id'] in watsonstudio_jobs_schedule_user_count:
                watsonstudio_jobs_schedule_user_count[job['metadata']['owner_id']]+=1
              else:
                watsonstudio_jobs_schedule_user_count[job['metadata']['owner_id']]=1
              
              if job['entity']['job']['last_run_status']=='Failed':
                 events.append({
                        "monitor_type":monitor_type, 
                        "event_type":event_type_watsonstudio_job_schedule_last_run_fail, 
                        "metadata": metadata_watsonstudio_job_schedule_last_run_fail.format
                        (job['entity']['job']['last_run_status_timestamp']), 
                        "severity": "info", 
                        "reference": project['entity']['name']+'_'+job['metadata']['name']})

              job_id = job['metadata']['asset_id']
              job_info = cp4d_monitor.get_job_info(jobs_info, job_id)

              #need to discuss and modify
              if job_info is not None and 'schedule_info' in job_info['entity']['job']:
                if 'startOn' in job_info['entity']['job']['schedule_info']:
                    nextrun_in_epoch_time=cp4d_monitor.calculate_next_schedule_run(job_info['entity']['job']['schedule_info']['startOn'], job_info['entity']['job']['schedule'])
                    if ('endOn' not in job_info['entity']['job']['schedule_info']) or ('endOn' in job_info['entity']['job']['schedule_info'] and nextrun_in_epoch_time*1000<=job_info['entity']['job']['schedule_info']['endOn']): 
                        events.append({
                            "monitor_type":monitor_type, 
                            "event_type":event_type_watsonstudio_job_schedule_next_run_epoch_time, 
                            "metadata": metadata_watsonstudio_jobs_schedule_next_run_epoch_time.format
                            (nextrun_in_epoch_time), 
                            "severity": "info", 
                            "reference": project['entity']['name']+'_'+job['metadata']['name']})
                elif 'future_scheduled_runs' in job_info['entity']['job']:
                    future_scheduled_runs=len(job_info['entity']['job']['future_scheduled_runs'])
                    print("Found {} future_scheduled_runs".format(future_scheduled_runs))
                    if future_scheduled_runs > 0:
                        next_future_scheduled_run=job_info['entity']['job']['future_scheduled_runs'][0]
                        nextrun_in_epoch_time=cp4d_monitor.calculate_next_schedule_run_in_epoch(next_future_scheduled_run)
                        events.append({
                            "monitor_type":monitor_type, 
                            "event_type":event_type_watsonstudio_job_schedule_next_run_epoch_time, 
                            "metadata": metadata_watsonstudio_jobs_schedule_next_run_epoch_time.format
                            (nextrun_in_epoch_time), 
                            "severity": "info", 
                            "reference": project['entity']['name']+'_'+job['metadata']['name']})                        

              runs=cp4d_monitor.get_job_run_info(project_id=project_id,job_id=job['metadata']['asset_id'])
              if len(runs)>0: 
                if job['metadata']['asset_id'] == runs[0]['entity']['job_run']['job_ref'] and runs[0]['entity']['job_run']['isScheduledRun'] == True:
                    if 'duration' in runs[0]['entity']['job_run']:
                        events.append({
                                    "monitor_type":monitor_type, 
                                    "event_type":event_type_watsonstudio_job_schedule_last_run_duration_seconds, 
                                    "metadata": metadata_watsonstudio_job_schedule_last_run_duration_seconds.format
                                    (runs[0]['entity']['job_run']['duration']), 
                                    "severity": "info", 
                                    "reference": project['entity']['name']+'_'+job['metadata']['name']})   
                    if 'last_state_change_timestamp' in runs[0]['entity']['job_run']:
                        last_run_epoch_time= calendar.timegm(time.strptime(runs[0]['entity']['job_run']['last_state_change_timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
                        events.append({
                                    "monitor_type":monitor_type, 
                                    "event_type":event_type_watsonstudio_job_schedule_last_run_epoch_time, 
                                    "metadata": metadata_watsonstudio_job_schedule_last_run_epoch_time.format
                                    (last_run_epoch_time), 
                                    "severity": "info", 
                                    "reference": project['entity']['name']+'_'+job['metadata']['name']})

        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_watsonstudio_jobs_schedule_project_count, 
                "metadata": metadata_watsonstudio_jobs_schedule_project_count.format(watsonstudio_jobs_schedule_project_count), 
                "severity": "info", 
                "reference": project['entity']['name']})
   
    for k, v in watsonstudio_jobs_schedule_user_count.items():
        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_watsonstudio_jobs_schedule_user_overall_count, 
                "metadata": metadata_watsonstudio_jobs_schedule_user_overall_count.format(v), 
                "severity": "info", 
                "reference": users[k]['displayName']})
               
    for project_id, _ in watsonstudio_jobs_schedule_user_notebook_count.items():
        for k, v in watsonstudio_jobs_schedule_user_notebook_count[project_id].items():    
            events.append({
                    "monitor_type":monitor_type, 
                    "event_type":event_type_watsonstudio_jobs_schedule_user_notebook_count, 
                    "metadata": metadata_watsonstudio_jobs_schedule_user_notebook_count.format(watsonstudio_jobs_schedule_overall_count), 
                    "severity": "info", 
                    "reference": projects_names[project_id]+'_'+users[k]['displayName']+'-notebook'})
    
    for project_id, _ in watsonstudio_jobs_schedule_user_datastage_count.items():
        for k, v in watsonstudio_jobs_schedule_user_datastage_count[project_id].items():        
            events.append({
                    "monitor_type":monitor_type, 
                    "event_type":event_type_watsonstudio_jobs_schedule_user_datastage_count, 
                    "metadata": metadata_watsonstudio_jobs_schedule_user_datastage_count.format(watsonstudio_jobs_schedule_overall_count), 
                    "severity": "info", 
                    "reference": projects_names[project_id]+'_'+users[k]['displayName']+'-datastage'})
    
    events.append({
            "monitor_type":monitor_type, 
            "event_type":event_type_watsonstudio_jobs_schedule_overall_count, 
            "metadata": metadata_watsonstudio_jobs_schedule_overall_count.format(watsonstudio_jobs_schedule_overall_count), 
            "severity": "info", 
            "reference": "All Watson Studio Projects"})
    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog    
    #print(events) 
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
    main()