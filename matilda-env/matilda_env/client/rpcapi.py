from oslo_config import cfg
import oslo_messaging as messaging
from oslo_log import log

from matilda_env.engine import rpc

conf = cfg.CONF

LOG = log.getLogger(__name__)

class RpcAPI(object):

    def __init__(self):
        super(RpcAPI, self).__init__()
        try:
            LOG.info('Initializing Request Queue client')
            rpclient = rpc.RPCManager('matilda-env-req', conf)
            self._client = rpclient.get_client(topic='matilda-env-req')
        except Exception as e:
            LOG.error('Server request queue client initialization failed', e)
            raise e

    def invoke_notifier(self, ctxt, payload, source, version, action):
        try:
            LOG.info('Posting request to engine')
            context = self._client.prepare(version='1.0')
            context.cast(ctxt=ctxt,
                         method='invoke_notifier',
                         payload=payload,
                         source=source,
                         version=version,
                         action=action)
        except messaging.MessageDeliveryFailure as e:
            LOG.error('Message delivery failed', e)
            raise e
