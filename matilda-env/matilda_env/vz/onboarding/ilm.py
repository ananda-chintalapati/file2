import time

from matilda_env.client.jenkins.jenkins_client import JenkinsClient
from matilda_env.vz.onboarding import jenkins_console_reader as jcr

def select_base_image():
    pass


def create_encrypted_img(app_id, org_name='VES', env='NonProd'):
    print 'Create encrypted image'
    job_name = create_job(app_id, org_name, env)
    resp = trigger_job(job_name, env)
    job_status, build_no = wait_for_job_finish(job_name)
    if job_status == 'success':
        return extract_images(job_name, build_no)
    return None



def create_job(app_id, org_name='VES', env='NonProd'):
    parent_job = 'VES.EKYV.EncryptBASEAMI.NonProd'
    app_job = '.'.join([org_name, app_id, 'EncryptBASEAMI', env])
    print 'Cloning job {}'.format(app_job)
    jc = JenkinsClient()
    response = jc.clone_job(parent_job, app_job)
    print 'Job clone completed {}'.format(response)
    return app_job

def trigger_job(job_name, env='NonProd'):
    print 'Triggering job {}'.format(job_name)
    args = {
        'ENV': env
    }
    jc = JenkinsClient()
    response = jc.build_param_job_cmd(job_name, args)
    print 'Jenkins job response %r' % response
    return response

def wait_for_job_finish(job_name):
    print 'Checking job status {}'.format(job_name)
    job_status = 'Pending'
    build_no = 1
    retries = 1
    while(retries < 30):
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

def extract_images(job_name, build_no):
    jc = JenkinsClient()
    output = jc.get_build_console_output(job_name, build_no)
    print 'Console output of AMI build {}'.format(output)
    image_ids = jcr.get_ami_ids(output)
    print 'Image ids {}'.format(image_ids)
    return image_ids