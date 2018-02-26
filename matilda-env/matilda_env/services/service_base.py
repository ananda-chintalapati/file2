from matilda_env.services import mysql, tomcat, weblogic, weblogic_app_deployment as wad

def install_service(service=None, hosts=None, type='service', args=None):
    if service == 'tomcat':
        response = tomcat.install_tomcat(hosts)
    elif service == 'weblogic':
        response = weblogic.install_weblogic(hosts)
    elif service == 'mysql':
        response = mysql.install_mysql(hosts)
    elif type == 'deploy':
        response = wad.install_weblogic_app(hosts, args)
    return response