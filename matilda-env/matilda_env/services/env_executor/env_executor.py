from matilda_env.task import task_builder
from matilda_env.task import task_executor

def execute_payload(payload):
    tb = task_builder.TaskBuilder(payload)
    task_list = tb.process_payload()
    task_executor.execute_taskflow(task_list)

    