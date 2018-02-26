import datetime
from matilda_env.db import api

class Template():

    def __init__(self, id=None, name=None, status=None, scope=None,
                 owner=None, created_by=None, created_at=None):
        self._id = id
        self._name = name
        self._status = status
        self._scope = scope
        self._owner = owner
        self._created_by = created_by
        self._created_at = created_at or datetime.datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def scope(self):
        return self._scope

    @property
    def owner(self):
        return self._owner

    @property
    def created_by(self):
        return self._created_by

    @property
    def created_at(self):
        return self._created_at

    def create(self, component_list=None):
        template = None
        if not self.is_template_exists(id, self.name):
            template = api.create_template(id, self.name, self.created_by, self.status, self.scope, self.created_at)
            if len(component_list) > 0:
                template_components = self.add_components_to_template(id, component_list)
                template['components'] = template_components
            return self.prepare_response('Template Created', 'Success', template)
        else:
            return self.prepare_response('Template already exists', 'Fail', template)

    def prepare_response(self, msg=None, request_status=None, response=None):
        response = {
            'request_status': request_status,
            'message': msg,
            'template': response
        }
        return response

    def is_template_exists(self, id, name):
        template = api.get_templates(id=id)
        if len(template) > 0:
            return True
        else:
            template = api.get_templates(name=name)
            if len(template) > 0:
                return True
        return False

    def add_components_to_template(self, id, component_list):
        for component in component_list:
            resp = {
                'project_id': id,
                'type': component['type'],
                'component_id': component['id']
            }
            api.add_component(resp)
        return True