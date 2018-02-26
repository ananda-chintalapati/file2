from matilda_env.services.env_executor import env_component_executor as ec

url = 'http://192.168.10.21:5002/cluster/new'
data = {"request": {"name": "kube cluster", "slave_list": "34.209.32.8,34.214.158.83", "master_ip": "52.32.55.223"}}
public_ips = ["52.32.55.223","34.209.32.8","34.214.158.83"]
resp = ec.install_k8s(public_ips)
print resp
