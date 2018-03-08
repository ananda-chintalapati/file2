import time

from matilda_env.client.jenkins.jenkins_client import JenkinsClient

def generate_keys(app_id, policy_name, stash_url, org_name='VES', env='NonProd', email_list=''):
    job_name = create_job(app_id, org_name, env)
    resp = trigger_job(job_name, policy_name, stash_url, email_list)
    job_status, build_no = wait_for_job_finish(job_name)
    if job_status == 'success':
        keys, roles = extract_keys(job_name, build_no)
        return keys, roles
    return None

def create_job(app_id, org_name='VES', env='NonProd'):
    parent_job = 'VES.EKYV.PQPolicyBuilder-Template.DIT'
    app_job = '.'.join([org_name, app_id, 'PolicyBuilder', env])
    jc = JenkinsClient()
    response = jc.clone_job(parent_job, app_job)
    return app_job

def trigger_job(job_name, policy_name, stash_url, env='NonProd', acct='VES', email=''):
    args = {
        'Stash URL': stash_url,
        'ENV': env,
        'Policy-Specification-Filename': policy_name,
        'ACCT': acct,
        'Email': email
    }
    jc = JenkinsClient()
    response = jc.build_job_params(job_name, args)
    print 'Jenkins job response %r' % response
    return response

def wait_for_job_finish(job_name):
    job_status = 'Pending'
    build_no = 1
    retries = 1
    while(retries < 20):
        jc = JenkinsClient()
        last_build, response = jc.check_latest_build_status(job_name)
        job_status = response.lower()
        build_no = last_build
        time.sleep(60)
        if job_status == 'success' or job_status == 'failure':
            break
    return job_status, build_no

def extract_keys(job_name, build_no):
    jc = JenkinsClient()
    output = jc.get_build_console_output(job_name, build_no)
    lines = output.split('\n')
    roles = []
    keys_list = []
    for line in lines:
        keys = {}
        if 'arn:aws:iam' in line:
            data = line.split(': ')
            arg = {
                data[0]: data[1]
            }
            roles.append(arg)
        if 'KMS Key ARN:' in line:
            items = line.split(': ')
            if 'arn:aws:kms:us-east-1:' in items[1]:
                key = items[1].split('key/')
                keys['us-east-1'] = key[1]
            elif 'arn:aws:kms:us-west-2:' in items[1]:
                key = items[1].split('key/')
                keys['us-west-2'] = key[1]
            keys_list.append(keys)

    print 'Keys %s' % keys_list
    print 'Roles %s' % roles
    return keys_list, roles
