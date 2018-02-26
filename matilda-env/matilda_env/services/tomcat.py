from matilda_virt.helper import ansible_executor as ae

roles = [
    'selinux',
    'tomcat'
]

def prepare_playbook(hosts):
    pb = {}
    pb['hosts'] = hosts
    pb['become_user'] = 'root'
    pb['roles'] = roles
    return pb

def run_playbook(pb):
    response = ae.execute_playbook(pb)
    print response
    return response

def install_tomcat(hosts):
    print 'Installing Tomcat'
    pb = prepare_playbook(hosts)
    response = run_playbook(pb)
    return response
