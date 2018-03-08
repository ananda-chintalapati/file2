import os
import subprocess
from git import Repo

class GitClient():

    def __init__(self):
        pass

    def commit_files(self, app_id, file_list, repo_dir=None):
        if repo_dir == None:
            repo_dir = '/opt/matilda/repo/matilda'
        repo = Repo(repo_dir)
        commit_message = '{} Policy file'.format(app_id)
        repo.index.add(file_list)
        repo.index.commit(commit_message)
        origin = repo.remote('origin')
        origin.push()

    def commit_files_cmd(self, app_id, file_list, repo_dir=None):
        if repo_dir == None:
            repo_dir = '/opt/matilda/repo/matilda'
        for item in file_list:
            self.run_cmd('git add {}'.format(item), repo_dir)
        commit_msg = '{} Policy File'.format(app_id)
        self.run_cmd('git commit -m "{}"'.format(commit_msg), repo_dir)
        self.run_cmd('git push origin master', repo_dir)

    def run_cmd(self, cmd, repo_dir):
        p = subprocess.Popen(cmd, cwd=repo_dir, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.communicate()

