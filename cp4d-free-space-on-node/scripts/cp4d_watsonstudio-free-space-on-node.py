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
       return  int(memory[0:-2])/1024
    return memory

def main():  
    #surpress warning on insecure SSL certificate
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    #definition of monitor_type
    # Note: should only contain a-z, 0-9 and _ characters
    monitor_type = cp4d_monitor.create_and_validate_type("cp4d_watsonstudio_max_space")
    
    #Definition of event_types
    # Note: should only contain a-z, 0-9 and _ characters
    event_type_watsonstudio_max_cpu_space=cp4d_monitor.create_and_validate_type ("cp4d_watsonstudio_max_cpu_space")
    event_type_watsonstudio_max_mem_space=cp4d_monitor.create_and_validate_type ("cp4d_watsonstudio_max_mem_space")
     
    metadata_watsonstudio_max_cpu_space='cp4d_watsonstudio_max_cpu_space={}'
    metadata_watsonstudio_max_mem_space='cp4d_watsonstudio_max_mem_space={}'
    
    #Array containing the monitor events
    events = []
    
    #   load k8s config
    config.load_kube_config()

#   load client
    v1 = client.CoreV1Api()
    node_list={}

#   sum over all running pods
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:

#       skip pods already done        
        if (item.status.phase == "Succeeded"):
            continue
        for j in item.spec.containers:
            if j.resources.requests:
 #               print(item.spec.node_name, j.name, j.resources)
                
                if ("cpu" in j.resources.requests): 
                    cpu=get_cpu(j.resources.requests["cpu"])
                else:
                    cpu=0

                if ("memory" in j.resources.requests):
                    mem=get_mem(j.resources.requests["memory"])
                else:
                    mem=0

                if (item.spec.node_name in node_list):
                    node_list[item.spec.node_name]["cpu"]=node_list[item.spec.node_name]["cpu"]+cpu
                    node_list[item.spec.node_name]["mem"]=node_list[item.spec.node_name]["mem"]+mem
                else:
                    node_list[item.spec.node_name]={"cpu":cpu, "mem":mem}

#   get node information 
    ret=v1.list_node(watch=False)

    max_cpu=0
    max_mem=0

    for item in ret.items:
#        print(item.metadata.name, item.status.allocatable["cpu"], item.status.allocatable["memory"])
        cpu_free=get_cpu(item.status.allocatable["cpu"])-node_list[item.metadata.name]["cpu"]
        mem_free=get_mem(item.status.allocatable["memory"])-node_list[item.metadata.name]["mem"]

#       remember max free space
        if (cpu_free > max_cpu):
            max_cpu=cpu_free
            max_cpu_mem=mem_free
        if (mem_free > max_mem):
            max_mem=mem_free
            max_mem_cpu=cpu_free

        node_list[item.metadata.name]={"cpu":node_list[item.metadata.name]["cpu"], "mem":node_list[item.metadata.name]["mem"], 
                                       "cpu-free": cpu_free, "mem-free":mem_free}

    print("%-16s %8s %10s %10s %10s" % ("Node", "cpu-req", "mem-req", "cpu-free", "mem-free"))
    for item in node_list:
        print("%-16s %8d %10d %10d %10d" % (item, node_list[item]["cpu"], node_list[item]["mem"], node_list[item]["cpu-free"], node_list[item]["mem-free"]))

    print()
    print("largest cpu environment - cpu: %8d /  mem: %10d" % (max_cpu, max_cpu_mem))
    print("largest mem environment - cpu: %8d /  mem: %10d" % (max_mem_cpu, max_mem))
    

    events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_max_cpu_space, 
                          "metadata": metadata_watsonstudio_max_cpu_space.format(max_cpu), 
                          "severity": "info", 
                          "reference": ""})
    events.append({"monitor_type":monitor_type, 
                          "event_type":event_type_watsonstudio_max_mem_space, 
                          "metadata": metadata_watsonstudio_max_mem_space.format(max_mem), 
                          "severity": "info", 
                          "reference": ""})

    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog     
    #print(events)
    cp4d_monitor.post_events(events)

if __name__ == '__main__':
   main()