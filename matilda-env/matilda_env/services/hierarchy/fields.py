
server = {
    'create': {
        'mandatory': ['name', 'image', 'network_id', 'flavor'],
        'optional': ['sec_groups']
    },
    'update': {
        'mandatory': ['instance_id', 'public_ip'],
        'optional': []
    }
}

network = {
    'create': {
        'mandatory': ['name', 'cidr'],
        'optional': ['sec_groups']
    },
    'update': {
        'mandatory': ['network_id', 'cidr'],
        'optional': []
    }
}

security_group = {
    'create': {
        'mandatory': ['name'],
        'optional': []
    },
    'update': {
        'mandatory': ['sec_group_id', 'cidr'],
        'optional': []
    }
}

subnet = {
    'create': {
        'mandatory': ['name', 'network_id', 'cidr'],
        'optional': []
    },
    'update': {
        'mandatory': ['subnet_id', 'cidr'],
        'optional': []
    }
}