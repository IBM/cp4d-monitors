import base64
from kubernetes import client, config


try:
    config.load_incluster_config()
except config.ConfigException:
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")

core_api = client.CoreV1Api()
custome_api = client.CustomObjectsApi()
app_api = client.AppsV1Api()

def is_exist_config_map(namespace,name):
    result = True
    try:
        core_api.read_namespaced_config_map(name=name,namespace=namespace)
    except:
        result = False
    return result

def create_configmap_cp4d_monitor_configuration(namespace):
    # Configureate ConfigMap metadata
    metadata = client.V1ObjectMeta(
        name = "cp4d-monitor-configuration"
    )
    data = {
        "cp4d-job-last-refresh" : "0",
        "cp4d-job-refresh-interval-minutes": "120",
        "cp4d-project-last-refresh": "0",
        "cp4d-project-refresh-interval-minutes": "240",
        "cp4d-space-last-refresh": "0",
        "cp4d-space-refresh-interval-minutes": "120",
        "cp4d-wkc-last-refresh": "0",
        "cp4d-wkc-refresh-interval-minutes": "120"
    }
    configmap = client.V1ConfigMap(
        api_version="v1",
        kind="ConfigMap",
        data=data,
        metadata=metadata
    )
    core_api.create_namespaced_config_map(namespace, configmap)


def get_config_map(namespace,name):        
    config_map = core_api.read_namespaced_config_map(name=name,namespace=namespace)   
    return config_map.data

def get_config_map_value(namespace,name,key):
    return get_config_map(namespace=namespace, name=name)[key]
    
def set_config_map(namespace,name, key, value):
    config_map = get_config_map(namespace=namespace, name=name)
    config_map[key]=value
    core_api.patch_namespaced_config_map(namespace=namespace, name=name,body=client.V1ConfigMap(data=config_map))

def set_config_map(namespace,name,data):
    core_api.patch_namespaced_config_map(namespace=namespace, name=name,body=client.V1ConfigMap(data=data))

def get_admin_secret(namespace):
    secret = core_api.read_namespaced_secret("admin-user-details", namespace).data
    return base64.b64decode(secret['initial_admin_password']).decode()

def get_deployment(namespace,label_selector):
  resources =app_api.list_namespaced_deployment(namespace=namespace,label_selector=label_selector)
  deployments={}
  for deployment in resources.items:
    #print(pod['containers'], "\n")
    deployments[deployment.metadata.name]=deployment
  return deployments
  

def get_pod_usage(namespace,label_selector):
  resources = custome_api.list_namespaced_custom_object(group="metrics.k8s.io",version="v1beta1",
                                               namespace=namespace, plural="pods",label_selector=label_selector)
  pods = []
  for pod in resources["items"]:
    #print(pod['containers'], "\n")
    pods.append(pod)
  return pods

def check_ccs_svc(namespace):
    error_msg = "Custom Resource Definition CCS is either not available or no instance available. CPDCTL capabilities are not available on this Cloud Pak for Data instance."
    result = False
    try:   
       ccs_cm = core_api.list_namespaced_config_map(
           label_selector="app=ccs",
           namespace=namespace           
       )    
       if len(ccs_cm.items) >= 1:
           result =  True
    # except Exception as e:        
    #     print(e)
    finally:
        if result == False:
            print(error_msg)
            exit(1)