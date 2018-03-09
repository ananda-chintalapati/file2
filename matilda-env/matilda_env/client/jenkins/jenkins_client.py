import getpass
import jenkins
import requests
import subprocess

class JenkinsClient():

    def __init__(self, url=None, user=None, token=None):
        if url == None:
            self.url = 'https://onejenkins.verizon.com/ves'
        else:
            self.url = url
        self.user = user
        if user == None:
            self.user = getpass.getuser()
        self.token = token
        if token == None:
            self.token = '24a8cccc018b3f4c493333c91a2478a0'
        self.jenkins = jenkins.Jenkins(self.url, username=self.user, password=self.token)


    def get_job_info(self, job_name):
        return self.jenkins.get_job_info(job_name)

    def get_build_info(self, job_name, build_no):
        return self.jenkins.get_build_info(job_name, build_no)

    def build_job_params(self, job_name, params, token=None):
        if token == None:
            token = self.token
        response = self.jenkins.build_job(job_name, params, token)
        return response

    def get_build_console_output(self, name, number):
        return self.jenkins.get_build_console_output(name, number)

    def get_job_info_curl(self, job_name):
        user = self.user + ':' + self.token
        url = self.url + '/job/' + job_name + '/api/json'
        response = requests.get(url, auth=(self.user, self.token))
        print 'Response %r' % response.json()

    def build_param_job_curl(self, job_name):
        user = self.user + ':' + self.token
        url = self.url + '/job/' + job_name + '/build/json'
        response = requests.get(url, auth=(self.user, self.token))
        print 'Response %r' % response.json()

    def build_param_job_cmd(self, job_name, params):
        user = self.user + ':' + self.token
        url = self.url + '/job/' + job_name + '/buildWithParameters?token=' + self.token
        query_str = '&'
        for k, v in params.iteritems():
            if v != None and v != '':
                query_str = query_str + k + '=' + v + '&'
        url = url + query_str
        cmd = 'curl -v -u {} {}'.format(user, url)
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        resp = p.communicate()
        print p[0], p[1]
        return resp

    def clone_job(self, from_job, to_job):
        from_job_xml = self.get_job_config(from_job)
        resp = self.jenkins.create_job(to_job, from_job_xml)
        return resp

    def get_job_config(self, job_name):
        return self.jenkins.get_job_config(job_name)

    def check_latest_build_status(self, job_name):
        job_info = self.jenkins.get_job_info(job_name)
        last_build = job_info['lastBuild']['number']
        response = self.jenkins.get_build_info(job_name, last_build)
        return last_build, response['result']

    def create_job_in_view(self, from_job, job_name):
        from_job_xml = self.get_job_config(from_job)
        user = self.user + ':' + self.token
        url = self.url + '/view/EKYV-Automation/view/Matilda/createItem?name=' + job_name
        response = requests.get(url, auth=(self.user, self.token), data=from_job_xml)
        print 'Response %r' % response.json()




