import datetime

from matilda_env.db import api


def create_project(id, name, requestor, status='Initiated',
                   manager=None, create_date=datetime.datetime.now()):
    project_list = get_project(id)
    if len(project_list) > 0:
        msg = 'Project with id {0} already exists'.format(id)
        resp = {
            'request_status': 'Fail',
            'message': msg,
            'project': project_list[0]
        }
        return resp

    project = {
        'id': id,
        'name': name,
        'requestor': requestor,
        'manager': manager,
        'create_date': create_date,
        'status': status,
    }

    api.create_project(project)
    resp = {
        'request_status': 'Success',
        'project': project
    }
    return resp


def get_project(id=None, name=None, health=None):
    project_list = api.get_project(id, name, health)
    return project_list


def update_project_status(id, status):
    api.update_project_status(id, status)
    resp = {
        'id': id,
        'action': 'Update Status',
        'request_status': 'Success'
    }
    return resp

