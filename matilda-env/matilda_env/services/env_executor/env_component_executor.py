import requests
import json
from matilda_virt.services.compute.aws import service_manager
from matilda_env.services import service_base
from aims_so.api.controller import api_handler as so_ah

def _get_auth(payload):
    return {
        'aws_access_key': payload['cloud_auth']['aws_accesskey'] or 'AKIAIAHYTLHZZDTHVEZA',
        'aws_secret_key': payload['cloud_auth']['aws_secret'] or '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',
        'region': payload['cloud_auth']['aws_region'] or 'us-west-2'
    }

def create_network(payload):
    network = {
        'name': payload['network_details']['env_net_name'],
        'cidr': payload['network_details']['env_ip_range'],
        'tenancy': 'default',
        'tags': {
           'Name': payload['network_details']['env_net_name']
        }
    }


    aws = service_manager.AwsCompute()
    return aws.create_network(_get_auth(payload), network, payload['ritm_no'])

def create_subnet(payload, vpc_id=None):
    payload_sn = {}
    payload_sn['vpc_id'] = vpc_id
    payload_sn['cidr'] = payload.get('env_sub_net_range')
    payload_sn['state'] = payload.get('state') or 'present'
    payload_sn['az'] = payload.get('env_avai_zone')
    tags = {
           'Name': payload['network_details'].get('env_sub_net')
        }
    payload['tags'] = tags

    aws = service_manager.AwsCompute()
    return aws.create_subnet(_get_auth(payload), payload_sn, payload['ritm_no'])

def create_sec_group(payload, vpc_id=None):
    sec_grp = {
        'name': payload['security_group_info'].get('security_name') or payload['request_no'],
        'vpc_id': vpc_id,
        'description': payload['request_no'] + '_sec_grp',
        'rules': []
    }

    aws = service_manager.AwsCompute()
    return aws.create_security_group(_get_auth(payload), sec_grp, payload['ritm_no'])

def create_instances(payload, vpc_id=None, sec_grp=[]):
    src_image = payload['image_details']['image']
    if 'rhel' in src_image.lower():
        src_image = 'ami-223f945a'
    else:
        src_image = 'ami-79873901'
    compute = {
        'key_name': payload['server_info'].get('key_name') or 'qa',
        'flavor': payload['flavor_details']['flavor'],
        'security_group': sec_grp,
        'count': payload['server_info'].get('quantity') or 1,
        'image_id': src_image,
        'net_id': vpc_id,
        'state': 'present',
        'init_scripts': get_public_key_command(),
        'name': payload['server_info'].get('server_name')
    }
    aws = service_manager.AwsCompute()
    return aws.create_instance(_get_auth(payload), compute, payload['ritm_no'])

def create_lb(payload, instance_ids=[], sec_groups=[], port=[]):
    lb = {
            'name': payload['request_no']+'_lb',
            #'zones': ['us-west-2'],
            'sec_groups': sec_groups,
            'instance_id': instance_ids,
            'listeners': []
            }
    listeners = []
    for item in port:
        data = {
             'load_balancer_port': item,
             'instance_port': item
           }
        listeners.append(data)

    lb['listeners'] = listeners 
    print 'LB paylaod %r' % lb
    aws = service_manager.AwsCompute()
    return aws.create_lb(_get_auth(payload), lb, payload['ritm_no'])

def install_k8s(public_ips):
    master_ip = public_ips[0]
    if len(public_ips) > 1:
        slave_list = public_ips[1:]
        slaves = ','.join(slave_list)
    else:
        slaves = public_ips[0]
    args = {
            'request': {
                'name': 'kube cluster', 
                'slave_list': slaves, 
                'master_ip': master_ip
            }

        }

    response = so_ah.create_cluster(args['request'])
    #url = 'http://192.168.10.21:5002/cluster/new'
    #response = run_post(url, args,'','','')
    print response

def install_k8s_service(service, master_ip):
    args = {
        'request': {
            'service_name': service,
            'git_url':'http://192.168.20.142/chandu/kubernetesrepo/raw/master/',
            'cluster_info': {'master_ip': master_ip},
            'public_ip': master_ip,
            'replication':'1',
            'scale_up':'2',
            'scale_down':'1',
            'service':service,
            'deployment':service,
            'replication_count':'1',
            'ritm_no':'',
            'request_type':''
        }}
    url = 'http://192.168.10.21:5002/service/new'
    response = run_post(url, args, '','','')
    print response

def install_service(service, hosts):
    response = service_base.install_service(service, hosts)
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
        #msg = response.json()
        raise Exception(msg)

    return response.json()
   

def get_public_key_command():
    msg = """|
        #!/bin/bash
        echo {{ lookup('file', '~/.ssh/id_rsa.pub') }} >> /root/.ssh/authorized_keys
    """
    return msg
