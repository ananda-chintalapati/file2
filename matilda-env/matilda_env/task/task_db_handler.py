import datetime

from matilda_env.db import api as db_api

def create_task(self, task_flow_id, name, payload, depend_list, component, action):
    args = {
        'task_flow_id': task_flow_id,
        'name': name,
        'payload': payload,
        'depend_list': depend_list,
        'status': 'DEFINED',
        'component': component,
        'action': action
    }
    resp = db_api.save_task(args)
    return resp.get('task_id')

def get_task(self, task_id):
    return db_api.get_task(task_id)

def save_task_output(self, task_id, status, output):
    args = {
        'status': status,
        'output': output,
        'complete_time': datetime.datetime.now()
    }
    resp = db_api.update_task(task_id, args)
    return resp