# coding=utf-8
import json
import jinja2

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_oslolog import OsloLog

from matilda_env.api.controller import app_handler

app = Flask(__name__)
CORS(app)
LOG = OsloLog(app).logger
app.jinja_loader = jinja2.FileSystemLoader('/opt/aims/templates')

@app.route('/matilda/environment/new', methods=['POST'])
def create_environment():
    #req_data = json.loads(request.data)
    LOG.info('Received request for new environment')
    req_data = request.get_json()
    print 'Request data %r' % req_data
    #task_flow = sn_task_builder.prepare_tasks(req_data['request'])
    app_handler.process_create_env_request(req_data['request'])
    return jsonify({'status': 'submitted'})

@app.route('/matilda/service/new', methods=['POST'])
def install_service():
    #req_data = json.loads(request.data)
    LOG.info('Received request for install service')
    req_data = request.get_json()
    print 'Request data %r' % req_data
    #task_flow = sn_task_builder.prepare_tasks(req_data['request'])
    app_handler.process_install_service_request(req_data['request'])
    return jsonify({'status': 'submitted'})

@app.route('/matilda/application/new', methods=['POST'])
def deploy_app():
    #req_data = json.loads(request.data)
    LOG.info('Received request for new application')
    req_data = request.get_json()
    print 'Request data %r' % req_data
    #task_flow = sn_task_builder.prepare_tasks(req_data['request'])
    app_handler.process_deploy_app_request(req_data['request'])
    return jsonify({'status': 'submitted'})


@app.route('/matilda/v2/environment/new', methods=['POST'])
def create_environment_v2():
    #req_data = json.loads(request.data)
    req_data = request.get_json()
    print 'req data %r' % req_data
    #task_flow = sn_task_builder.prepare_tasks(req_data['request'])
    app_handler.process_create_env_request(req_data['request'])
    return {'status':'submitted'}

def sn_env_request():
    payload = json.loads(request.data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
