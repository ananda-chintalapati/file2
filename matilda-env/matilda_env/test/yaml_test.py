#from ruamel import yaml
import yaml
import json

st = 'aws_ws.yaml'
data = None
with open(st, 'r') as stream:
  try:
    print stream
    data = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

print data
print '------------------'
print yaml.safe_dump(data, allow_unicode=True,default_flow_style=False)
print '------------------'

user_data = ['|','#!/bin/bash','echo "{{ key_item }}" >> /root/.ssh/authorized_keys']

data2=[{'tasks': [{'register': 'my_ip', 'name': 'Get my current IP address', 'uri': {'url': 'http://checkip.amazonaws.com/', 'return_content': True}}, {'debug': 'var=k_item', 'with_file': ['~/.ssh/id_rsa.pub'], 'name': 'capture public key'}, {'register': 'image_search', 'name': 'Search Image', 'ec2_ami_find': {'aws_secret_key': 'o6H3UDWSIYF0kLdm0RxiTazgcKgpswzy/pONLpZ1', 'sort': 'name', 'aws_access_key': 'AKIAIAHYTLHZZDTHVEZA', 'name': 'Ubuntu Server 14.04 LTS (HVM)*'}}, {'ec2_group': {'aws_secret_key': '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', 'aws_access_key': 'AKIAIAHYTLHZZDTHVEZA', 'name': 'dbservers', 'description': 'A security group for my current IP'}, 'name': 'Create simple security group'}, {'register': 'ec2_master', 'name': 'Create EC2 instances', 'ec2': {'aws_secret_key': 'o6H3UDWSIYF0kLdm0RxiTazgcKgpswzy/pONLpZ1', 'aws_access_key': 'AKIAIAHYTLHZZDTHVEZA', 'count_tag': {'application': 'db'}, 'key_name': 'qa', 'instance_tags': {'application': 'db'}, 'user_data': '\n'.join(user_data), 'wait': 'yes'}}], 'hosts': 'localhost', 'vars': {'region': 'us-west-2'}}]



#'user_data': '|\n#!/bin/bash\necho \"{{ key_item }}\" >> /root/.ssh/authorized_keys\n', 'wait': 'yes'
print yaml.dump(data2, default_flow_style=False, encoding=None, allow_unicode=True)
