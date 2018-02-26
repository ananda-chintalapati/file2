from matilda_env.helper import endpoint, rest

class TaskExecutor():

    component = {
        'infra': 'matilda_virt',
        'service': 'matida_service'
    }

    def __init__(self):
        pass

    def execute_task(self, task_id):
        task = self.get_task(task_id)
        url = self.get_endpoint(task.component, task.action)
        response = rest.post(url=url, data=task.payload)
        return response



    def get_task(self, task_id):
        return None

    def get_endpoint(self, component, action):
        return endpoint.get_endpoint(component, action)