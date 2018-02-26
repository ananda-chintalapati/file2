from matilda_env.vo.component.component import BaseComponent

class Rule(BaseComponent):

    def __init__(self, protocol=None, from_port=None, to_port=None, cidr=None, group_name=None, type=None):
        self._protocol = protocol
        self._from_port = from_port
        self._to_port = to_port
        self._cidr = cidr
        self._group_name = group_name
        self._type = type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value


    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def from_port(self):
        return self._from_port

    @from_port.setter
    def from_port(self, value):
        self._from_port = value

    @property
    def to_port(self):
        return self._to_port

    @to_port.setter
    def to_port(self, value):
        self._to_port = value

    @property
    def cidr(self):
        return self._cidr

    @cidr.setter
    def cidr(self, value):
        self._cidr = value

    @property
    def group_name(self):
        return self._group_name

    @group_name.setter
    def group_name(self, value):
        self._group_name = value
