import requests
import json
import logging

from matilda_virt.services.compute.aws import service_manager
from matilda_virt.services.storage.aws import service_manager as storage_manager
from matilda_env.services import service_base
from aims_so.api.controller import api_handler as so_ah

from matilda_env.services.portable.tomcat import tomcat

LOG = logging.getLogger(__name__)

def _get_auth(payload):
    return {
        'aws_access_key': payload['cloud_auth']['aws_accesskey'] or 'AKIAIAHYTLHZZDTHVEZA',
        'aws_secret_key': payload['cloud_auth']['aws_secret'] or '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',
        'region': payload['cloud_auth']['aws_region'] or 'us-west-2'
    }

def create_network(payload):
    network = {
        'name': payload['network_details']['env_sel_net'],
        'cidr': payload['network_details']['env_ip_range'],
        'tenancy': 'default',
        'tags': {
           'Name': payload['network_details']['env_sel_net']
        }
    }
    LOG.info('Calling Network creation module')
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

    LOG.info('Calling Subnet creation module')
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
    LOG.info('Calling Security Group creation module')
    return aws.create_security_group(_get_auth(payload), sec_grp, payload['ritm_no'])

def create_instances(payload, vpc_id=None, sec_grp=[], service=None):
    src_image = payload['image_details']['image']

    compute = {
        'key_name': payload['server_info'].get('key_name'),
        'flavor': payload['flavor_details']['flavor'],
        'security_group': sec_grp,
        'count': payload['server_info'].get('quantity') or 1,
        'image_id': src_image,
        'net_id': vpc_id,
        'vpc_subnet_id': payload['network_details'].get('env_sub_net'),
        'state': 'present',
        'init_scripts': get_public_key_command(),
        'name': payload['server_info'].get('server_name')
    }
    if service == 'oracle':
        compute['volumes'] = [
            {
                'name': '/dev/xvda',
                'size': '60',
                'type': 'gp2'
            }
        ]
    aws = service_manager.AwsCompute()
    LOG.info('Calling Instance creation module')
    return aws.create_instance(_get_auth(payload), compute, payload['ritm_no'])

def create_volume(payload, public_ips=[]):
    s3 = {
        'bucket_name': payload['volume_details'].get('name')
    }
    print 'S3 name %r' % s3
    aws = storage_manager.AwsStorage()
    bucket_resp = aws.create_s3_bucket(_get_auth(payload), s3, payload['ritm_no'])
    return mount_s3(payload, payload['volume_details'].get('name'))

def mount_s3(payload, bucket_name, mount_dir='/', public_ips=[]):
    s3_mount = {
        'bucket_name': bucket_name,
        'mount_dir': mount_dir,
        'public_ips': public_ips
    }
    aws = storage_manager.AwsStorage()
    return aws.create_s3_bucket(_get_auth(payload), s3_mount, payload['ritm_no'])

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
    LOG.info('Calling LB creation module')
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
    LOG.info('Calling Kubernetes creation module')
    response = so_ah.create_cluster(args['request'])
    #url = 'http://192.168.10.21:5002/cluster/new'
    #response = run_post(url, args,'','','')
    LOG.info('Kubernetes Response %r' % response)
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
    LOG.info('Calling K8s Service creation module')
    response = run_post(url, args, '','','')
    print response

def install_service(service, hosts):
    if service == 'tomcat':
        for host in hosts:
            tomcat.install_tomcat(host)
        return True
    response = service_base.install_service(service, hosts)
    print response
    return response

def deploy_app(args, hosts):
    args =  {
        'username': args.get('username'),
        'password': args.get('password'),
        'target_server': args.get('target_server'),
        'warfile_path': args.get('warfile_path'),
        'warfile_name': args.get('warfile_name')
    }
    #response = service_base.install_service(args=args, hosts=hosts)
    for host in hosts:
        response = tomcat.deploy_application(args.get('warfile_path'), host)
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
        LOG.debug('url: %r, data: %r, type: %r' % (url, data, type(data)))
        response = requests.post(url, data=data, headers=headers, auth=(username, password))
        LOG.debug('REST Call response: %r' % response)
    except Exception as e:
        LOG.error('Failed to make REST call: %r' % e)
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
