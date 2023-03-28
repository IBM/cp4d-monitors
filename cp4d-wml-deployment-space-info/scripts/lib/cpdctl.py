import os
import json
import subprocess
import io

def is_json(json_string):
    try:
        json_object = json.loads(json_string)
    except Exception:
        return False
    return True

def cmd_execute(command, parameters="", output_format="json"):
    cmd_exist = os.popen(f'which {command}')
    output_cmd_exist = cmd_exist.read()
    if output_cmd_exist == "":
        print (f'{command}: command not found')
        exit(1)
    
    command=output_cmd_exist.strip('\n')
    whole_command =  (f'{command} {parameters}')
    
    if output_format == 'json':        
        whole_command = f'{whole_command} --output json'
    
    proc = subprocess.Popen(whole_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
    proc.wait()
    stream_stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8')
    stream_stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8')      
    str_stdout = str(stream_stdout.read())
    str_stderr = str(stream_stderr.read())
 
    if output_format == 'json':
        if str_stderr != "":
            print(f'Got error for the command: "{whole_command}"')
            print(f'Please refer to the response for details: {str_stderr}')
            return json.loads('{"status":"error"}')
        else:   
            if str_stdout == "":
                return json.loads("{}")
            else:
                return json.loads(str_stdout)
    else:
        if str_stderr != "":        
            return str_stderr
        else:
            return str_stdout

def cpdctl_init_config_context(username, password, url, context_name="default"):
    result = cmd_execute(command='cpdctl', parameters=f'config profile set {context_name} --username={username} --password={password} --url {url}')
    if 'status' in result and result['status'] == 'error':
        print("Got error to create cpd context.")
        exit(1)

def cpdctl_get_projects(context_name="default"):  
    projects = cmd_execute(command='cpdctl', parameters=f'project list --limit 100 --profile {context_name}')
    if 'status' in projects and projects['status'] == 'error':
        print("Got error to list all projects.")
        return []
    return projects

def cpdctl_get_jobs(project_id, context_name="default"):
    jobs = cmd_execute(command='cpdctl', parameters=f'job list --limit 100 --project-id {project_id} --profile {context_name}')
    if 'status' in jobs and jobs['status'] == 'error':
        print(f'Got error to get job for the project {project_id}.')
        return []
    return jobs

def cpdctl_get_job(project_id, job_id, context_name="default"):
    job = cmd_execute(command='cpdctl', parameters=f'job get --project-id {project_id} --job-id {job_id} --profile {context_name}')
    if 'status' in job and job['status'] == 'error':
        print(f'Got error to get job for the job {job_id} in the project {project_id}.')
        return None
    return job

def cpctl_get_spaces(context_name="default"):
    spaces = cmd_execute(command='cpdctl', parameters=f'space list --limit 100')
    if 'status' in spaces and spaces['status'] == 'error':
        print("Got error to list spaces.")
        return None
    return spaces


if __name__ == '__main__':
    cpdctl_init_config_context('username', 'password', 'CPD-URL')
    result = cpdctl_get_projects()
    print (result)