import os
import yaml

from collections import OrderedDict

from matilda_env.client.jenkins import jenkins_client
from matilda_env.client.git_client.git_client import GitClient


REPO_PATH = '/opt/matilda/repo/matilda/'


def generate_policy_file(app_id, policies, instance_roles, service_roles, repo=''):
    print 'Policy file generation started for {} app'.format(app_id)
    policy_data = build_poilcy_file(app_id, policies, instance_roles, service_roles)
    file_path = create_policy_file(app_id, policy_data, repo)
    print 'File created at repo {} and ready to upload'.format(file_path)
    REPO_PATH, file = upload_file_to_repo(app_id, file_path, repo)
    print 'Policy file is available at {}/{}'.format(REPO_PATH, file)
    gc = GitClient()
    if gc.is_file_exist_in_repo(file):
        print 'File verification with git completed'
        return REPO_PATH, file
    return REPO_PATH, file


def build_poilcy_file(app_id, policies, instance_roles, service_roles):
    policy_data = OrderedDict()
    policy_data['ApplicationId'] = app_id
    policy_data['Policies'] = policies

    if instance_roles != None and len(instance_roles) > 0:
        policy_data['InstanceRoles'] = instance_roles
    if service_roles != None and len(service_roles) > 0:
        policy_data['ServiceRoles'] = service_roles
    print 'Generated Policy %r' % dict(policy_data)
    return dict(policy_data)

def create_policy_file(app_id, data, path=None):
    print "Creating file at %r" % path
    if path == None:
        path = REPO_PATH

    file_name = path + app_id + '_Policy.json'
    with open(file_name, 'w') as f:
        f.write(yaml.safe_dump(data, default_flow_style=False, default_style='', indent=4))
    print 'Policy creation completed'
    return path

def upload_file_to_repo(app_id, file, repo=None):
    if repo == None:
        repo = REPO_PATH
    file_list = [file]
    gc_client = GitClient()
    gc_client.commit_files_cmd(app_id, file_list, 'Policy', repo)
    print 'File commit completed'
    return REPO_PATH, file
