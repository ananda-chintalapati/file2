from matilda_env.db.sqlalchemy import api as IMPL


def save_request(req_data):
    return IMPL.save_request(req_data)

def save_ritm(req_data):
    return IMPL.save_ritm(req_data)

def get_request(request_id):
    return IMPL.get_request(request_id)

def get_ritm(ritm):
    return IMPL.get_ritm(ritm)

def get_ritm_for_request(req_id):
    return IMPL.get_ritm_for_request(req_id)


def update_request(request_id, req_data):
    return IMPL.update_request(request_id, req_data)

def save_taskflow(data):
    return IMPL.save_taskflow(data=data)

def get_taskflow(task_flow_id):
    return IMPL.get_taskflow(task_flow_id)

def update_task_flow(task_flow_id, req_data):
    return IMPL.update_task_flow(task_flow_id=task_flow_id,req_data=req_data)


def save_task(data):
    return IMPL.save_task(data)

def get_task(task_id):
    return IMPL.get_task(task_id)

def update_task(task_id, req_data):
    return IMPL.update_task(task_id, req_data)

def save_ritm_task(data):
    return IMPL.save_ritm_task(data)

def get_ritm_task(task_id):
    return IMPL.get_ritm_task(task_id)

def get_ritm_tasks(ritm_no):
    return IMPL.get_ritm_tasks(ritm_no)

def get_ritm_tasks_by_req_role(req_no, role=None):
    return IMPL.get_ritm_tasks_by_req_role(req_no, role=None)

