

class BaseComponent():

    def __init__(self):
        pass

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def status(self):
        return self.status

    @status.setter
    def status(self, value):
        self._status = value

    def add_component(self, req):
        raise NotImplemented

    def get_component(self, id, name, status):
        raise NotImplemented

    def update_component(self, id, req):
        raise NotImplemented

    def get_component(self, args):
        raise NotImplemented