import getpass
import jinja2
import json


from matilda_env.client.git_client.git_client import GitClient

REPO_PATH = '/opt/matilda/repo/matilda/'

def generate_cft_file(args, repo=REPO_PATH):
    cft_data = get_cft_data(args)
    file_path = create_cft_file(args.get('app_id'), cft_data, repo)
    REPO_PATH, file = upload_file_to_repo(args.get('app_id'), file_path, repo)
    return REPO_PATH, file

def create_cft_file(app_id, data, path=REPO_PATH):
    print "Creating file at %r" % path
    file_name = path + app_id + '_CFT.json'
    with open(file_name, 'w') as f:
        f.write(data)
    return file_name


def get_cft_data(args, template='/opt/matilda/templates/cft/cft_template.json'):
    base_template = None
    with open(template, 'r') as f:
        base_template = json.load(f)
    base_template['Resources']['EC2Instance']['Properties']['BlockDeviceMappings'] = base_template['Resources']\
                                                                                         ['EC2Instance']['Properties']['BlockDeviceMappings'][0:1]
    if 'volumes' in args.keys():
        for item in args['volumes']:
            vol = {
                "DeviceName": item.get('device_name'),
                "Ebs": {
                    "VolumeSize": item.get('size') or "60",
                    "DeleteOnTermination": True,
                    "VolumeType": "gp2"
                }
            }
            base_template['Resources']['EC2Instance']['Properties']['BlockDeviceMappings'].append(vol)
    base_template['Parameters']['AppID']['Default'] = args.get('app_id')
    base_template['Parameters']['UserID']['Default'] = args.get('user_id') or getpass.getuser(),
    base_template['Parameters']['InstanceName']['Default'] = args.get('name'),
    base_template['Parameters']['IAMInstanceProfile']['Default'] = args.get('instance_profile') or \
                                                                   'VzPol-profile-NonProd-VES-NP-'+ args.get('app_id') +'-SD_EC2',
    base_template['Parameters']['SecurityGroupIds']['Default'] = args.get('sec_groups') or "sg-85840ef4,sg-5ef8382d,sg-8a911ff5,sg-ab8ee5d5",
    base_template['Parameters']['ImageID']['Default'] = args.get('image_id') or 'ami-0700067d',
    base_template['Parameters']['SubnetID']['Default'] = args.get('subnet_id') or 'subnet-77440712'
    return base_template



def prepare_cft(args):
    args = {
        "app_id": args.get('app_id'),
        "user_id": args.get('user_id') or getpass.getuser(),
        "instance_name": args.get('name'),
        "instance_profile": args.get('instance_profile') or 'VzPol-profile-NonProd-VES-NP-EKYV-EC2',
        "sec_groups": args.get('sec_groups') or "sg-85840ef4,sg-5ef8382d,sg-8a911ff5,sg-ab8ee5d5",
        "image_id": args.get('image_id') or 'ami-0700067d',
        "subnet_id": args.get('subnet_id') or 'subnet-77440712'
    }

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader("/opt/matilda/templates/cft")
    ).get_template("cft_template.json").render(args)

def upload_file_to_repo(app_id, file, repo=None):
    if repo == None:
        repo = REPO_PATH
    file_list = [file]
    gc_client = GitClient()
    gc_client.commit_files_cmd(app_id, file_list, 'CFT', repo)
    return REPO_PATH, file
