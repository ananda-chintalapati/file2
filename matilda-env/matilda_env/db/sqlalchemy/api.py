import sys
import threading


from oslo_config import cfg
from oslo_db import exception as db_exc
from oslo_db import options as oslo_db_options
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as sqlalchemyutils
from oslo_log import log as logging


from matilda_env.db.sqlalchemy import models


api_db_opts = [
    cfg.StrOpt('db_connection',
               help='The SQLAlchemy connection string to use to connect to '
                    'the AIMS Virtualization database.',
               secret=True,
               default='mysql://root:openstack@192.168.10.21/matilda_env'),
    # cfg.BoolOpt('sqlite_synchronous',
    #             default=True,
    #             help='If True, SQLite uses synchronous mode.'),
     cfg.StrOpt('mysql_sql_mode',
                default='TRADITIONAL',
                help='The SQL mode to be used for MySQL sessions. '
                     'This option, including the default, overrides any '
                     'server-set SQL mode. To use whatever SQL mode '
                     'is set by the server configuration, '
                     'set this to no value. Example: mysql_sql_mode='),
    # cfg.IntOpt('idle_timeout',
    #            default=3600,
    #            help='Timeout before idle SQL connections are reaped.'),
    # cfg.IntOpt('max_pool_size',
    #            help='Maximum number of SQL connections to keep open in a '
    #                 'pool.'),
    # cfg.IntOpt('max_retries',
    #            default=10,
    #            help='Maximum number of database connection retries '
    #                 'during startup. Set to -1 to specify an infinite '
    #                 'retry count.'),
    # cfg.IntOpt('retry_interval',
    #            default=10,
    #            help='Interval between retries of opening a SQL connection.'),
    # cfg.IntOpt('max_overflow',
    #            help='If set, use this value for max_overflow with '
    #                 'SQLAlchemy.'),
    # cfg.IntOpt('connection_debug',
    #            default=0,
    #            help='Verbosity of SQL debugging information: 0=None, '
    #                 '100=Everything.'),
    # cfg.BoolOpt('connection_trace',
    #             default=False,
    #             help='Add Python stack traces to SQL as comment strings.'),
]

CONF = cfg.CONF

opt_group = cfg.OptGroup(name='database')
CONF.register_group(opt_group)
CONF.register_opts(oslo_db_options.database_opts, opt_group)
CONF.register_opts(api_db_opts, opt_group)


LOG = logging.getLogger(__name__)

_ENGINE_FACADE = {'matilda_env': None}
_CSS_FACADE = 'matilda_env'
_LOCK = threading.Lock()


def _create_facade(conf_group):

    return db_session.EngineFacade(
        sql_connection=conf_group.db_connection,
        autocommit=True,
        expire_on_commit=False,
        mysql_sql_mode=conf_group.mysql_sql_mode,
        idle_timeout=conf_group.idle_timeout,
        connection_debug=conf_group.connection_debug,
        max_pool_size=conf_group.max_pool_size,
        max_overflow=conf_group.max_overflow,
        pool_timeout=conf_group.pool_timeout,
        sqlite_synchronous=conf_group.sqlite_synchronous,
        connection_trace=conf_group.connection_trace,
        max_retries=conf_group.max_retries,
        retry_interval=conf_group.retry_interval)


def _create_facade_lazily(facade, conf_group):
    global _LOCK, _ENGINE_FACADE
    if _ENGINE_FACADE[facade] is None:
        with _LOCK:
            if _ENGINE_FACADE[facade] is None:
                _ENGINE_FACADE[facade] = _create_facade(conf_group)
    return _ENGINE_FACADE[facade]


def get_engine(use_slave=False):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_engine(use_slave=use_slave)


def get_session(use_slave=False, **kwargs):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_session(use_slave=use_slave, **kwargs)


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def model_query(model,
                args=None,
                session=None):
    if session is None:
        session = get_session()

    query = sqlalchemyutils.model_query(model, session, args)
    return query


def save_request(reqs_data):
    session = get_session()
    with session.begin():
        req_data = models.SNRequest()
        req_data.update(reqs_data)
        req_data.save(session=session)
    return req_data

def save_ritm(ritm_data):
    session = get_session()
    with session.begin():
        req_data = models.SNRitm()
        req_data.update(ritm_data)
        req_data.save(session=session)
        print 'Saved %r' % req_data
    return req_data

def get_request(request_id):
    session = get_session()
    with session.begin():
        query = session.query(models.SNRequest)
        query = query.filter_by(request_id=request_id)
        return query.first()

def get_ritm(ritm):
    session = get_session()
    with session.begin():
        query = session.query(models.SNRitm)
        query = query.filter_by(ritm_no=ritm)
        return query.first()

def get_ritm_for_request(req_id):
    session = get_session()
    with session.begin():
        query = session.query(models.SNRitm)
        query = query.filter_by(request_id=req_id)
        return query.all()


def update_request(request_id, req_data):
    session = get_session()
    with session.begin():
        query = session.query(models.SNRequest)
        query = query.filter_by(request_id=request_id)
        rows = query.update(req_data)
        if not rows:
            raise Exception('Failed DB update')

def save_taskflow(data):
    session = get_session()
    with session.begin():
        req_data = models.TaskFlow()
        req_data.update(data)
        req_data.save(session=session)
    return req_data

def get_taskflow(task_flow_id):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskFlow)
        query = query.filter_by(task_flow_id=task_flow_id)
        return query.first()

def update_task_flow(task_flow_id, req_data):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskFlow)
        query = query.filter_by(task_flow_id=task_flow_id)
        rows = query.update(req_data)
        if not rows:
            raise Exception('Failed DB update')


def save_task(data):
    session = get_session()
    with session.begin():
        req_data = models.Task()
        req_data.update(data)
        req_data.save(session=session)
    return req_data

def get_task(task_id):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskFlow)
        query = query.filter_by(task_id=task_id)
        return query.first()

def update_task(task_id, req_data):
    session = get_session()
    with session.begin():
        query = session.query(models.Task)
        query = query.filter_by(task_id=task_id)
        rows = query.update(req_data)
        if not rows:
            raise Exception('Failed DB update')


def get_taskflow_tasks(task_flow_id):
    session = get_session()
    with session.begin():
        query = session.query(models.TaskFlow)
        query = query.filter_by(task_flow_id=task_flow_id)
        return query.all()

def save_ritm_task(data):
    session = get_session()
    with session.begin():
        req_data = models.RITMTask()
        req_data.update(data)
        req_data.save(session=session)
    return req_data

def get_ritm_task(task_id):
    session = get_session()
    with session.begin():
        query = session.query(models.RITMTask)
        query = query.filter_by(task_id=task_id)
        return query.first()

def get_ritm_tasks(ritm_no):
    session = get_session()
    with session.begin():
        query = session.query(models.RITMTask)
        query = query.filter_by(ritm_no=ritm_no)
        return query.all()

def get_ritm_tasks_by_req_role(req_no, role=None):
    session = get_session()
    with session.begin():
        query = session.query(models.RITMTask)
        query = query.filter_by(req_no=req_no)
        if role is not None:
            query = query.filter_by(role=role)
        return query.all()