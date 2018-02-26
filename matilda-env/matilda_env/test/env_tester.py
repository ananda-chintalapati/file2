from matilda_env.services.env_executor.v1 import env_executor

payload_db = {"request": {"env_project": "TEST","typ_env_deploy": "Create Environment-New","env_name_n": "TestFebAWS1","typ_env": "Testing","cloud_pl_n": "AWS_New York","cp_region":"us-west-2","cp_account":"MATILDA_SNOW_1","cloud_auth": {"aws_accesskey": "","aws_secret": "","aws_region": "","os_username": "","os_password": "","os_auth_url": "","os_tenant_name": "","os_region": "","vm_vcenter_host": "","vm_vcenter_version": "","vm_username": "","vm_esxi_host": "","vm_password": "","vm_datacenter": "","az_client_id": "","az_tenant_name": "","az_secret": "","az_subscription_id": "","az_resource_group": ""},"service_info": {"ser_cat_ds": "Database Server","db_ser_typ_n": "Oracle","ser_req_db": "Oracle 1.0","con_db": "Yes"," cont_pl_ds":"Kubernetes","db_ser_dp_pl_n": "Virtual Servers","mode_db": "Standalone","app_sy_id_db": "ORACLCDB","ha_db": "Yes","app_pwd_db": "**********","my_user":"root","my_password":"**********","my_port":"3306"},"server_info": {"server_name": "NYW_AWS_QDB_CLU_ORACLE1","quantity":"1"},"image_details": {"image": "ami-79873901"},"flavor_details": {"flavor": "t2.medium","vcpus": "4","ram": "ESB","disk": "8"},"network_details": {"network": "","public_net": "","private_net_name": "","env_net_conf": "Create New Network","env_net_name": "vpc-feb12dbnetwork","env_sel_net": "","env_ip_range": "172.18.0.0/16","env_sub_net": "subnet-feb12dbname","env_sub_net_range": "172.18.0.0/20","env_avai_zone": "us-west-1c"},"volume_details": {"storage_provider": "","storage_server_ip_address": "","name": "","storage_array": "","size": ""},"firewall_info": {"Array_string": "[{&quot;protocol&quot;:&quot;TCP&quot;"},"server_acccess_info": {"users": "QA User","service_account": "admin"},"additional_features": {"auto_scaling": "","auto_healing": "Yes","load_balancing": "Round Robin"},"monitoring_info": {"req_monitoring": ""},"autoscaling_indo": {"as_metric_typ": "","as_units": "","cpu_up_threshold": "70","cpu_down_threshold": "20","down_count": "1","up_count": "2","memory_up_threshold": "70","memory_down_threshold": "","req_count_low_threshold": "100","req_count_high_threshold": ""},"request_no": "REQ0010185","ritm_count": "","ritm_no": "RITM0010475","u_request_type":"Database Server Environment & Application Info"}}


payload_ws = {"request": {"env_project": "TEST","typ_env_deploy": "Create Environment-New","env_name_n": "matilda","typ_env": "","cloud_pl_n": "AWS_New York","cp_region":"us-west-2","cp_account":"MATILDA_SNOW_1","cloud_auth": {"aws_accesskey": "","aws_secret": "","aws_region": "","os_username": "","os_password": "","os_auth_url": "","os_tenant_name": "","os_region": "","vm_vcenter_host": "","vm_vcenter_version": "","vm_username": "","vm_esxi_host": "","vm_password": "","vm_datacenter": "","az_client_id": "","az_tenant_name": "","az_secret": "","az_subscription_id": "","az_resource_group": ""},"service_info": {"ser_cat_ws": "Web Server","ws_typ_n": "","con_ws": "No"," cont_pl_ws": "","ws_dp_pl_n": "Virtual Servers","ser_req_ws": "Weblogic 12.2.1.0","java_version_ws": "java 1.8.0_131","mode": "","no_of_as": "1","no_of_nm": "1","no_of_aps": "","high_availability": "Yes","application_nodes": "1","managed_nodes": "1","appl_servers_host": "1"},"server_info": {"server_name": "web1","quantity": "1"},"image_details": {"image": "ami-223f945a"},"flavor_details": {"flavor": "m3.large","vcpus": "2","ram": "7.5","disk": "1 x 32 SSD"},"network_details": {"network": "","public_net": "","private_net_name": "","env_net_conf": "Use Existing Network","env_net_name": "","env_sel_net": "vpc-f7c3d993","env_ip_range": "172.31.0.0/16","env_sub_net": "subnet-3a03d661","env_sub_net_range": "172.31.0.0/20","env_avai_zone": "us-west-1c"},"volume_details": {"storage_provider": "","storage_server_ip_address": "","name": "","storage_array": "","size": ""},"firewall_info": {"Array_string": ""},"server_acccess_info": {"users": "","service_account": ""},"additional_features": {"auto_scaling": "","auto_healing": "Yes","load_balancing": "Round Robin"},"monitoring_info": {"req_monitoring": ""},"autoscaling_info": {"ws_metric_typ": "","ws_units": "","nm_cpu_up_threshold": "70","nm_cpu_down_threshold": "20","nm_down_count": "1","nm_up_count": "2","nm_memory_up_threshold": "70","nm_memory_down_threshold": "","ws_rq_low_tr": "100","ws_req_count_high_tr": ""},"request_no": "REQ0010179","ritm_count": "","ritm_no": "RITM0010458","u_request_type":""}}

env_executor.execute_environment(payload_ws)
