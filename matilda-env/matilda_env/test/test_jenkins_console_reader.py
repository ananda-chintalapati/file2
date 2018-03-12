from matilda_env.vz.onboarding import jenkins_console_reader as jcr

def test_policy_reader():
    with open('policy_output.txt', 'r') as f:
        data = f.read()

    print jcr.get_role_alias(data)

def test_ami_ids():
    data = """
    TASK [epilogue : Display image IDs of encrypted AMIs] **************************
ok: [localhost] => {
    "changed": false, 
    "image_ids": {
        "NONPROD": {
            "us-east-1": "ami-0700067d", 
            "us-west-2": "ami-23308b5b"
        }
    }
}
    """

    print jcr.get_ami_ids(data)

test_policy_reader()
test_ami_ids()