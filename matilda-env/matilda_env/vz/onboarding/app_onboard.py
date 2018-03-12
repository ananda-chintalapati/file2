from matilda_env.vz.onboarding import policy_builder as pb
from matilda_env.vz.onboarding import key_generator as kg
from matilda_env.vz.onboarding import ilm
from matilda_env.vz.onboarding import cft_generator as cg
from matilda_env.vz.onboarding import cft_executor as ce
from matilda_env.vz.onboarding import playbook_generator as pg


def onboard(app_info, ilm_info, cft_data):
    stash_url, file = pb.generate_policy_file(app_info['app_id'], app_info.get('policies'),
                                              app_info.get('instance_roles'), app_info.get('service_roles'))
    print 'Policy file generation completed'
    print 'Stash URL {} and File name {}'.format(stash_url, file)
    inst_role, roles, keys = kg.generate_keys(app_info['app_id'], file, stash_url, app_info.get('org_name'), app_info.get('env'),
                                   app_info.get('email_list') or 'shahrzad.amin@verizon.com')
    print 'KMS Keys generated'
    print 'Inst Profile {} Roles {} and Keys {}'.format(inst_role, roles, keys)
    print 'Initiating IMG Encryption'
    image_ids = ilm.create_encrypted_img(app_info['app_id'], app_info.get('org_name'), app_info.get('env'))
    print 'New Encrypted AMIs available'
    print 'Image IDs {}'.format(image_ids)
    img_id = image_ids['us-east-1']
    cft_data['image_id'] = img_id
    playbook = pg.generate_playbook(app_info['app_id'])
    run_cft(app_info, cft_data, image_ids, inst_role, playbook)



def run_cft(app_info, cft_data, image_ids, instance_profile, playbook=None):
    args = {
        'app_id': app_info.get('app_id'),
        'user_id': app_info.get('requestor'),
        'image_id': image_ids['us-east-1'],
        'name': cft_data.get('name'),
        'instance_profile': instance_profile,
        'sec_groups': cft_data.get('sec_groups'),
        'subnet_id': cft_data.get('subnet_id')
    }
    cft_file = cg.generate_cft_file(cft_data)
    print 'CFT file is generated at {}'.cft_file
    print 'Executing CFT to launch instances'
    args = {
        'playbook': playbook
    }
    resp = ce.run_cft(app_info['app_id'], cft_file, args)
    print 'CFT Execution response {}'.format(resp)



def get_roles(app_info):
    policies = app_info.get('policies')
    instance_role_ids = []
    service_role_ids = []
    instance_roles = []
    service_roles = []
    for policy in policies:
        if policy.get('role_type') == 'instance_role':
            if policy.get('role_id') in instance_role_ids:
                irole = None
                for r in instance_roles:
                    if r['ID'] == policy.get('role_id'):
                        r['Policies'].append(policy.get('name'))
                        break
            elif policy.get('role_id') in service_role_ids:
                srole = None
                for r in service_roles:
                    if r['ID'] == policy.get('role_id'):
                        r['Policies'].append(policy.get('name'))
                        break
            else:
                role = {
                    'ID': policy.get('role_id'),
                    'Policies': [policy.get('name')],
                    'PrincipalServices': policy.get('principal_services')
                }
