from matilda_env.services.env_executor import env_component_executor as ec

service='weblogic'
public_ips = ['34.214.183.216']
resp = ec.install_service(service, public_ips)
print resp
