from matilda_env.vo.component.component import BaseComponent

class Listener(BaseComponent):

    def __init__(self, protocol=None, load_balancer_port=None, instance_port=None, instance_protocol=None,
                   proxy_protocol=None, ssl_certificate_id=None):
        self._protocol = protocol
        self._load_balancer_port = load_balancer_port
        self._instance_port = instance_port
        self._instance_protocol = instance_protocol
        self._proxy_protocol = proxy_protocol
        self._ssl_certificate_id = ssl_certificate_id

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value

    @property
    def load_balancer_port(self):
        return self._load_balancer_port

    @load_balancer_port.setter
    def load_balancer_port(self, value):
        self._load_balancer_port = value

    @property
    def instance_port(self):
        return self._instance_port

    @instance_port.setter
    def instance_port(self, value):
        self._instance_port = value

    @property
    def instance_protocol(self):
        return self._instance_protocol

    @instance_protocol.setter
    def instance_protocol(self, value):
        self._instance_protocol = value

    @property
    def proxy_protocol(self):
        return self._proxy_protocol

    @proxy_protocol.setter
    def proxy_protocol(self, value):
        self._proxy_protocol = value

    @property
    def ssl_certificate_id(self):
        return self._ssl_certificate_id

    @ssl_certificate_id.setter
    def ssl_certificate_id(self, value):
        self._name = value


class LoadBalancer(BaseComponent):

    def __init__(self, zones=None, name=None, id=None, sec_groups=None, sec_group_ids=None, state=None, subnets=None,
                   instance_ids=None, listeners=None, access_logs=None, health_check=None, instance_ips=None, provider=None):
        self._zones = zones
        self._name = name
        self._id = id
        self._sec_groups = sec_groups
        self._sec_group_ids = sec_group_ids
        self._state = state
        self._subntes = subnets
        self._instance_ids = instance_ids
        self._listeners = listeners
        self._access_logs = access_logs
        self._health_check = health_check
        self._instance_ips = instance_ips
        self._provider = provider

    @property
    def zones(self):
        return self._zones

    @zones.setter
    def zones(self, value):
        self._zones = value

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
    def sec_groups(self):
        return self._sec_groups

    @sec_groups.setter
    def sec_groups(self, value):
        self._sec_groups = value

    @property
    def sec_group_ids(self):
        return self._sec_group_ids

    @sec_group_ids.setter
    def sec_group_ids(self, value):
        self._sec_group_ids = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def subnets(self):
        return self._subntes

    @subnets.setter
    def subnets(self, value):
        self._subnets = value

    @property
    def instance_ids(self):
        return self._instance_ids

    @instance_ids.setter
    def instance_ids(self, value):
        self._instance_ids = value

    @property
    def instace_ips(self):
        return self._instance_ips

    @instace_ips.setter
    def instace_ips(self, value):
        self._instace_ips = value

    @property
    def listeners(self):
        return self._listeners

    @listeners.setter
    def listeners(self, value):
        self._listeners = value

    @property
    def access_logs(self):
        return self._access_logs

    @access_logs.setter
    def access_logs(self, value):
        self._access_logs = value

    @property
    def health_check(self):
        return self._health_check

    @health_check.setter
    def health_check(self, value):
        self._health_check = value

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value