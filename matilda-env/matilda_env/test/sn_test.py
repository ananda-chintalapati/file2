from matilda_env.services.env_executor.v1 import env_executor as ee

def send_payload_to_sn():
    payload = {
        'u_status': 'Success',
        'u_ritm_no': '',
        'u_request_type': '',
        'u_name': 'Tomcat',
        'u_ip_address': '10.118.128.95',
        'u_storage_name': '',
        'u_storage_ip':''
       }

    ee.send_response_to_sn(payload, ip)

send_payload_to_sn()