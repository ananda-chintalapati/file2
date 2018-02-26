import datetime
import uuid

from matilda_env.vo.task import Task
from matilda_env.payload_builder.sn import aws
from matilda_env.db import api as db_api

class TaskFlowBuilder():

    def __init__(self, task_flow_id=uuid.uuid4()):
        self.task_flow_id = task_flow_id
        self.metadata = {}
        self.task_list = []

    def set_metadata(self, args):
        self.metadata = args

    def add_task_list(self, task):
        self.task_list.append(task)


    def build_taskflow(self, args, payload):
        task_list = []
        for item in args:
            task_id = item.get('task_id')
            if task_id is not None:
                task = self.get_task(task_id)
                if task.status == 'COMPLETE':
                    continue
                task.attempt = int(task.attempt) + 1
                task.status = 'RETRY'
            else:
                task = Task()
                task.task_id = uuid.uuid4()
                task.name = item.get('name')
                task.attempt = 1
                task.task_flow_id = item.get('task_flow_id')
                task.launch_time = datetime.datetime.now()
                task.max_retries = item.get('max_retries')
                task.depend_task = item.get('depend_task')
                task.depend_params = item.get('depend_params')
                task.payload = self.prepare_payload(item.get('component'), item.get('action'), payload)
                task.priority = item.get('priority')
                task.status = 'DEFINED'
                task.status_msg = 'DEFINED'
                task.component = item.get('component')
                task.action = item.get('action')
            task_list.append(task)
        return task_list

    def prepare_task(self, task_data, payload):
        task = Task()
        task.task_id = uuid.uuid4()
        task.name = task_data.get('name')
        task.attempt = 1
        task.task_flow_id = self.task_flow_id
        task.launch_time = datetime.datetime.now()
        task.max_retries = task_data.get('max_retries') or 1
        task.depend_task = task_data.get('depend_task')
        task.depend_params = task_data.get('depend_params')
        task.payload = self.prepare_payload(task_data.get('component'), task_data.get('action'), payload)
        task.priority = task_data.get('priority')
        task.status = 'DEFINED'
        task.status_msg = 'DEFINED'
        task.component = task_data.get('component')
        task.action = task_data.get('action')
        self.save_task(task)
        return task

    def save_taskflow(self):
        args = {
            'task_flow_id': self.task_flow_id,
            'task_list': self.task_list,
            'metadata': self.metadata
        }
        db_api.save_taskflow(args)

    def save_task(self, task):
        args = {
            'task_id': task.task_id,
            'task_flow_id': task.task_flow_id,
            'name': task.name,
            'depend_list': task.depend_list,
            'status': 'DEFINED'
        }
        db_api.save_task(args)


    def prepare_payload(self, component, action, payload):
        return aws.prepare_payload(component, action, payload)

    def get_task(self, task_id):
        return None

    def update_task(self, task_id, args):
        task = self.get_task(task_id)
        for k, v in args.iteritems():
            task.k = args[k]
        return task

