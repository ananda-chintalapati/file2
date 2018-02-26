import uuid

from matilda_env.vo.component.component import BaseComponent


class Server(BaseComponent):

    def __init__(self, id=None, provider=None, flavor=None, image=None, vcpus=None, memory=None, disk=None, public_ip=None,
                 mac_addr=None, status=None, nics=None, region=None, key=None, sec_groups=None, instance_id=None, launch_time=None,
                 private_ip=None, placement=None):
        self._id = id
        self._provider = provider
        self._flavor = flavor
        self._image = image
        self._vcpus = vcpus
        self._memory = memory
        self._disk = disk
        self._public_ip = public_ip
        self._mac_addr = mac_addr
        self._status = status
        self._nics = nics
        self._region = region
        self._key = key
        self._sec_groups = sec_groups
        self._instance_id = instance_id
        self._launch_time = launch_time
        self._private_ip = private_ip
        self._placement = placement


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value

    @property
    def flavor(self):
        return self._flavor

    @flavor.setter
    def flavor(self, value):
        self._flavor = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def vcpus(self):
        return self._vcpus

    @vcpus.setter
    def vcpus(self, value):
        self._vcpus = value

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @property
    def disk(self):
        return self._disk

    @disk.setter
    def disk(self, value):
        self._disk = value

    @property
    def public_ip(self):
        return self._public_ip

    @public_ip.setter
    def public_ip(self, value):
        self._public_ip = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def mac_addr(self):
        return self._mac_addr

    @mac_addr.setter
    def mac_addr(self, value):
        self._mac_addr = value


    @property
    def nics(self):
        return self._nics

    @nics.setter
    def nics(self, value):
        self._nics = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value


    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def sec_groups(self):
        return self._sec_groups

    @sec_groups.setter
    def sec_groups(self, value):
        self._sec_groups = value

    @property
    def instance_id(self):
        return self._instance_id

    @instance_id.setter
    def instance_id(self, value):
        self._instance_id = value

    @property
    def launch_time(self):
        return self._launch_time

    @launch_time.setter
    def launch_time(self, value):
        self._launch_time = value

    @property
    def private_ip(self):
        return self._private_ip

    @private_ip.setter
    def private_ip(self, value):
        self._private_ip = value

    @property
    def placement(self):
        return self._placement

    @placement.setter
    def placement(self, value):
        self._placement = value

    def to_dict(self):
        return self.__dict__

    def list(self, args):
        pass



