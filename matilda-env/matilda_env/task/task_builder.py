import uuid

from matilda_env.task import task_db_handler as tdh

class TaskBuilder():

    def __init__(self, payload):
        self.task_flow_id = uuid.uuid4()
        self.payload = payload
        self.task_list = []

    def process_payload(self):
        print 'Executing paylaod %r' % self.payload
        net_task = self.create_network_task()
        self.task_list.append(net_task)
        depend_list = [{'task': net_task, 'key': 'vpc.id'}]
        subnet_task = self.create_subnet_task(depend_list)
        sec_grp_task = self.create_sec_group(depend_list)
        self.task_list.append(subnet_task)
        self.task_list.append(sec_grp_task)
        depend_list.append({'task': sec_grp_task, 'key': 'group_id'})
        instance_task = self.create_instances(depend_list)
        self.task_list.append(instance_task)
        depend_list = []
        depend_list.append({'task': sec_grp_task, 'key': 'group_id'})
        depend_list.append({'task': instance_task, 'key': 'instance_id'})
        if self.payload['server_info']['quantity'] > 1:
            lb_task = self.create_lb(depend_list)
            self.task_list.append(lb_task)
        depend_list = []
        depend_list.append({'task': instance_task, 'key': 'public_ip'})
        need_k8 = self.payload['service_info'].get('con_ws') or self.payload['service_info'].get('con_db') or 'No'
        if need_k8 == 'Yes':
            k8_task = self.install_k8s(depend_list)
            k8s_service_task = self.install_k8s_service(depend_list)
            self.task_list.append(k8_task)
            self.task_list.append(k8s_service_task)
        else:
            service_task = self.install_service(depend_list)
            self.task_list.append(service_task)
        if 'application_info' in self.payload:
            app_task = self.install_application(depend_list)
            self.task_list.append(app_task)
        sn_task = self.send_response_to_sn(depend_list)
        self.task_list.append(sn_task)
        return self.task_list

    def _get_auth(self):
        return {
            'aws_access_key': self.payload['cloud_auth']['aws_accesskey'] or 'AKIAIAHYTLHZZDTHVEZA',
            'aws_secret_key': self.payload['cloud_auth']['aws_secret'] or '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',
            'region': self.payload['cloud_auth']['aws_region'] or 'us-west-2'
        }

    def create_network_task(self):
        data = {
            'auth': self._get_auth(),
            'args': {
                'name': self.payload['network_details']['env_sel_net'],
                'cidr': self.payload['network_details']['env_ip_range'],
                'tenancy': 'default',
                'tags': {
                    'Name': self.payload['network_details']['env_sel_net']
                }
            }
        }

        return tdh.create_task(self.task_flow_id, 'create_network', data, None, 'network', 'create')

    def create_subnet_task(self, depend_list):
        payload_sn = {}
        payload_sn['vpc_id'] = self.payload['network_details']['env_sel_net']
        payload_sn['cidr'] = self.payload['network_details'].get('env_sub_net_range')
        payload_sn['state'] = self.payload['network_details'].get('state') or 'present'
        payload_sn['az'] = self.payload['network_details'].get('env_avai_zone')
        tags = {
            'Name': self.payload['network_details'].get('env_sub_net')
        }
        payload_sn['tags'] = tags
        data = {
            'auth': self._get_auth(),
            'args': payload_sn
        }

        return tdh.create_task(self.task_flow_id, 'create_subnet', data, depend_list, 'subnet', 'create')

    def create_sec_group(self, depend_list):
        sec_grp = {
            'name': self.payload['security_group_info'].get('security_name') or self.payload['request_no'],
            'vpc_id': self.payload['network_details']['env_sel_net'],
            'description': self.payload['request_no'] + '_sec_grp',
            'rules': []
        }
        data = {
            'auth': self._get_auth(),
            'args': sec_grp
        }

        return tdh.create_task(self.task_flow_id, 'create_sec_group', data, depend_list, 'sec_group', 'create')

    def create_instances(self, depend_list):
        compute = {
            'key_name': self.payload['server_info'].get('key_name') or 'qa',
            'flavor': self.payload['flavor_details']['flavor'],
            'security_group': self.payload['security_group_info'].get('security_name'),
            'count': self.payload['server_info'].get('quantity') or 1,
            'image_id': self.payload['image_details']['image'],
            'net_id': self.payload['network_details']['env_sel_net'],
            'state': 'present',
            'init_scripts': self.get_public_key_command(),
            'name': self.payload['server_info'].get('server_name')
        }
        data = {
            'auth': self._get_auth(),
            'args': compute
        }
        return tdh.create_task(self.task_flow_id, 'create_instance', data, depend_list, 'instance', 'create')

    def create_lb(self, depend_list):
        lb = {
            'name': self.payload['request_no'] + '_lb',
            # 'zones': ['us-west-2'],
            'subnets': self.payload['network_details'].get('env_sub_net'),
            'sec_groups': self.payload['security_group_info'].get('security_name'),
            'instance_id': [],
            'listeners': []
        }
        listeners = []
        port = []
        for item in port:
            data = {
                'load_balancer_port': item,
                'instance_port': item
            }
            listeners.append(data)

        lb['listeners'] = listeners
        print 'LB paylaod %r' % lb
        return tdh.create_task(self.task_flow_id, 'create_lb', data, depend_list, 'lb', 'create')

    def install_k8s(self, depend_list, public_ips):
        master_ip = public_ips[0]
        if len(public_ips) > 1:
            slave_list = public_ips[1:]
            slaves = ','.join(slave_list)
        else:
            slaves = public_ips[0]
        data = {
            'request': {
                'name': 'kube cluster',
                'slave_list': slaves,
                'master_ip': master_ip
            }

        }
        return tdh.create_task(self.task_flow_id, 'create_k8s', data, depend_list, 'k8s', 'create')


    def install_k8s_service(self, depend_list):
        service = None
        if 'ser_cat_ws' in self.payload['service_info']:
            service = self.payload['service_info']['ws_typ_n'].lower()
        elif 'ser_cat_ds' in self.payload['service_info']:
            service = self.payload['service_info']['db_ser_typ_n'].lower()
        print 'Service %r' % service
        master_ip = ''
        args = {
            'request': {
                'service_name': service,
                'git_url': 'http://192.168.20.142/chandu/kubernetesrepo/raw/master/',
                'cluster_info': {'master_ip': master_ip},
                'public_ip': master_ip,
                'replication': '1',
                'scale_up': '2',
                'scale_down': '1',
                'service': service,
                'deployment': service,
                'replication_count': '1',
                'ritm_no': '',
                'request_type': ''
            }}
        return tdh.create_task(self.task_flow_id, 'install_k8s_service', args, depend_list, 'k8s_service', 'create')

    def install_service(self, depend_list):
        service = None
        if 'ser_cat_ws' in self.payload['service_info']:
            service = self.payload['service_info']['ws_typ_n'].lower()
        elif 'ser_cat_ds' in self.payload['service_info']:
            service = self.payload['service_info']['db_ser_typ_n'].lower()
        print 'Service %r' % service
        return tdh.create_task(self.task_flow_id, 'install_service', service, depend_list, 'service', 'create')

    def install_application(self, depend_list):

        return tdh.create_task(self.task_flow_id, 'install_application', self.payload.get('application_info'),
                               depend_list, 'application', 'install')

    def send_response_to_sn(self, depend_list):
        return tdh.create_task(self.task_flow_id, 'sn_response', depend_list,
                               depend_list, 'service', 'create')

    def get_public_key_command(self):
        msg = """|
            #!/bin/bash
            echo {{ lookup('file', '~/.ssh/id_rsa.pub') }} >> /root/.ssh/authorized_keys
        """
        return msg
