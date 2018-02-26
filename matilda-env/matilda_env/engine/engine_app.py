from oslo_config import cfg
from oslo_log import log

from matilda_env.engine.engine import Engine, QueueHandler
from matilda_env.engine import rpc

CONF = cfg.CONF

LOG = log.getLogger(__name__)

def setup_app():
    log.register_options(CONF)
    CONF(default_config_files=['/opt/matilda/matilda-env/etc/matilda_env.conf'])
 #   log.setup(CONF,'aims-virt')
    try:
        rpclient = rpc.RPCManager('matilda-env-req', CONF)
        engine = Engine()
        endpoints = [QueueHandler(engine)]
        server = rpclient.get_server(topic='matilda-env-req',
                                     endpoints=endpoints,
                                     executor='blocking')
        LOG.info('MQ Server Starting.......')
        server.start()
        server.wait()
    except Exception as e:
        LOG.error('Failed to start MQ', e)
        raise e

setup_app()
