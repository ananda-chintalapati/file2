import os
import yaml
import jinja2

from matilda_env.client.jenkins import jenkins_client
from matilda_env.client.git_client.git_client import GitClient


REPO_PATH = '/opt/matilda/repo/matilda/'


def generate_playbook(app_id, service='tomcat', application=None, repo=''):
    print 'Policy file generation started for {} app'.format(app_id)
    policy_data = build_playbook(app_id, application)
    file_name = create_playbook_file(app_id, policy_data, repo)
    print 'File created at repo {} and ready to upload'.format(file_name)
    REPO_PATH, file = upload_file_to_repo(app_id, file_name, repo)
    print 'Policy file is available at {}/{}'.format(REPO_PATH, file)
    gc = GitClient()
    if gc.is_file_exist_in_repo(file):
        print 'File verification with git completed'
        return REPO_PATH, file
    return REPO_PATH, file_name


def build_playbook(app_id, application, service='tomcat'):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader("/opt/matilda/templates/cft")
    ).get_template("playbook_sample.yaml").render()

def create_playbook_file(app_id, data, path=None):
    print "Creating file at %r" % path
    if path == None:
        path = REPO_PATH

    file_name = app_id + '_Playbook.yaml'
    with open(path + file_name, 'w') as f:
        f.write(yaml.safe_dump(data, default_flow_style=False, default_style='', indent=4))
    print 'Policy creation completed'
    return file_name

def upload_file_to_repo(app_id, file, repo=None):
    if repo == None:
        repo = REPO_PATH
    file_list = [file]
    gc_client = GitClient()
    gc_client.commit_files_cmd(app_id, file_list, 'Playbook', repo)
    print 'File commit completed'
    return REPO_PATH, file
