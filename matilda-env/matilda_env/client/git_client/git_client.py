import os
import subprocess
from git import Repo

class GitClient():

    def __init__(self):
        self.repo_dir = '/opt/matilda/repo/matilda'

    def commit_files(self, app_id, file_list, repo_dir=None):
        if repo_dir == None:
            repo_dir = '/opt/matilda/repo/matilda'
        repo = Repo(repo_dir)
        commit_message = '{} Policy file'.format(app_id)
        repo.index.add(file_list)
        repo.index.commit(commit_message)
        origin = repo.remote('origin')
        origin.push()

    def commit_files_cmd(self, app_id, file_list, type, repo_dir=None):
        if repo_dir == None:
            repo_dir = self.repo_dir
        for item in file_list:
            self.run_cmd('git add {}'.format(item), repo_dir)
        commit_msg = '{} {} File'.format(app_id, type)
        self.run_cmd('git commit -m "{}"'.format(commit_msg), repo_dir)
        out, err = self.run_cmd('git push origin master', repo_dir)
        return out, err

    def is_file_exist_in_repo(self, file_name, repo_dir=None):
        if repo_dir == None:
            repo_dir = self.repo_dir
        cmd = 'git ls-tree -r HEAD~1 --name-only'
        resp = self.run_cmd(cmd, repo_dir)
        for item in resp:
            if file_name in item:
                return True
        return False


    def run_cmd(self, cmd, repo_dir):
        p = subprocess.Popen(cmd, cwd=repo_dir, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        return stdout, stderr

