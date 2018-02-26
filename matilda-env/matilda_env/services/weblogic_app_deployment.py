import subprocess
import uuid
import time
import logging

from matilda_virt.helper import ansible_executor as ae

LOG = logging.getLogger(__name__)

roles = [
    'appdeploy'
]

def prepare_vars(args):
    vars = {
        'username': args.get('username'),
        'password': args.get('password'),
        'target_server': args.get('target_server'),
        'warfile_path': args.get('warfile_path'),
        'warfile_name': args.get('warfile_name'),
        'jenkins_host': args.get('jenkins_host'),
        'jenkins_user': args.get('jenkins_user'),
        'jenkins_job': args.get('jenkins_job'),
        'jenkins_job_token': args.get('jenkins_job_token'),
        'jenkins_cred': args.get('jenkins_cred')
    }
    return vars

def prepare_playbook(hosts, vars):
    pb = {}
    pb['hosts'] = 'weblogic_app'
    pb['become_user'] = 'root'
    pb['vars'] = vars
    pb['roles'] = roles
    return [pb]


def execute_playbook(pb, hosts):
    response = ae.execute_playbook(pb, hosts=[hosts], component='weblogic_app')
    print response
    return response


def run_playbook(pb, hosts):
    dir_path = ae.create_dir(str(uuid.uuid4()))
    playbook = ae.create_playbook_file(pb, 'weblogic_app', dir_path)
    hostfile = ae.create_host_file([hosts], 'weblogic_app', dir_path)
    LOG.info('Playbook path for weblogic for [%r] hosts: %r' % (hosts, playbook))
    LOG.info('Hostfile path for weblogic for [%r] hosts: %r' % (hosts, hostfile))
    cmd = 'ansible-playbook -i {} {} -s -vvvv'.format(hostfile, playbook)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resp = process.communicate()
    LOG.debug('Response %r' % resp[0])
    LOG.error('Error %r' % resp[1])


def install_weblogic_app(hosts, args):
    LOG.info('Installing Weblogic Application')
    vars = prepare_vars(args)
    pb = prepare_playbook(hosts, vars)
    response = run_playbook(pb, hosts)
    time.sleep(30)
    return response
