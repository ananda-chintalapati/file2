def create_network(task_flow, input_req, dependent_list):
    task_data = get_task('network', 'create')
    payload = {
        'auth': _get_auth(input_req),
        'network': {
            'name': input_req['network_details']['network'],
            'cidr': input_req['network_details']['env_ip_range'],
            'tenancy': 'default'
            }
        }
    net_task = task_flow.prepare_task(task_data, payload)
    task_flow.save_task(net_task)
    task_flow.add_task_list(net_task.task_id)
    depend_list = [
        {
            'task_id': net_task.task_id,
            'params': 'vpc_id',
            'type': 'network'
        }
    ]
    task_data = get_task('subnet', 'create', depend_list)
    subnet_task = task_flow.prepare_task(task_data, payload)
    task_flow.save_task(subnet_task)
    task_flow.add_task_list(subnet_task.task_id)
    return task_flow

def create_subnet(task_flow, input_req, dependent_list):
    pass

def get_task(component, action, depend_list=[]):
    task = {
        'component': component,
        'action': action,
        'name': component + '_' + action
    }
    if len(depend_list) > 0:
        task['depend_list'] = []
        for item in depend_list:
            task['depend_list'].append(item)
    return task

def _get_auth(payload):
    return {
        'aws_access_key': payload['cloud_auth']['aws_accesskey'] or 'AKIAIAHYTLHZZDTHVEZA',
        'aws_secret_key': payload['cloud_auth']['aws_secret'] or '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',
        'region': payload['cloud_auth']['aws_region'] or 'us-west-2'
    }