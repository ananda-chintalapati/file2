import uuid

from matilda_env.vo.component.component import BaseComponent
from matilda_env.vo.component.rule import Rule


class SecurityGroups(BaseComponent):

    def __init__(self, id=None, name=None, rules=None):
        self._id = id
        self._name = name
        self._rules = rules

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        self._rules = value
    