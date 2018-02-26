import random
import threading
import six

from matilda_env.client import rpcengine
from matilda_env.services.env_executor.v1 import env_executor as ev1
from matilda_env.services.env_executor import env_executor as ev2

import logging

LOG = logging.getLogger(__name__)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

@six.add_metaclass(Singleton)
class WorkerFactory(object):
    _db_client = None
    _rpcengine = None
    _client_initialize = False
    _threadpool = {}
    _init_error = None

    def __init__(self):
        LOG.info('Worker factory initialized? %r ' % WorkerFactory._client_initialize)
        if WorkerFactory._client_initialize is False:
            WorkerFactory._client_init()
        WorkerFactory._client_initialize = True

    @staticmethod
    def _client_init():
        WorkerThread._init_error = None
        try:
            WorkerThread._rpcengine = rpcengine.RpcEngine()
        except Exception as e:
            WorkerThread._init_error = 'ERROR'
        finally:
            WorkerThread._threadpool = {}
            if WorkerThread._init_error is None:
                WorkerThread._client_initialize = True

    @classmethod
    def removeworker(cls, id):
        try:
            del WorkerThread._threadpool[id]
        except KeyError as e:
            LOG.error('Thread failed %s' % id, e)
            raise 'Thread failed %r ' % id

    def getworker(self, worker_payload, source, version, action):
        LOG.info('Creating new thread for request processing')
        thread_id = random.randint(0, 99999999)
        worker = WorkerThread(thread_id=thread_id, request_payload=worker_payload, source=source, version=version, action=action)
        WorkerThread._threadpool.update({thread_id: worker})
        return thread_id

    def execute(self, id):
        try:
            worker = WorkerThread._threadpool[id]
        except KeyError:
            raise Exception(message='Thread %r failed' % id)
        worker.start()


class WorkerThread(threading.Thread):

    def __init__(self, thread_id, request_payload, 
                 source, version, action, client_error=None):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.client_error = client_error
        self.payload = request_payload
        self.version = version
        self.source = source
        self.action = action


    def run(self):
        LOG.info('Thread starting - %s' % self.thread_id)
        LOG.info('payload to be executed %r' % self.payload)
        if self._is_engine_initialized():
            try:
                LOG.info('Execute environment creation')
                self._execute(self.payload, self.source, self.version, self.action)
            except Exception as e:
                LOG.error('Request failed to execute', e)
                print 'Error %r' % e
                #raise e
            finally:
                WorkerFactory.removeworker(self.thread_id)
        else:
            raise Exception('Engine is not initialized')

    def _is_engine_initialized(self):
        return True

    def _execute(self, payload, source, version, action='deploy_env'):
        print 'Executing payload %r' % payload
        LOG.info('Execute payload with version %r' % version)
        if version == '1':
            if action == 'deploy_env':
                ev1.execute_payload(payload)
            elif action == 'install_service':
                ev1.install_service(payload['service'], payload['hosts'])
            elif action == 'deploy_app':
                ev1.deploy_application_to_wl(payload['args'], payload['hosts'])
        else:
            ev2.execute_payload(payload)
