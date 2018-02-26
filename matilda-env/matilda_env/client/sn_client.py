from aims_core.servicenow import servicenow_client as sn
from aims_virt.db import api as db_api

def get_cluster_master_info(cluster_name):
    return db_api.get_cluster_info(cluster_name)

def _prepare_sn_server_resp_payload(req_data, vm_data, status_info):
    req_data = req_data['request']
    resp = []
    master_resp = get_cluster_master_info(req_data['cluster_info']['cluster_name'])
    master_ip = None
    if master_resp is None or len(master_resp) == 0:
        master_ip = vm_data[0]['public_ip'], 'Active'
    else:
        pass
        #master_ip = master_resp[0].get('master_ip')
    for vm in vm_data:
        r = {}
        r['u_request_type'] = req_data.get('request_type')
        r['u_name'] = vm['name']
        r['u_cluster'] = req_data['cluster_info']['cluster_name']
        r['u_ip_address'] = vm['public_ip']
        r['install_status'] = status_info.get('status')
        r['u_is_virtual'] = 'true'
        r['u_provider'] = req_data['provider']
        r['u_tenant_name'] = req_data['cloud_auth'].get('tenant_name') or ''
        r['u_datacenter'] = req_data['cloud_auth'].get('datacenter') or ''
        r['u_server_size'] = req_data['cluster_info'].get('flavor_details').get('name') or ''
        r['u_project'] = req_data['cloud_auth'].get('tenant_name') or ''
        r['u_cpu_count'] = req_data['cluster_info'].get('flavor_details').get('vcpus') or ''
        r['u_disk_space_gb'] = req_data['cluster_info'].get('flavor_details').get('disk') or ''
        r['u_ram_mb'] = req_data['cluster_info'].get('flavor_details').get('ram') or ''
        r['u_authentication_url'] = req_data['cloud_auth'].get('auth_url') or ''
        r['u_username'] = req_data['cloud_auth'].get('username') or ''
        r['u_password'] = req_data['cloud_auth'].get('password') or ''
        r['u_access_key'] = req_data['cloud_auth'].get('access_key') or ''
        r['u_secret_key'] = req_data['cloud_auth'].get('secret_key') or ''
        r['u_operating_system'] = req_data['cluster_info'].get('image_details').get('image') or ''
        r['u_host'] = req_data['cloud_auth'].get('host') or ''
        r['u_esxi_host'] = req_data['cloud_auth'].get('esxi_hostname') or ''
        r['u_additional_storage'] = 'Yes'
        r['u_cluster_ip'] = master_ip
        r['u_status'] = status_info.get('vm_status')
        r['u_ritm_no'] = req_data['cluster_info'].get('ritm_no')
        resp.append(r)
    return resp

def send_server_data(req_data, vm_data, status_info):
    data = _prepare_sn_server_resp_payload(req_data, vm_data, status_info)
    status = sn.send_ip_data_to_sn(payload_list=data)
    if status.get('status_code') not in (200, 201):
        return False
    return status.get('status_code')

def prepare_update_vm_payload(ip, name, status, ritm_no=None):
    resp = {
	'u_request _type': 'Decommission a Server',
	'u_ip_address': ip,
	'u_status': status,
	'u_ritm_no': ritm_no

    }

def send_update_vm_status(ip, status, ritm_no=None):
    data = prepare_update_vm_payload(ip, None, status, ritm_no)
    status = sn.send_resp(data=data)
    if status.get('status_code') not in (200, 201):
        return False
    return status.get('status_code')