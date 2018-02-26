import jenkinsapi
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester

class JenkinsManager():

   def __init__(self, url, username, password):
      self.server = Jenkins(url, username='admin', password='jenkins', 
                      requester=CrumbRequester(baseurl=url, username='admin', password='jenkins'))

   def trigger_job(self, job_name, params=None):
      if self.server.has_job(job_name, params):
         self.server.build_job(job_name)

   def get_latest_build_info(self, job_name):
      job_instance = self.server.get_job(job_name)
      latest_build = job_instance.get_last_build()
      print latest_build, latest_build.get_status()
