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
    monitor_type="cp4d-wkc-info"

    event_type_wkc_info_catalog_overall_count=cp4d_monitor.create_and_validate_type("cp4d_wkc_info_catalog_overall_count") 
    event_type_wkc_info_catalog_asset_count=cp4d_monitor.create_and_validate_type("cp4d_wkc_info_catalog_asset_count") 

    metadata_wkc_info_catalog_overall_count="cp4d_wkc_info_catalog_overall_count={}"    
    metadata_wkc_info_catalog_asset_count="cp4d_wkc_info_catalog_asset_count={}"         

    events=[]
    wkcs = cp4d_monitor.get_waston_knowledge_catalogs()   
    cp4d_wkc_info_catalog_overall_count = 0
    cp4d_wkc_info_catalog_asset_count = 0
 
    for wkc in wkcs:
        cp4d_wkc_info_catalog_overall_count=+1

        catalog_id=wkc['metadata']['guid']
        assets = cp4d_monitor.get_assets_by_catalog(catalog_id)
        cp4d_wkc_info_catalog_asset_count=assets['total_rows']
        events.append({
                "monitor_type":monitor_type, 
                "event_type":event_type_wkc_info_catalog_asset_count, 
                "metadata": metadata_wkc_info_catalog_asset_count.format(cp4d_wkc_info_catalog_asset_count), 
                "severity": "info", 
                "reference": catalog_id})

    events.append({
            "monitor_type":monitor_type, 
            "event_type":event_type_wkc_info_catalog_overall_count, 
            "metadata": metadata_wkc_info_catalog_overall_count.format(cp4d_wkc_info_catalog_overall_count), 
            "severity": "info", 
            "reference": "All Watson Knowledge Catalogs"})
    
    #Post the events to the IBM Cloud Pak for Data Zen-Watchdog  
    #print(events)
    cp4d_monitor.post_events(events)


if __name__ == '__main__':
    main()