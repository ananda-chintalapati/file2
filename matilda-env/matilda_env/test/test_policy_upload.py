from matilda_env.client.git_client.git_client import GitClient
from matilda_env.vz.onboarding import policy_builder as pb

def test_policy_file():
    app_id = 'AB34'
    policies = [
        {'Name': 'Compute',
         'Services': ['ec2', 'efs']},
        {'Name': 'Database',
         'Services': ['rds']},
        {'Name': 'Compute2',
         'Services': ['lambda']}
    ]
    instance_roles = [
        {
            'ID': 'AB_ID',
            'Policies': ['Compute'],
            'PrincipalServices': ['ec2']
        }
    ]
    service_roles = [
        {
            'ID': 'AB_ID',
            'Policies': ['Compute'],
            'PrincipalServices': ['ec2']
        }
    ]

    repo = 'C:\Anand\workspace_matilda\\file2\\'
    file_name = pb.generate_policy_file(app_id, policies, instance_roles, service_roles, repo)

test_policy_file()