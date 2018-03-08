import time

from matilda_env.client.jenkins.jenkins_client import JenkinsClient

def select_base_image():
    pass


def create_encrypted_img(app_id, org_name='VES', env='NonProd'):
    job_name = create_job(app_id, org_name, env)
    resp = trigger_job(job_name, env)
    job_status, build_no = wait_for_job_finish(job_name)
    if job_status == 'success':
        return extract_images(job_name, build_no)
    return None



def create_job(app_id, org_name='VES', env='NonProd'):
    parent_job = 'VES.EKYV.EncryptBASEAMI.NonProd'
    app_job = '.'.join([org_name, app_id, 'EncryptBASEAMI', env])
    jc = JenkinsClient()
    response = jc.clone_job(parent_job, app_job)
    return app_job

def trigger_job(job_name, env='NonProd'):
    args = {
        'ENV': env
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

def extract_images(job_name, build_no):
    jc = JenkinsClient()
    output = jc.get_build_console_output(job_name, build_no)
    lines = output.split('\n')
    regions = ['us-east-1', 'us-west-2']
    image_ids = []
    for line in lines:
        for region in regions:
            if regions in line:
                data = line.split(': ')
                img = {
                    data[0]: data[1]
                }
                image_ids.append(img)
    return image_ids