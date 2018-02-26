from matilda_env.services.portable import transfer

def test_transfer():
    src_file = 'rest_tester.py'
    target_dir = '/tmp'
    target_file = 'rest_tester.py'

    resp = transfer.transfer_file(src_file, target_file, target_dir, '192.168.20.208', '22', 'root', 'openstack')
    print resp

test_transfer()