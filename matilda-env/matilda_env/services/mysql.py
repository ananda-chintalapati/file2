from matilda_virt.helper import ansible_executor as ae
vars_files = [
    '/opt/matilda/so/mysql/vars/mysql-vars.yml'
]

roles = [
    'mysql'
]

def prepare_playbook(hosts):
    pb = {}
    pb['hosts'] = hosts
    pb['become_user'] = 'root'
    pb['vars_files'] = vars_files
    pb['roles'] = roles
    return pb

def run_playbook(pb):
    response = ae.execute_playbook(pb)
    print response
    return response

def install_mysql(hosts):
    print 'Installing MySQL'
    pb = prepare_playbook(hosts)
    response = run_playbook(pb)
    return response
