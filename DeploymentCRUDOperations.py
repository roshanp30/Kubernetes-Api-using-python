import yaml
from os import path
from kubernetes import client, config, utils
from pprint import pprint

DEPLOYMENT_NAME = "termi-demo"
IMAGE_NAME = "chetanpawar968/terminado"
PORT_NO = 8765
APP_NAME = "termi-demo"
API_VERSION = "extensions/v1beta1"
KIND = "Deployment"
NAMESPACE = "default"

def create_deployment_object(count):
    # Configureate Pod template container
    container = client.V1Container(
        name=DEPLOYMENT_NAME,
        image=IMAGE_NAME,
        ports=[client.V1ContainerPort(container_port=PORT_NO)])
    # Create and configurate a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": APP_NAME}),
        spec=client.V1PodSpec(containers=[container]))
    # Create the specification of deployment
    spec = client.ExtensionsV1beta1DeploymentSpec(
        replicas=int(count),
        template=template)
    # Instantiate the deployment object
    deployment = client.ExtensionsV1beta1Deployment(
        api_version=API_VERSION,
        kind=KIND,
        metadata=client.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=spec)

    return deployment

def create_deployment(api_instance,newnamespace):
    # Create deployement
    count=1
    deployment = create_deployment_object(count)
    api_response = api_instance.create_namespaced_deployment(
        body=deployment,
        namespace=str(newnamespace).lower())
    """
    print("Deployment deleted. status='%s'" % str(api_response.status))
    print(api_response.kind)
    print("METADATA")
    print(api_response.metadata)
    print("SPEC")
    print(api_response.spec)
    print("Status")
    print(api_response.status)
    """

def increase_replicas(api_instance,count,name,namespace):
    config.load_kube_config()
    #deployment_name="hello-world-deployment.yaml"
    #name="termi-demo"
    deployment = create_deployment_object(count)
    #namespace="default"
    #api_response = k8s_api.patch_namespaced_deployment(name, namespace, body, pretty=pretty, dry_run=dry_run)
    api_response = api_instance.patch_namespaced_deployment(name, namespace, deployment)
    #pprint(api_response)
    #deployment_name="dep_term1.yaml"
    #with open(path.join(path.dirname(__file__),deployment_name )) as f:
    #    dep = yaml.safe_load(f)

def read_scale(api_instance,name,namespace):
    api_response = api_instance.read_namespaced_deployment_scale(name, namespace)
    #pprint(api_response.spec)
    replicas_count=api_response.spec.replicas
    if replicas_count>=1:
        return replicas_count
    else :
        return 0

def check_if_deployment_exists(api_instance,namespace,deploymentName):
     api_response=api_instance.list_namespaced_deployment(namespace,include_uninitialized=True)
     #pprint(api_response)
     #print(len(api_response.items))
     deploymentSize=len(api_response.items)
     if deploymentSize>0:
         for z in range(deploymentSize):
             deploymentAlreadyExists=api_response.items[z].metadata.name
             #print(type(deploymentAlreadyExists))
             #print(deploymentAlreadyExists)
             if  deploymentAlreadyExists==deploymentName:
                return True
             """
		     #Add some logic as per use-case if deployment doesnt exist
             else :
                return False
             """
     else:
        return False

if __name__ == '__main__':
    config.load_kube_config()
    extensions_v1beta1 = client.ExtensionsV1beta1Api()
    #create_deployment(extensions_v1beta1,"default")
    create_deployment(extensions_v1beta1,NAMESPACE)
    exists=check_if_deployment_exists(extensions_v1beta1,NAMESPACE,DEPLOYMENT_NAME)
    #Uncomment below to check no of replicas for deployment	
    #replica_scale=read_scale(extensions_v1beta1,DEPLOYMENT_NAME,NAMESPACE)
    
    #Uncomment below to increase number of replicas,first parameter is api instance and second is desired number of replicas and remaining parameters are self explanatory
    #increase_replicas(extensions_v1beta1,replica_scale+2,DEPLOYMENT_NAME,NAMESPACE)
