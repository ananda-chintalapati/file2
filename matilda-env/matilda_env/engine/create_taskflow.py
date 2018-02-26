import contextlib
import hashlib
import logging
import os
import random
import sys
import time
import subprocess
logging.basicConfig(level=logging.ERROR)
self_dir = os.path.abspath(os.path.dirname(__file__))
top_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       os.pardir,
                                       os.pardir))
sys.path.insert(0, top_dir)
sys.path.insert(0, self_dir)
import futurist
from oslo_utils import uuidutils
from taskflow import engines
from taskflow import exceptions as exc
from taskflow.patterns import graph_flow as gf
from taskflow.patterns import linear_flow as lf
from taskflow.persistence import models
from taskflow import task
from aims_virt.infra import create_server
from aims_virt.client import sn_client
from aims_virt.services import zabbix_manager

class CreateInstance(task.Task):
    def __init__(self, name):
        super(CreateInstance, self).__init__(provides='install_vm',
                                             name=name)
    def execute(self, payload):
        print payload
        provider = payload['request']['provider'].lower()
        payload['request']['provider'] = provider
        if provider == 'openstack':
            manager = create_server.OpenStackManager(self.payload)
        elif provider == 'vmware':
            manager = create_server.VMWareManager(self.payload)
        elif provider == 'aws':
            manager = create_server.AWSManager(self.payload)
        elif provider == 'azure':
            manager = create_server.AzureManager(self.payload)
        status = {}
        output = None
        try:
            output = manager.create_server()
            if output is not None:
                status['vm_status'] = 'Active'
                status['status'] = 'Success'
        except Exception as e:
            status['vm_status'] = 'Not Installed'
            status['status'] = 'Failure'
        return output, status

class UpdateServiceNow(task.Task):
    def __init__(self, name):
        super(UpdateServiceNow, self).__init__(provides='update_sn',
                                             name=name)
    def execute(self, payload, output, status):
        sn_client.send_server_data(req_data=payload, vm_data=output, status_info=status)

class UpdateHostData(task.Task):
    def __init__(self, name):
        super(UpdateHostData, self).__init__(provides='update_hosts',
                                             name=name)
    def execute(self, vm_data):
        for vm in vm_data:
            cmd = "echo \"" + vm['public_ip'] + "  " + vm['name'] + "\" >> /etc/hosts"
            print 'cmd %r' % cmd
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            resp = proc.communicate()[1]
            print 'Std Out %r ' % (resp)

class UploadMasterKeys(task.Task):
    def __init__(self, name):
        super(UploadMasterKeys, self).__init__(provides='upload_keys',
                                               name=name)
    def execute(self, ip_list, master='localhost'):
        for ip in ip_list:
            cmd = "sudo sshpass -p css@dmin ssh -o StrictHostKeyChecking=no  css@" + master + \
                  " \"sshpass -p css@dmin ssh-copy-id -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa.pub css@"+ip+"\""
            print 'cmd %r' % cmd
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            resp = proc.communicate()[1]
            print 'Std Out %r ' % (resp)

class GrantUserPrivilege(task.Task):
    def __init__(self, name):
        super(GrantUserPrivilege, self).__init__(provides='grant_aims_sudo',
                                                 name=name)
    def execute(self, ip_list, user='css'):
        for ip in ip_list:
            cmd = "sudo sshpass -p css@dmin ssh -o StrictHostKeyChecking=no  " + user +"@" + ip + \
                  " \"echo css@dmin | sudo -S sed -i '/#includedir/i " + user + " ALL=(ALL) NOPASSWD: ALL' /etc/sudoers\""
            print 'cmd %r' % cmd
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            resp = proc.communicate()[1]
            print 'Std Out %r ' % (resp)

class InstallPython(task.Task):
    def __init__(self, name):
        super(InstallPython, self).__init__(provides='install_python',
                                            name=name)
    def execute(self, ip_list):
        for ip in ip_list:
            cmd = "su -c css \"sudo ssh css@" + ip + " \"sudo apt-get install python -y\"\""
            print 'cmd %r' % cmd
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            resp = proc.communicate()[1]
            print 'Std Out %r ' % (resp)

class InstallSNMP(task.Task):
    pass

class InstallZabbix(task.Task):

    def __init__(self, name):
        super(InstallZabbix, self).__init__(provides='install_zabbix',
                                            name=name)

    def get_zabbix_server_details(self):
        # TODO: FIX this
        data = {'ip': '192.168.20.89',
                'url': 'http://192.168.20.89/zabbix/api_jsonrpc.php',
                'user': 'admin',
                'password': 'zabbix',
                'host_list': ['Linux Servers']}
        return data

    def execute(self, zabbix_data, ip_list, cloud_id):
        zabbix_data = self.get_zabbix_server_details()
        try:
            zabbix_manager.install_zabbix_agent(ip_list, zabbix_data['ip'], zabbix_data['url'], 'true',
                                                zabbix_data['user'], zabbix_data['password'],
                                                cloud_id, None)
        except Exception as e:
            print e
            return False
        return True

class InstallFilebeat(task.Task):

    def __init__(self, name):
        super(InstallFilebeat, self).__init__(provides='install_filebeat',
                                            name=name)
    def install_filebeat(self):
        return True

class CreateServerTaskflow(object):

    def __init__(self, payload):
        self.payload = payload

    def create_taskflow(self):
        print 'Hello'
        create_instance = lf.Flow("origin").add(CreateInstance('create_instance'))
        results = engines.run(create_instance, store={'payload': self.payload})
        output = results['output']
        status = results['status']
        create_instance = gf.Flow("addon").add(UpdateServiceNow('update_sn'),
                                               UpdateHostData('update_host'),
                                               UploadMasterKeys('upload_keys'),
                                               GrantUserPrivilege('add_user_ssh'),
                                               InstallPython('install_python'))

