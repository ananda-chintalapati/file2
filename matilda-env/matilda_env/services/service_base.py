from matilda_env.services import mysql, tomcat, weblogic, weblogic_app_deployment as wad

from matilda_env.services.portable.tomcat import tomcat as tomcat_p
from matilda_env.services.portable.mysql import mysql as mysql_p

def install_service(service=None, hosts=None, type='service', args=None):
    if service == 'tomcat':
        #response = tomcat.install_tomcat(hosts)
        for host in hosts:
            response = tomcat_p.install_tomcat(host)
    elif service == 'weblogic':
        response = weblogic.install_weblogic(hosts)
    elif service == 'mysql':
        #response = mysql.install_mysql(hosts)
        for host in hosts:
            response = mysql_p.install_mysql(host)
    elif type == 'deploy':
        response = wad.install_weblogic_app(hosts, args)
    return response