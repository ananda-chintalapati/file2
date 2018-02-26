from matilda_env.task.v1.task_builder import TaskFlowBuilder

def prepare_tasks(payload):
    task_flow = TaskFlowBuilder()
    task_flow.set_metadata({'request_no': payload['request_no'], 'ritm_no': payload['ritm_no']})
    net_task = None
    sec_group_task = None
    subnet_task = None
    instance_task = None
    if payload['network_info'] != None:
        task_data = get_task('network', 'create')
        net_task = task_flow.prepare_task(task_data, payload)
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
        task_flow.add_task_list(subnet_task.task_id)
    if payload['firewall_info'].get('array_string') != None:
        depend_list = [
            {
                'task_id': net_task.task_id,
                'params': 'vpc_id',
                'type': 'network'
            }
        ]
        task_data = get_task('security_group', 'create', depend_list)
        sec_group_task = task_flow.prepare_task(task_data, payload)
        task_flow.add_task_list(sec_group_task.task_id)
    if payload['server_info'] != None:
        depend_list = [
            {
                'task_id': net_task.task_id,
                'params': 'vpc_id',
                'type': 'network'
            },
            {
                'task_id': sec_group_task.task_id,
                'params': 'group_id',
                'type': 'security_group'
            },
            {
                'task_id': subnet_task.task_id,
                'params': 'subnet_id',
                'type': 'subnet'
            }
        ]
        task_data = get_task('instance', 'create', depend_list)
        instance_task = task_flow.prepare_task(task_data, payload)
        task_flow.add_task_list(instance_task.task_id)
    if payload['server_info']['quantity'] > 1:
        depend_list = [
            {
                'task_id': instance_task.task_id,
                'params': 'instance_id',
                'type': 'instance'
            },
            {
                'task_id': subnet_task.task_id,
                'params': 'subnet_id',
                'type': 'subnet'
            }
        ]
        task_data = get_task('lb', 'create', depend_list)
        lb_task = task_flow.prepare_task(task_data, payload)
        task_flow.add_task_list(lb_task.task_id)
    if payload['service_info'] != None:
        depend_list = [
            {
                'task_id': instance_task.task_id,
                'params': 'public_ip',
                'type': 'instance'
            }
        ]
        task_data = get_task('service', 'create', depend_list)
        lb_task = task_flow.prepare_task(task_data, payload)
        task_flow.add_task_list(lb_task.task_id)

    task_flow.save()
    return task_flow
