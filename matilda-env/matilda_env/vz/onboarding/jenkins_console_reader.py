
def get_role_alias(data):
    for line in data.split('\n'):
        if 'instance-profile' in line:
            data = line.split('instance-profile/')
            return data[1]
    return None

def get_ami_ids(data):
    resp = {}
    for line in data.split('\n'):
        if '"us-east-1": "ami' in line:
            data = line.split('"us-east-1": ')
            resp['us-east-1'] = find_between(data[1], '"', '"')
        elif '"us-west-2": "ami' in line:
            data = line.split('"us-west-2": ')
            resp['us-west-2'] = find_between(data[1], '"', '"')
    return resp

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
