import uuid

from matilda_env.db import api as db_api

def save_task(name, role, ritm_no, req_no, status, msg, output):
    args = {
        'task_id': uuid.uuid4(),
        'name': name,
        'role': role,
        'ritm_no': ritm_no,
        'req_no': req_no,
        'status': status,
        'msg': msg,
        'output': output
    }

    return db_api.save_ritm_task(args)

def get_task_by_req_role(req_no, role=None):
    data = db_api.get_ritm_tasks_by_req_role(req_no, role)
    resp = []
    for item in data:
        resp.append(item.to_dict())
    return resp

def get_ritm_task(task_id):
    data = db_api.get_ritm_task(task_id)
    return data.to_dict()
