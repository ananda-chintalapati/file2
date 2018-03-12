from matilda_env.vz.onboarding import app_onboard

def test_app_onboarding():
    app_id = 'EICV'
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
    service_roles = []

    app_info = {
        'app_id': app_id,
        'policies': policies,
        'instance_roles': instance_roles,
        'service_roles': service_roles
    }

    cft_data = {
        "app_id": app_id,
        "instance_name": 'Matilda10',
        "image_id": 'ami-0700067d',
        "subnet_id": 'subnet-77440712'
    }

    app_onboard.onboard(app_info, None, cft_data)

test_app_onboarding()