from matilda_env.vo.component.component import BaseComponent

class Network(BaseComponent):

    def __init__(self, name=None, cidr=None, provider=None, id=None, state=None, tenancy=None):
        self._name = name
        self._cidr = cidr
        self._provider = provider
        self._id = id
        self._state = state
        self._tenancy = tenancy

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def cidr(self):
        return self._cidr

    @cidr.setter
    def cidr(self, value):
        self._cidr = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def tenancy(self):
        return self._state

    @tenancy.setter
    def tenancy(self, value):
        self._tenancy = value