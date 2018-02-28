import uuid
import logging
import time

from matilda_env.db import api as db_api
from matilda_env.client import rpcapi

LOG = logging.getLogger(__name__)

def get_hosts(role):
    hosts = {
        'webserver': ['10.118.135.148'],
        'db': ['10.118.128.95']
    }
    return hosts[role]

def install_webserver(payload, service='tomcat', hosts=get_hosts('webserver'), warfile_loc=None, warfile_name=None):
    if warfile_name == None:
        warfile_name = 'samplepoc.war'

    if warfile_loc == None:
        warfile_loc = '/tmp'

    install_payload = {
        'service': service,
        'hosts': hosts,
        'u_ritm_no': payload['ritm_no'],
        'u_request_type': payload['u_request_type'],
        'u_name': payload['u_name']
    }

    process_install_service_request(install_payload)
    #time.sleep(180)
    deploy_payload = {
            'hosts': hosts,
            'args': {
            'username': None,
            'password': None,
            'target_server': hosts[0],
            'warfile_path': warfile_loc,
            'warfile_name': warfile_name,
            'u_ritm_no': payload['ritm_no'],
            'u_request_type': payload['u_request_type'],
            'u_name': payload['u_name']

            }
    }
    process_deploy_app_request(deploy_payload)

def install_database(payload, service='mysql', hosts=get_hosts('db'), warfile_loc=None, warfile_name=None):
    install_payload = {
        'service': service,
        'hosts': hosts,
        'u_ritm_no': payload['ritm_no'],
        'u_request_type': payload['u_request_type'],
        'u_name': payload['u_name']

    }

    process_install_service_request(install_payload)

def process_install_service_request(payload, source='ServiceNow', version='1'):
    LOG.info('Processing request with version %r' % version)
    cntx = {'req_id': str(uuid.uuid4())}
    rpc = rpcapi.RpcAPI()
    LOG.info('Posting payload %r' % payload)
    rpc.invoke_notifier(ctxt=cntx, payload=payload,
                        source=source, version=version, action='install_service')

def process_deploy_app_request(payload, source='ServiceNow', version='1'):
    LOG.info('Processing request with version %r' % version)
    cntx = {'req_id': str(uuid.uuid4())}
    rpc = rpcapi.RpcAPI()
    LOG.info('Posting payload %r' % payload)
    rpc.invoke_notifier(ctxt=cntx, payload=payload,
                        source=source, version=version, action='deploy_app')
