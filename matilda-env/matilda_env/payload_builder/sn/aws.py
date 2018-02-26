def prepare_payload(component, action, payload, instance_ids=None):
    if component == 'instance':
        return create_instance(payload)
    elif component == 'network':
        return create_network(payload)
    elif component == 'subnet':
        return create_subnet(payload)
    elif component == 'lb':
        return create_lb(payload, instance_ids)
    elif component == 'security_group':
        return create_sec_group(payload)

def create_instance(payload):
    req = {
        "action": "create",
        "req_id": payload['request_no'],
        "component": "instance",
        "provider": "aws",
        "auth": {
            "aws_access_key": payload['auth']['aws_access_key'],
            "aws_secret_key": payload['auth']['aws_secret_key'],
            "region": payload['auth']['region']
        },
        "args": {
            "flavor": payload['flavor_details']['flavor'],
            "image_id": payload['image_details']['image'],
            "count": payload['server_info']['quantity'],
            "key_name": payload['server_info'].get('key'),
            "init_scripts": payload['server_info'].get('init_scripts'),
            "name": payload['server_info']['server_name']
        }
    }
    return req


def create_network(payload):
    req = {
        "action": "create",
        "req_id": payload['request_no'],
        "component": "network",
        "provider": "aws",
        "auth": {
            "aws_access_key": payload['auth']['aws_access_key'],
            "aws_secret_key": payload['auth']['aws_secret_key'],
            "region": payload['auth']['region']
        },
        "args": {
            "name": payload['network_info']['name'],
            "cidr": payload['network_info']['env_ip_range']
        }
    }
    return req

def create_subnet(payload):
    req = {
        "action": "create",
        "req_id": payload['request_no'],
        "component": "network",
        "provider": "aws",
        "auth": {
            "aws_access_key": payload['auth']['aws_access_key'],
            "aws_secret_key": payload['auth']['aws_secret_key'],
            "region": payload['auth']['region']
        },
        "args": {
            "network_id": payload['network_info']['network'],
            "cidr": payload['network_info']['env_sub_net_range']
        }
    }
    return req

def create_lb(payload, instance_ids=None):
    req = {
        "action": "create",
        "req_id": payload['request_no'],
        "component": "network",
        "provider": "aws",
        "auth": {
            "aws_access_key": payload['auth']['aws_access_key'],
            "aws_secret_key": payload['auth']['aws_secret_key'],
            "region": payload['auth']['region']
        },
        "args": {
            "zones": payload['auth'].get('zones'),
            "name": payload['server_info']['server_name'] + '_elb',
            "instance_ids": instance_ids
        }
    }
    return req


def create_sec_group(payload):
    req = {
        "action": "create",
        "req_id": payload['request_no'],
        "component": "network",
        "provider": "aws",
        "auth": {
            "aws_access_key": payload['auth']['aws_access_key'],
            "aws_secret_key": payload['auth']['aws_secret_key'],
            "region": payload['auth']['region']
        },
        "args": {
            "vpc_id": payload['auth'].get('zones'),
            "name": payload['firewall_info'].get('name'),
            "rules": []
        }
    }
    return req
