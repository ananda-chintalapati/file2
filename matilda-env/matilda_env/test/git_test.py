from matilda_env.client.git_client import git_client as gc

def test_git_push():
    repo = 'C:\Anand\workspace_matilda\\file2'
    file = [
        'C:\Anand\workspace_matilda\\file2\AB23_Policy.json'
    ]
    gc_client = gc.GitClient()
    gc_client.commit_files('abcd', file, repo)

test_git_push()