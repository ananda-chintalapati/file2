import getpass
import jenkins
import requests

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



