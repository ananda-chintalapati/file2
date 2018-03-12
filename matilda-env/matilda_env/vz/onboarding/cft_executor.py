import time
import random

from matilda_env.client.jenkins.jenkins_client import JenkinsClient

def run_cft(app_id, cft_name, args, org_name='VES', env='NonProd'):
    print 'CFT execution started'
    job_name = create_job(app_id, org_name, env)
    resp = trigger_job(app_id, job_name, cft_name, args)
    job_status, build_no = wait_for_job_finish(job_name)
    print 'CFT execution completed'
    return job_status

def create_job(app_id, org_name='VES', env='NonProd'):
    parent_job = 'VES.EKYV.InstanceLaunch.NonProd'
    app_job = '.'.join([org_name, app_id, 'InstanceLaunch', env])
    print 'Cloning job {}'.format(app_job)
    jc = JenkinsClient()
    response = jc.create_job_in_view(parent_job, app_job)
    print 'Job Cloning completed'
    return app_job

def trigger_job(app_id, job_name, cft_name, args):
    print 'Triggering job {}'.format(job_name)
    args = {
        'AppID': args.get('app_id') or app_id,
        'StackName': args.get('stack_name') or get_stack_name(args.get('app_id')),
        'AWS_REGION': args.get('region') or 'us-east-1',
        'StashRepoUrl': 'https://v678508@onestash.verizon.com/scm/ek/matilda.git',
        'CloudFormationTemplate': cft_name,
        'ANSIBLE_PLAYBOOK': args.get('playbook')
    }
    jc = JenkinsClient()
    response = jc.build_param_job_cmd(job_name, args)
    print 'Jenkins job response %r' % response
    return response

def get_stack_name(app_id):
    return 'VZ-' + app_id + 'Matilda' + str(random.randint(1, 99))


def wait_for_job_finish(job_name):
    print 'Tracking {} job'.format(job_name)
    job_status = 'Pending'
    build_no = 1
    retries = 1
    while(retries < 20):
        print 'Retry : {}, Job Status: {}, Build No: {}'.format(retries, job_status, build_no)
        jc = JenkinsClient()
        last_build, response = jc.check_latest_build_status(job_name)
        job_status = response.lower()
        build_no = last_build
        time.sleep(60)
        if job_status == 'success' or job_status == 'failure':
            break
    print 'Job Status: {}, Build No: {}'.format(job_status, build_no)
    return job_status, build_no

