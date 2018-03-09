
from matilda_env.vz.onboarding import cft_generator as cg
from matilda_env.vz.onboarding import cft_executor as ce

def test_create_cft():
    args = {
        "app_id": 'AB15',
        "instance_name": 'Matilda10',
        "image_id": 'ami-0700067d',
        "subnet_id": 'subnet-77440712'
    }

    cg.generate_cft_file(args)

def test_run_cft():
    args = {

    }
    ce.run_cft('AB15')

test_create_cft()