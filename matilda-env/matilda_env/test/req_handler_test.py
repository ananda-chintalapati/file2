from matilda_env.services.env_executor.v1 import req_handler

def test_policy_script():
    pol_ip = [{
            "Name": "Compute",
            "Services": "ec2, efs, ebs",
            "role": "role1",
            "role_type": "Instance Role",
            "principal_services": "ec2"
        }, {
            "Name": "DB",
            "Services": "rds",
            "role": "role2",
            "role_type": "Service Role",
            "principal_services": "rds"
        }]

    resp = req_handler.prepare_policies(pol_ip)

    print resp

test_policy_script()