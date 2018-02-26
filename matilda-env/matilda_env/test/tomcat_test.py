from matilda_env.services.portable.tomcat import tomcat

def test_tomcat():
    tomcat.install_tomcat('192.168.10.156', 'root', 'openstack')

test_tomcat()