from matilda_env.vo.component.component import BaseComponent


class Subnet(BaseComponent):

    def __init__(self):
        pass

    @property
    def availability_zone(self):
        return self._az

    @availability_zone.setter
    def availability_zone(self, value):
        self._az = value

    @property
    def cidr(self):
        return self._cidr

    @cidr.setter
    def cidr(self, value):
        self._cidr = value

    @property
    def map_public(self):
        return self._map_public

    @map_public.setter
    def map_public(self, value):
        self._map_public = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def network_id(self):
        return self._network_id

    @network_id.setter
    def network_id(self, value):
        self._network_id = value