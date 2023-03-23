import os
import requests
import json
from lib import cp4d_monitor
from kubernetes import client, config, watch
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def convert_cpu_unit(cpu):
  if 'm' not in cpu:
    return int(cpu) * 1000
  return int(cpu[0:-1])

def convert_memory_unit(memory):
    if "Ki" in memory:
       return int(memory[0:-2])/1024/1024
    if "Gi" in memory:
       return int(memory[0:-2])
    if "Mi" in memory:
       return int(memory[0:-2])/1024
    return int(memory)

def main():  
    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #definition of monitor_type
    #monitor type should only contain a-z, 0-9 and should start with a-z
    monitor_type="cp4dwatsonstudioruntimeusage"
    
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_watsonstudio_runtime_usage_total_count=  cp4d_monitor.create_and_validate_type ("cp4d_watsonstudio_runtime_usage_total_count")
    event_type_watsonstudio_runtime_usage_project_count = cp4d_monitor.create_and_validate_type('cp4d_watsonstudio_runtime_usage_project_count')
    event_type_watsonstudio_runtime_usage_project_cpu = cp4d_monitor.create_and_validate_type('cp4d_watsonstudio_runtime_usage_project_cpu')
    event_type_watsonstudio_runtime_usage_project_memory= cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_runtime_usage_project_memory")
    event_type_watsonstudio_runtime_usage_cpu = cp4d_monitor.create_and_validate_type ("cp4d_watsonstudio_runtime_usage_cpu")
    event_type_watsonstudio_runtime_usage_memory = cp4d_monitor.create_and_validate_type ("cp4d_watsonstudio_runtime_usage_memory")
    
    metadata_watsonstudio_runtime_usage_project_count = 'cp4d_watsonstudio_runtime_usage_project_count={}'
    metadata_watsonstudio_runtime_usage_project_cpu="cp4d_watsonstudio_runtime_usage_project_cpu_limit={},cp4d_watsonstudio_runtime_usage_project_cpu_requests={},cp4d_watsonstudio_runtime_usage_project_cpu_utilization={}"
    metadata_watsonstudio_runtime_usage_project_memory="cp4d_watsonstudio_runtime_usage_project_memory_limit={},cp4d_watsonstudio_runtime_usage_project_memory_requests={},cp4d_watsonstudio_runtime_usage_project_memory_utilization={}"
    metadata_watsonstudio_runtime_usage_total_count ='cp4d_watsonstudio_runtime_usage_total_count={}'
    metadata_watsonstudio_runtime_usage_cpu='cp4d_watsonstudio_runtime_usage_cpu_limit={},cp4d_watsonstudio_runtime_usage_cpu_requests={},cp4d_watsonstudio_runtime_usage_cpu_utilization={}'
    metadata_watsonstudio_runtime_usage_memory='cp4d_watsonstudio_runtime_usage_memory_limit={},cp4d_watsonstudio_runtime_usage_memory_requests={},cp4d_watsonstudio_runtime_usage_memory_utilization={}'
    #Array containing the monitor events
    events = []
    
    #get project ids
    projects = cp4d_monitor.get_project_list()
    total_runtime=0
    events=[]
    for project in projects:
      project_total_runtime=0
      project_total_cpu_limits=0
      project_total_memory_limits=0
      project_total_cpu_requests=0
      project_total_memory_requests=0
      project_total_memory_usage=0
      project_total_cpu_usage=0

      labels='icpdsupport/projectId={},runtime=true'.format(project['metadata']['guid'])
      pods = cp4d_monitor.get_pod_usage(label_selector=labels)

      app_labels='dsxProjectId={}'.format(project['metadata']['guid'])      
      deployments = cp4d_monitor.get_deployment(label_selector=app_labels)  

      if len(pods)>0:
         total_runtime+=1
         for pod in pods:

           project_total_runtime=+1
           key_deployment=pod['metadata']['name'][0:-14]
           deployment_resources=deployments[key_deployment].spec.template.spec.containers[0].resources           
           pod_cpu_usage=convert_cpu_unit(pod['containers'][1]['usage']['cpu'])          
           pod_cpu_limits=convert_cpu_unit(deployment_resources.limits['cpu'])
           pod_cpu_requests=convert_cpu_unit(deployment_resources.requests['cpu'])           
           pod_memory_limits=convert_memory_unit(deployment_resources.limits['memory'])          
           pod_memory_requests=convert_memory_unit(deployment_resources.requests['memory'])           
           pod_memory_usage=convert_memory_unit(pod['containers'][1]['usage']['memory'])

           project_total_cpu_limits+=pod_cpu_limits
           project_total_memory_limits+=pod_memory_limits
           project_total_cpu_requests+=pod_cpu_requests
           project_total_memory_requests+=pod_memory_requests
           project_total_memory_usage+=pod_memory_usage
           project_total_cpu_usage+=project_total_cpu_usage
          
           key_deployment=pod['metadata']['name'][0:-14]
           deployment_resources =deployments[key_deployment].spec.template.spec.containers[0].resources
           events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_runtime_usage_cpu, 
                          "metadata": metadata_watsonstudio_runtime_usage_cpu.format(pod_cpu_limits,pod_cpu_requests,pod_cpu_usage), 
                          "severity": "info", 
                          "reference": project['entity']['name']+'_'+pod['metadata']['name']})
           events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_runtime_usage_memory, 
                          "metadata": metadata_watsonstudio_runtime_usage_memory.format(pod_memory_limits,pod_memory_requests,pod_memory_usage), 
                          "severity": "info", 
                          "reference": project['entity']['name']+'_'+pod['metadata']['name']})
         
         events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_runtime_usage_project_count, 
                          "metadata": metadata_watsonstudio_runtime_usage_project_count.format(project_total_runtime), 
                          "severity": "info", 
                          "reference": project['entity']['name']})
         events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_runtime_usage_project_cpu, 
                          "metadata": metadata_watsonstudio_runtime_usage_project_cpu.format(project_total_cpu_limits,project_total_memory_requests,project_total_cpu_usage), 
                          "severity": "info", 
                          "reference": project['entity']['name']})
         events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_runtime_usage_project_memory, 
                          "metadata": metadata_watsonstudio_runtime_usage_project_memory.format(project_total_memory_limits,project_total_memory_requests,project_total_memory_usage), 
                          "severity": "info", 
                          "reference": project['entity']['name']})
      events.append({"monitor_type":monitor_type, 
                           "event_type":event_type_watsonstudio_runtime_usage_total_count, 
                           "metadata": metadata_watsonstudio_runtime_usage_total_count.format(total_runtime), 
                           "severity": "info", 
                           "reference": project['entity']['name']})

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog     
    #print(events)
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
   main()