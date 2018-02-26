
class Task():

    def __init__(self, name=None, task_id=None, input_args=None, payload=None, priority=None, depend_task=None,
                 depend_params=None, output=None, status=None, launch_time=None, complete_time=None, attempt=None,
                 max_retries=None, status_msg=None, task_flow_id=None, component=None, action=None, depend_list=[]):
        self._name = name
        self._task_id = task_id
        self._payload = payload
        self._input_args = input_args
        self._priority = priority
        self._depend_task = depend_task
        self._depend_params = depend_params
        self._depend_list = depend_list
        self._status = status
        self._launch_time = launch_time
        self._complete_time = complete_time
        self._attempt = attempt
        self._max_retries = max_retries
        self._status_msg = status_msg
        self._task_flow_id = task_flow_id
        self._output = output
        self._component = component
        self._action = action

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def task_id(self):
        return self.task_id

    @task_id.setter
    def task_id(self, value):
        self._task_id = value

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    @property
    def input_args(self):
        return self._input_args

    @input_args.setter
    def input_args(self, value):
        self._input_args = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value

    @property
    def depend_task(self):
        return self._depend_task

    @depend_task.setter
    def depend_task(self, value):
        self._depend_task = value

    @property
    def depend_params(self):
        return self._depend_params

    @depend_params.setter
    def depend_params(self, value):
        self._depend_params = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def launch_time(self):
        return self._launch_time

    @launch_time.setter
    def launch_time(self, value):
        self._launch_time = value

    @property
    def complete_time(self):
        return self._complete_time

    @complete_time.setter
    def complete_time(self, value):
        self._complete_time = value

    @property
    def attempt(self):
        return self._attempt

    @attempt.setter
    def attempt(self, value):
        self._attempt = value

    @property
    def max_retries(self):
        return self._max_retries

    @max_retries.setter
    def max_retries(self, value):
        self._max_retries = value

    @property
    def status_msg(self):
        return self._status_msg

    @status_msg.setter
    def status_msg(self, value):
        self._status_msg = value

    @property
    def task_flow_id(self):
        return self._task_flow_id

    @task_flow_id.setter
    def task_flow_id(self, value):
        self._task_flow_id = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, value):
        self._component = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def depend_list(self):
        return self._depend_list

    @depend_list.setter
    def depend_list(self, value):
        self._depend_list.extend(value)
