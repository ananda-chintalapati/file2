import time

from matilda_env.client.jenkins.jenkins_client import JenkinsClient

def trigger_instance_job(args={}):
    params = {
        'AppID': 'EKYV',
        'StackName': 'VZ-EKYV-PQ-Matilda-Feb2018-remote-creation',
        'Role': 'App',
        'IAMInstanceProfile': 'VzPol-profile-NonProd-VES-NP-EKYV-EC2',
        'AWS_REGION': 'us-east-1',
        'SecurityGroupIds': 'sg-5f83e821',
        'ENV': 'NONPROD',
        'ImageID': args.get('image') or 'ami-0700067d',
        'SubnetID': 'subnet-77440712',
        'StashRepoUrl': 'https://v678508@onestash.verizon.com/scm/ek/sample_repo.git',
        'CloudFormationTemplate': 'EKYV-Matilda-CFT.json',
        'InstanceName': args.get('name') or 'VZ-EKYV-PQ-Matilda-Feb2018-remote-creation',
        'InstanceType': args.get('flavor') or 't2.xlarge'
    }

    job_name = 'VES.EKYV.PQT.InstanceLaunch.NonProd'
    jc = JenkinsClient()
    response = jc.build_job_params(job_name, params)
    print 'Jenkins job response %r' % response
    return response

def check_latest_build_status(job_name):
    jc = JenkinsClient()
    job_info = jc.get_job_info(job_name)
    last_build = job_info['lastBuild']['number']
    response = jc.get_build_info(job_name, last_build)
    return last_build, response['result']


def get_instance_console_output(job_name, build_no):
    jc = JenkinsClient()
    output_str = jc.get_build_console_output(job_name, build_no)
    return output_str

def extract_ip_from_output(data):
    lines = data.split('\n')
    ip_string = None
    for line in lines:
        if 'IP' in line:
            ip_string = line
            break
    print 'IP Address %s' % ip_string
    ip = ip_string.split(':')
    if len(ip) > 1:
        return ip[1]
    return ip

def create_instance(name, flavor):
    args = {
        'name': name,
        'flavor': flavor
    }
    job_name = 'VES.EKYV.PQT.InstanceLaunch.NonProd'
    trigger_response = trigger_instance_job(args)
    print 'Trigger response %s' % trigger_response
    job_status = 'Pending'
    build_no = 1
    while(job_status.lower() == 'success' or job_status.lower() == 'failure'):
        last_build, response = check_latest_build_status(job_name)
        job_status = response
        build_no = last_build
        time.sleep(60)
    console_output = get_instance_console_output(job_name, build_no)
    print 'Console Output %s' % console_output
    ip_address = extract_ip_from_output(console_output)
    print 'IP address %s' % ip_address
    return ip_address

