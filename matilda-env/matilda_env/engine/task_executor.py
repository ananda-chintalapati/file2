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

def create_instance(payload):
    provider = payload['request']['provider'].lower()
    payload['request']['provider'] = provider
    if provider == 'openstack':
        manager = create_server.OpenStackManager(payload)
    elif provider == 'vmware':
        manager = create_server.VMWareManager(payload)
    elif provider == 'aws':
        manager = create_server.AWSManager(payload)
    elif provider == 'azure':
        manager = create_server.AzureManager(payload)
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


def update_sn(payload, output, status):
    sn_client.send_server_data(req_data=payload, vm_data=output, status_info=status)


def update_hosts(vm_data):
    for vm in vm_data:
        cmd = "echo \"" + vm['public_ip'] + "  " + vm['name'] + "\" >> /etc/hosts"
        print 'cmd %r' % cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        resp = proc.communicate()[1]
        print 'Std Out %r ' % (resp)

def upload_keys(ip_list, master='localhost'):
    for ip in ip_list:
        cmd = "sudo sshpass -p css@dmin ssh -o StrictHostKeyChecking=no  css@" + master + \
              " \"sshpass -p css@dmin ssh-copy-id -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa.pub css@"+ip+"\""
        print 'cmd %r' % cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        resp = proc.communicate()[1]
        print 'Std Out %r ' % (resp)


def grant_permissions(ip_list, user='css'):
    for ip in ip_list:
        cmd = "sudo sshpass -p css@dmin ssh -o StrictHostKeyChecking=no  " + user +"@" + ip + \
              " \"echo css@dmin | sudo -S sed -i '/#includedir/i " + user + " ALL=(ALL) NOPASSWD: ALL' /etc/sudoers\""
        print 'cmd %r' % cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        resp = proc.communicate()[1]
        print 'Std Out %r ' % (resp)


def install_python(ip_list):
    for ip in ip_list:
        cmd = "su -c css \"sudo ssh css@" + ip + " \"sudo apt-get install python -y\"\""
        print 'cmd %r' % cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        resp = proc.communicate()[1]
        print 'Std Out %r ' % (resp)

def get_zabbix_server_details():
    #TODO: FIX this
    data = {'ip': '192.168.20.89',
            'url': 'http://192.168.20.89/zabbix/api_jsonrpc.php',
            'user': 'admin',
            'password': 'zabbix',
            'host_list': ['Linux Servers']}
    return data


def install_zabbix_agent(zabbix_data, ip_list, cloud_id):
    try:
        zabbix_manager.install_zabbix_agent(ip_list, zabbix_data['ip'], zabbix_data['url'], 'true',
                                        zabbix_data['user'], zabbix_data['password'],
                                        cloud_id, None)
    except Exception as e:
        print e
        return False
    return True


def install_filebeat():
    return True

def install_snmp():
    return True

def flow_watch(state, details):
    print('Flow => %s' % state)


def task_watch(state, details):
    print('Task %s => %s' % (details.get('task_name'), state))


class TaskExecutor(object):

    def __init__(self):
        pass

    def create_taskflow(self, payload):
        flow = lf.Flow("install_vm").add(
            task.FunctorTask(create_instance, provides='created_instance'))





