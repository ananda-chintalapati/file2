from matilda_env.vz.onboarding import key_generator

def test_output():
    with open('key.txt', 'r') as content_file:
        content = content_file.read()

    lines = content.split('\n')
    roles = []
    keys_list = []
    for line in lines:
        keys = {}
        if 'arn:aws:iam' in line:
            data = line.split(': ')
            arg = {
                data[0]: data[1]
            }
            roles.append(arg)
        if 'KMS Key ARN:' in line:
            items = line.split(': ')
            if 'arn:aws:kms:us-east-1:' in items[1]:
                key = items[1].split('key/')
                keys['us-east-1'] = key[1]
            elif 'arn:aws:kms:us-west-2:' in items[1]:
                key = items[1].split('key/')
                keys['us-west-2'] = key[1]
            keys_list.append(keys)

    print 'Keys %s' % keys_list
    print 'Roles %s' % roles

test_output()