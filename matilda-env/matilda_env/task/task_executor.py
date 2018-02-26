import requests

from matilda_env.db import api as db_api
from matilda_env.services import service_base
from matilda_env.task import task_db_handler as tdh

from matilda_virt.services.compute.aws import service_manager
from aims_so.api.controller import api_handler as so_ah

def execute_taskflow(task_flow_id, task_list, ritm_no=''):
    for task_id in task_list:
        task = db_api.get_task(task_id)
        payload = task.get('payload')
        depend_data = task.get('depend_data')
        task_name = task.get('name')
        response = getattr('matilda_env.task.task_executor', task_name)(payload, '', depend_data)
        tdh.save_task_output(task_id, response['data'])



def create_network(payload, ritm_no, depend_data):
    aws = service_manager.AwsCompute()
    return aws.create_network(payload['auth'], payload['args'], ritm_no)


def create_subnet(payload, ritm_no, depend_data):
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    payload['args']['vpc_id'] = output[0].get('vpc').get('id')
    aws = service_manager.AwsCompute()
    return aws.create_subnet(payload['auth'], payload['args'], ritm_no)


def create_sec_group(payload, ritm_no, depend_data):
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    payload['args']['vpc_id'] = output[0].get('vpc').get('id')
    aws = service_manager.AwsCompute()
    return aws.create_security_group(payload['auth'], payload['args'], ritm_no)


def create_instances(payload, ritm_no, depend_data):
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    payload['args']['vpc_id'] = output[0].get('vpc').get('id')
    task_id = depend_data[1]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    payload['args']['sec_grp'] = output[0].get('group_id')
    aws = service_manager.AwsCompute()
    return aws.create_instance(payload['auth'], payload['args'], ritm_no)


def create_lb(payload, ritm_no, depend_data):
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    payload['args']['sec_groups'] = [output[0].get('group_id')]
    instance_ids = []
    task_id = depend_data[1]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    for item in output:
        instance_ids.append(item.get('instance_id'))
    payload['args']['instance'] = instance_ids
    aws = service_manager.AwsCompute()
    return aws.create_lb(payload['auth'], payload['args'], ritm_no)


def create_k8s(payload, ritm_no, depend_data):
    instance_ips = []
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    for item in output:
        instance_ips.append(item.get('public_ip'))
    master_ip = instance_ips[0]
    if len(instance_ips) > 1:
        slave_list = instance_ips[1:]
        slaves = ','.join(slave_list)
    else:
        slaves = instance_ips[0]
    args = {
        'request': {
            'name': 'kube cluster',
            'slave_list': slaves,
            'master_ip': master_ip
        }

    }

    response = so_ah.create_cluster(args['request'])
    # url = 'http://192.168.10.21:5002/cluster/new'
    # response = run_post(url, args,'','','')
    print response


def install_k8s_service(payload, ritm_no, depend_data):
    instance_ips = []
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    for item in output:
        instance_ips.append(item.get('public_ip'))
    master_ip = instance_ips[0]
    payload['request']['public_ip'] = master_ip
    payload['request']['cluster_info']['master_ip'] = master_ip
    url = 'http://192.168.10.21:5002/service/new'
    response = run_post(url, payload, '', '', '')
    print response


def install_service(payload, ritm_no, depend_data):
    instance_ips = []
    task_id = depend_data[0]['task']
    task = db_api.get_task(task_id)
    output = task.get('output')
    for item in output:
        instance_ips.append(item.get('public_ip'))
    response = service_base.install_service(payload, instance_ips)
    print response
    return response


def run_post(url, data, in_headers=None, username='qa.user', password='Cnet123$'):
    headers = {'Content-Type': 'application/json', 'Accepts': 'application/json'}
    auth = None
    if username is not None and password is not None:
        auth = '(' + username + ',' + password + ')'

    if in_headers is not None:
        headers.update(in_headers)

    try:
        print 'url: %r, data: %r, type: %r' % (url, data, type(data))
        response = requests.post(url, data=data, headers=headers, auth=(username, password))
        print response
    except Exception as e:
        print e
        raise Exception(e.message)
    except ValueError as e:
        raise Exception(e.message)

    if not response.ok:
        msg = response
        print msg
        # msg = response.json()
        raise Exception(msg)

    return response.json()


def get_public_key_command():
    msg = """|
        #!/bin/bash
        echo {{ lookup('file', '~/.ssh/id_rsa.pub') }} >> /root/.ssh/authorized_keys
    """
    return msg
