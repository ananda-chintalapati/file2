from matilda_env.client.jenkins.jenkins_client import JenkinsClient

url = 'http://localhost:3000'
user = 'admin'
token = '5b9575fb7ed9cfa8f0e4def647e9ddb2'

def test_job_info():
    jc = JenkinsClient(url, user, token)
    response = jc.get_job_info('mat_sample_build')
    print response
    last_build = response['lastBuild']['number']
    print last_build
    test_build_info(last_build)

def test_build_info(build_no=1):
    jc = JenkinsClient(url, user, token)
    response = jc.get_build_info('mat_sample_build', build_no)
    print response
    print response['result']
    test_console_output(build_no)

def get_ip_from_output(text):
    pass

def test_console_output(build_no=1):
    jc = JenkinsClient(url, user, token)
    response = jc.get_build_console_output('mat_sample_build', build_no)
    print response
    with open('output.txt', 'w') as f:
        f.write(response)
    data2 = response.split('\n')
    data = open('output.txt', 'r')
    resp = []
    for line in data:
        print line
        if 'File encoding' in line:
            resp.append(line)
    print 'Resp %r ' % resp[0]

    for item in data2:
        if 'File encoding' in item:
            print 'New one %r' % item


def build_job():
    jc = JenkinsClient(url, user, token)
    response = jc.build_job_params('mat_sample_build', None)
    print response


def test_job_curl():
    jc = JenkinsClient(url, user, token)
    print jc.get_job_info_curl('mat_sample_build')

def test_job_with_params():
    jc = JenkinsClient(url, user, token)
    params = {
        'name': 'test2',
        'city': 'frisco',
        'state': 'texas'
    }
    print jc.build_job_params('param_test', params)

def test_job_clone():
    jc = JenkinsClient(url, user, token)
    print jc.clone_job('param_test', 'param_test_clone')

#test_job_info()
#build_job()
#test_job_curl()

test_job_with_params()

#test_job_clone()