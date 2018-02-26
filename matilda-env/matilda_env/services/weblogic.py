import subprocess
import uuid
import time
import logging

from matilda_virt.helper import ansible_executor as ae

LOG = logging.getLogger(__name__)

vars_files = [
    '/opt/matilda/so/weblogic/vars/jdk-vars.yml',
    '/opt/matilda/so/weblogic/vars/weblogic-vars.yml',
    '/opt/matilda/so/weblogic/vars/domain-vars.yml'
]

roles = [
    'ansibleWeblogic',
    'startdomain'
]

def prepare_playbook(hosts):
    pb = {}
    pb['hosts'] = 'weblogic'
    pb['become_user'] = 'root'
    pb['vars_files'] = vars_files
    pb['roles'] = roles
    return [pb]

def execute_playbook(pb,hosts):
    response = ae.execute_playbook(pb, hosts=[hosts], component='weblogic')
    print response
    return response

def run_playbook(pb, hosts):
    dir_path = ae.create_dir(str(uuid.uuid4()))
    playbook = ae.create_playbook_file(pb,'weblogic',dir_path)
    hostfile = ae.create_host_file([hosts], 'weblogic', dir_path)
    LOG.info('Playbook path for weblogic for [%r] hosts: %r' % (hosts, playbook))
    LOG.info('Hostfile path for weblogic for [%r] hosts: %r' % (hosts, hostfile))
    cmd = 'ansible-playbook -i {} {} -s -vvvv'.format(hostfile, playbook)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resp = process.communicate()
    LOG.debug('Response %r' % resp[0])
    LOG.error('Error %r' % resp[1])

    

def install_weblogic(hosts):
    LOG.info('Installing Weblogic')
    pb = prepare_playbook(hosts)
    response = run_playbook(pb, hosts)
    time.sleep(30)
    return response
