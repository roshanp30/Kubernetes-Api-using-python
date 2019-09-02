import yaml
from os import path
from kubernetes import client, config, utils
from pprint import pprint

DEPLOYMENT_NAME = "termi-demo"
IMAGE_NAME = "chetanpawar968/terminado"
PORT_NO = 8765
APP_NAME = "termi-demo"
API_VERSION = "v1"
KIND = "Pod"
NAMESPACE = "default"

def create_pod_object():
    # Configureate Pod template container
    container = client.V1Container(
        name=DEPLOYMENT_NAME,
        image=IMAGE_NAME,
        ports=[client.V1ContainerPort(container_port=PORT_NO)])
    # Create and configurate a spec section
    
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"name": APP_NAME}),
        spec=client.V1PodSpec(containers=[container]))
    """
    template = client.V1PodTemplateSpec(
        spec=client.V1PodSpec(containers=[container]))
    """   
    # Create the specification of deployment
    spec = client.V1PodSpec(containers=[container])
    #    template=template)
    # Instantiate the deployment object
    pod_object = client.V1Pod(
        api_version=API_VERSION,
        kind=KIND,
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return pod_object
    
        
def create_pod(api_instance,namespace):
    pod_body = create_pod_object()
    api_response = api_instance.create_namespaced_pod(namespace, pod_body)
    pprint(api_response)
    
    
def delete_pod(api_instance,namespace,name):
    api_response = api_instance.delete_namespaced_pod(name, namespace,body=client.V1DeleteOptions(
            propagation_policy='Foreground',
            grace_period_seconds=5))    
    pprint(api_response)
    
def main():
    config.load_kube_config()
    configuration = client.Configuration()
    api_instance = client.CoreV1Api(client.ApiClient(configuration))
    create_pod(api_instance,"default")
    #delete_pod(api_instance,"default","termi-demo")
main()
    

