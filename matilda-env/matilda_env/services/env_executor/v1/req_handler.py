import os
import json

from matilda_env.vz.onboarding import app_onboard


def prepare_backend_req(req_id):
    app_info = {}
    cft_data = {}
    path = '/opt/matilda/requests/' + req_id
    with open(path + 'policy.json', 'r') as f:
        d = json.load(f)
        env_data = d.get('env_conf')
        app_info = {
            'region': env_data.get('region') or 'us-east-1',
            'app_id': env_data.get('app_id'),
            'org_name': env_data.get('org_name'),
            'acct_name': env_data.get('acct_name')
        }
        req_policies = env_data.get('policy_info').get('policies')
        mod_pol, inst_role, serv_role = prepare_policies(req_policies)
        app_info['policies'] = mod_pol
        app_info['instance_roles'] = inst_role
        app_info['serv_roles'] = serv_role


    with open(path + 'cft.json', 'r') as f:
        d = json.load(f)
        cloud_data = d.get('cloud_info')
        cft_data = {
            'image_id': cloud_data.get('select_image'),
            'name': cloud_data.get('instance_name'),
            'sec_groups': cloud_data.get('security_array'),
            'volumes': cloud_data.get('volume_info')
        }

    app_onboard.onboard(app_info, None, cft_data)

def prepare_policies(req_policies):
    policies = []
    roles = []
    policy_ids = []
    role_ids = {
        'instance_roles': [],
        'service_roles': []
    }

    instance_roles = []
    service_roles = []
    for item in req_policies:
        policy = {
            "Name": item.get('Name'),
            "Services": [item.get('Services')]
        }
        policy_ids.append(item.get('Name'))
        policies.append(policy)

        if item.get('role_type') == 'Instance Role':
            if item.get('role') in role_ids['instance_roles']:
                for irole in instance_roles:
                    if irole.get['ID'] == item.get('role'):
                        irole.get['Policies'].append(item.get('Name'))
            else:
                new_role = {
                    'ID': item.get('role'),
                    'Policies': [item.get('Name')]

                }
                instance_roles.append(new_role)
                role_ids['instance_roles'].append(item.get('role'))
        else:
            if item.get('role') in role_ids['service_roles']:
                for irole in service_roles:
                    if irole.get['ID'] == item.get('role'):
                        irole.get['Policies'].append(item.get('Name'))
            else:
                new_role = {
                    'ID': item.get('role'),
                    'Policies': [item.get('Name')]

                }
                service_roles.append(new_role)
                role_ids['service_roles'].append(item.get('role'))
    return policies, instance_roles, service_roles