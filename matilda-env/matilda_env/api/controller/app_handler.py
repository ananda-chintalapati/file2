import os
import uuid
import logging

from matilda_env.db import api as db_api
from matilda_env.client import rpcapi

from matilda_env.api.controller import app_handler_poc

LOG = logging.getLogger(__name__)

def save_sn_request(payload):
    ritm_resp = _save_ritm(payload)
    LOG.info('Saving RITM')
    response = _save_request(payload['request_no'], payload['ritm_count'])
    LOG.info('Request saved. %r' % response)
    return response

def _save_ritm(payload):
    ritm = db_api.get_ritm(payload['ritm_no'])
    if ritm == None:
        args = {
            'ritm_no': payload['ritm_no'],
            'request_id': payload['request_id'],
            'payload': payload,
            'status': 'Received'
        }
        return db_api.save_ritm(args)
    else:
        return ritm

def _save_request(request_id, ritm_count):
    req = db_api.get_request(request_id)
    status = 'Request Pending'
    response = None
    if req == None:
        if req.get('total_ritm_count') == 1:
            status = 'Request Processing'
        args = {
            'request_id': request_id,
            'total_ritm_count': ritm_count,
            'received_ritm': 1,
            'status': status
        }
        response = db_api.save_request(args)
    else:
        curr_ritm = req.get('received_ritm')
        if int(curr_ritm) + 1 == req.get('total_ritm_count'):
            status = 'Request Processing'
        args = {
            'received_ritm': int(curr_ritm) + 1,
            'status': status
        }
        response = db_api.save_request(args)

    if status == 'Request Processing':
        process_request(request_id)
    return response

def process_request(req_id):
    ritms = db_api.get_ritm_for_request(req_id)
    response = process_ritms(ritms)
    return response

def process_ritms(ritms):
    return True

def process_create_env_request_old(payload, source='ServiceNow', version='1'):
    LOG.info('Processing request with version %r' % version)
    cntx = {'req_id': str(uuid.uuid4())}
    rpc = rpcapi.RpcAPI()
    LOG.info('Posting payload %r' % payload)
    rpc.invoke_notifier(ctxt=cntx, payload=payload,
                        source=source, version=version, action='deploy_env')

def process_create_env_request(payload, source='ServiceNow', version='1'):
    LOG.info('Processing request with version %r' % version)
    cntx = {'req_id': str(uuid.uuid4())}
    # if 'service_info' in payload.keys():
    #     if 'ser_cat_ds' in payload['service_info'].keys():
    #         app_handler_poc.install_database(payload)
    #     else:
    #         app_handler_poc.install_webserver(payload)
    rpc = rpcapi.RpcAPI()
    LOG.info('Posting payload %r' % payload)
    rpc.invoke_notifier(ctxt=cntx, payload=payload,
                        source=source, version=version, action='deploy_env')


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

def save_policy_req(req_id, type, data):
    path = '/opt/matilda/requests/' + req_id
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = str(type) + '.json'
    with open(path + file_name, 'w') as f:
        f.write(data)
    return True

def trigger_backend(req_id):
    DIR = '/opt/matilda/requests/' + req_id
    file_count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    if file_count == 3:
        cntx = {'req_id': str(uuid.uuid4())}
        payload = {'request_id': req_id}
        rpc = rpcapi.RpcAPI()
        LOG.info('Posting payload %r' % payload)
        rpc.invoke_notifier(ctxt=cntx, payload=payload,
                            source='', version='1', action='vz_pol')