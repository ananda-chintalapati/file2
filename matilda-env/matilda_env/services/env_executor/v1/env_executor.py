import time
import requests
import logging

from matilda_env.db import api as db_api
from matilda_env.services.env_executor.v1 import env_component_executor as ec
from matilda_env.services.jenkins import JenkinsManager as jc
from matilda_env.services.env_executor.v1 import task_db_handler as td

LOG = logging.getLogger(__name__)

def execute_environment(payload):
    if 'request' in payload.keys():
        payload = payload.get('request')
    _save_ritm(payload)
    ritms = get_ritms(payload['request_no'])
    if len(ritms) == payload['ritm_count'] or 1:
        _run_ritms(ritms)


def _run_ritms(ritms):
    print 'Running %r ritms' % len(ritms)
    for ritm in ritms:
        payload = ritm.get('payload')
        execute_payload(payload)


def execute_payload(payload):
    LOG.info('Executing payload %r' % payload)
    vpc_id = payload['network_details'].get('env_sel_net')
    sec_grp = []
    if payload['network_details'].get('env_net_conf') != 'Use Existing Network':
        LOG.info('Network creation task started')
        resp = ec.create_network(payload)
        LOG.info('Network creation task completed')
        LOG.debug('Network response %r' % resp)
        td.save_task('create_network', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success', '', resp)
        vpc_id = resp.get('output')[0].get('vpc').get('id')

        sec_grp = resp.get('output')[0].get('group_id')
        resp = ec.create_subnet(payload, vpc_id)
        LOG.info('Subnet creation task completed')
        LOG.debug('Subnet response %r' % resp)
        td.save_task('create_subnet', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)
    if payload['security_group'].get('Array_string') != None:
        LOG.info('Security Group creation task started')
        resp = ec.create_sec_group(payload, vpc_id)
        LOG.info('Sec Group creation task completed')
        LOG.debug('Sec Group response %r' % resp)
        td.save_task('create_sec_group', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)


    service = None
    if 'ser_cat_ws' in payload['service_info']:
        service = payload['service_info']['ws_typ_n'].lower()
    elif 'ser_cat_ds' in payload['service_info']:
        service = payload['service_info']['db_ser_typ_n'].lower()
    print 'Service %r' % service
    ports = get_service_ports(service)

    resp = ec.create_instances(payload, vpc_id, sec_grp, service)
    LOG.info('Instance creation task completed')
    LOG.debug('Instance response %r' % resp)
    td.save_task('create_instance', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                 '', resp)


    instance_ids = resp.get('output')[0].get('instance_ids')
    public_ips = []
    instance_ids = []
    for item in resp.get('output'):
        public_ips.append(item.get('public_ip'))
        instance_ids.append(item.get('instance_id'))
    print 'Public Ips : %r' % public_ips

    if payload['volume_details'].get('name') != None:
        resp = ec.create_volume(payload, public_ips)
        LOG.info('Volume creation task completed')
        LOG.debug('Volume response %r' % resp)
        td.save_task('create_volume', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)

    if payload['server_info']['quantity'] > 1:
        LOG.info('LB Creation started')
        resp = ec.create_lb(payload, instance_ids, [sec_grp], ports)
        LOG.info('LB creation task completed')
        LOG.debug('LB response %r' % resp)
        td.save_task('create_lb', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)

    need_k8 = payload['service_info'].get('con_ws') or payload['service_info'].get('con_db') or 'No'
    LOG.info('Need Kubernetes: %s' % need_k8)
    if need_k8 == 'Yes':
        LOG.info('Waiting to finish instance creation steps')
        time.sleep(120)
        resp = ec.install_k8s(public_ips)
        LOG.info('Kubernetes creation task completed')
        LOG.debug('Kubernetes response %r' % resp)
        td.save_task('install_k8s', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)
        time.sleep(120)
        resp = ec.install_k8s_service(service, public_ips[0])
        LOG.info('Kubernetes service creation task completed')
        LOG.debug('Kubernetes service response %r' % resp)
        td.save_task('install_k8s_service', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)
    else:
        LOG.info('Installing service')
        time.sleep(120)
        LOG.info('Waiting to finish instance creation steps')
        resp = ec.install_service(service, public_ips)
        LOG.info('Service creation task completed')
        LOG.debug('Service response %r' % resp)
        td.save_task('install_service', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)
        
    if 'application_info' in payload:
        LOG.info('Triggering application')
        trigger_application(payload)
        LOG.info('Application creation task completed')
        LOG.debug('Application response %r' % resp)
        td.save_task('trigger_application', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                     '', resp)

    LOG.info('Sending final response to ServiceNow')
    resp = send_response_to_sn(payload, public_ips)
    td.save_task('send_response_to_sn', payload['u_request_type'], payload['ritm_no'], payload['request_no'], 'Success',
                 '', resp)

def install_service(service, ip_list):
    LOG.info('Waiting to finish instance creation steps')
    resp = ec.install_service(service, ip_list)
    LOG.info('Service creation task completed')
    LOG.debug('Service response %r' % resp)

def create_security_group(payload, vpc_id):
    ec.create_sec_group()


def deploy_application_to_wl(args, ip_list):
    LOG.info('Waiting to finish instance creation steps')
    resp = ec.deploy_app(args, ip_list)
    LOG.info('Service creation task completed')
    LOG.debug('Service response %r' % resp)


def trigger_application(payload):
    jenkins_url = "http://192.168.10.161:8080"
    username = 'admin'
    password = 'jenkins'
    jenkins = jc(jenkins_url, username, password)
    job_name = payload['application_info']['jen_jn']
    print 'Triggering Jenkins job'
    jenkins.trigger_job(job_name)
    return 'Success'

def get_output_for_web(req_no):
    tasks = db_api.get_ritm_tasks_by_req_role(req_no, 'Web Server Environment & Application Info')
    public_ips = []
    for task in tasks:
        if task.get('name') == 'create_instance':
            output = task.get('output')
            for item in output:
                public_ips.append(item.get('public_ip'))
    return public_ips



def send_response_to_sn(payload, public_ip):
    data = {
        'u_status': 'Success',
        'u_ritm_no': payload['ritm_no'],
        'u_request_type': payload['u_request_type'],
        'u_name': payload['u_name'],
        'u_ip_address': public_ip,
        'u_storage_name': '',
        'u_storage_ip':''
       }
    url = 'https://dev21017.service-now.com.service-now.com/api/now/table/u_server_temp'
    username = 'qa.user'
    password = 'Cnet123$'
    headers = {'Content-type': 'application/json'}
    LOG.info('Sending response to ServiceNow: %r' % data)
    resp = requests.post(url=url, auth=(username, password), data=data, headers=headers)
    LOG.info('ServiceNow call response %r' % resp)
    print resp

    
def get_service_ports(service):
    ports = {
     'weblogic': [7002],
     'tomcat': [8080],
     'mysql': [3306],
     'oracle': [1521]
    }

    return ports[service]

def _save_ritm(payload):
    ritm_args = {
        'ritm_no': payload['ritm_no'],
        'request_id': payload['request_no'],
        'payload': payload,
        'status': 'Created'
    }
    print 'DB Args %r' % ritm_args
    db_api.save_ritm(ritm_args)

def get_ritms(req_no):
    print 'Getting rimts for %r' % req_no
    ritm_list = db_api.get_ritm_for_request(req_no)
    print 'RITM List data' % ritm_list
    return ritm_list


