from matilda_env.vz.onboarding import policy_builder as pb
from matilda_env.vz.onboarding import key_generator as kg
from matilda_env.vz.onboarding import ilm


def onboard(app_info, ilm_info, cft_data):
    stash_url, file = pb.generate_policy_file(app_info['app_id'], app_info.get('policies'),
                                              app_info('instance_roles'), app_info.get('service_roles'))
    print 'Policy file generation completed'
    print 'Stash URL {} and File name {}'.format(stash_url, file)
    roles, keys = kg.generate_keys(app_info['app_id'], file, stash_url, app_info.get('org_name'), app_info.get('env'),
                                   app_info.get('email_list'))
    print 'KMS Keys generated'
    print 'Roles {} and Keys {}'.format(roles, keys)
    image_ids = ilm.create_encrypted_img(app_info['app_id'], app_info.get('org_name'), app_info.get('env'))
    print 'New Encrypted AMIs available'
    print 'Image IDs {}'.format(image_ids)

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
