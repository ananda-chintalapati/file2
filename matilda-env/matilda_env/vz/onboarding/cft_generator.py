import getpass
import jinja2


from matilda_env.client.git_client.git_client import GitClient

REPO_PATH = '/opt/matilda/repo/matilda/'

def generate_cft_file(args, repo=REPO_PATH):
    cft_data = prepare_cft(args)
    file_path = create_cft_file(args.get('app_id'), cft_data, repo)
    REPO_PATH, file = upload_file_to_repo(args.get('app_id'), file_path, repo)
    return REPO_PATH, file

def create_cft_file(app_id, data, path=REPO_PATH):
    print "Creating file at %r" % path
    file_name = path + app_id + '_CFT.json'
    with open(file_name, 'w') as f:
        f.write(data)
    return file_name


def prepare_cft(args):
    args = {
        "app_id": args.get('app_id'),
        "user_id": args.get('user_id') or getpass.getuser(),
        "instance_name": args.get('name'),
        "instance_profile": args.get('instance_profile') or 'VzPol-profile-NonProd-VES-NP-EKYV-EC2',
        "sec_groups": args.get('sec_groups') or ["sg-85840ef4","sg-5ef8382d","sg-8a911ff5","sg-ab8ee5d5"],
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
