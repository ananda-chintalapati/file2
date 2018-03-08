from matilda_env.vz.onboarding import policy_builder as pb


def test_policy_file():
    app_id = 'ABCD'
    policies = [
        {'Name': 'Compute',
         'Services': ['ec2', 'efs']}
    ]
    instance_roles = [
        {
            'ID': 'AB_ID',
            'Policies': ['Compute'],
            'PrincipalServices': ['ec2']
        }
    ]

    pb.generate_policy_file(app_id, policies, instance_roles, None)

test_policy_file()