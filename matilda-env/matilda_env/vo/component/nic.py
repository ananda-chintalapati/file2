import uuid
import matilda_client

from matilda_env.vo.component.component import BaseComponent


class Nic(BaseComponent):

    def __init__(self, id, add_public_ip):
        self._id = id
        self._add_public_ip = add_public_ip

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def add_public_ip(self):
        return self._add_public_ip

    @add_public_ip.setter
    def add_public_ip(self, value):
        self._add_public_ip = value

