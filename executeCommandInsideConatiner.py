"""
The below code is api version of the kubectl command exec
eg :
 kubectl exec pod-name exec command
"""

from os import path

from kubernetes import client, config, utils

from kubernetes.stream import stream

from pprint import pprint

def execute_on_container(core_api_instance,pod,namespace,exec_command1):
    user_name_str = stream(core_api_instance.connect_get_namespaced_pod_exec, pod,
    namespace,command=exec_command1, stderr=True, stdin=False,
    stdout=True, tty=False)
    return user_name_str

config.load_kube_config()
namespace = "default"
#Pod name on which commands is to be executed
pod = "termi-demo-6bf977984f-f254l"
exec_command1 = ['bash','/abc/t1.sh']
core_api_instance = client.CoreV1Api()
print(execute_on_container(core_api_instance,pod,namespace,exec_command1))
    
