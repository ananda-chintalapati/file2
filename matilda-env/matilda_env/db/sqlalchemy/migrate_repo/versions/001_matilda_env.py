import datetime
import logging
import uuid

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Enum, Float
from sqlalchemy import dialects
from sqlalchemy import ForeignKey, Index, Integer, MetaData, String, Table, JSON
from sqlalchemy import Text
from sqlalchemy.types import NullType
#from sqlalchemy.dialects.mysql import JSON

log = logging.getLogger(__name__)


def MediumText():
    return Text().with_variant(dialects.mysql.MEDIUMTEXT(), 'mysql')


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    sn_request = Table('sn_request', meta,
                       Column('request_id', String(length=50),
                             primary_key=True, nullable=False ),
                       Column('total_ritm_count', Integer),
                       Column('received_ritm', Integer),
                       Column('status', String(50)),
                       Column('create_dt', DateTime, default=datetime.datetime.now()),
                       Column('complete_dt', DateTime),
                      mysql_engine='InnoDB',
                      mysql_charset='utf8')

    sn_ritm = Table('sn_ritm', meta,
                    Column('ritm_no', String(length=50),
                             primary_key=True, nullable=False),
                    Column('request_id', String(length=50)),
                    Column('status', String(length=50)),
                    Column('received_dt', DateTime, default=datetime.datetime.now()),
                    Column('payload', JSON),
                      mysql_engine='InnoDB',
                      mysql_charset='utf8')

    task = Table('task', meta,
                 Column('task_id', String(length=50),
                        primary_key=True, nullable=False),
                 Column('name', String(length=50)),
                 Column('payload', JSON),
                 Column('input_args', String(length=50)),
                 Column('priority', String(length=50)),
                 Column('depend_task', String(length=250)),
                 Column('depend_params', String(length=50)),
                 Column('depend_list', JSON),
                 Column('status', String(length=50)),
                 Column('launch_time', String(length=50)),
                 Column('complete_time', String(length=50)),
                 Column('attempt', Integer),
                 Column('max_retries', Integer),
                 Column('status_msg', String(length=50)),
                 Column('task_flow_id', String(length=50)),
                 Column('output', JSON),
                 Column('component', String(length=50)),
                 Column('action', String(length=50)),
                 mysql_engine='InnoDB',
                 mysql_charset='utf8')

    task_flow = Table('task_flow', meta,
                      Column('task_flow_id', String(length=50),
                             primary_key=True, nullable=False),
                      Column('status', String(length=50)),
                      Column('task_length', Integer),
                      Column('completed_tasks', Integer),
                      Column('pending_tasks', Integer),
                      Column('taskflow_metadata', JSON),
                      Column('description', String(length=50)),
                      Column('task_list', String(length=250)),
                      Column('create_dt', DateTime),
                      Column('complete_dt', DateTime),
                      Column('last_updated', DateTime),
                      mysql_engine='InnoDB',
                      mysql_charset='utf8')

    task = Table('ritm_task', meta,
                 Column('task_id', String(length=50),
                        primary_key=True, nullable=False),
                 Column('name', String(length=50)),
                 Column('role', String(length=50)),
                 Column('ritm_no', String(length=50)),
                 Column('req_no', String(length=50)),
                 Column('status', String(length=50)),
                 Column('msg', String(length=250)),
                 Column('output', JSON),
                 Column('update_dt', DateTime),
                 mysql_engine='InnoDB',
                 mysql_charset='utf8')


    tables = [sn_request, sn_ritm, task, task_flow]

    for table in tables:
        try:
            table.create()
        except Exception:
            log.info(repr(table))
            log.exception('Exception while creating table')
            raise

    if migrate_engine.name == 'mysql':
        migrate_engine.execute(
            'ALTER TABLE migrate_version CONVERT TO CHARACTER SET utf8')
        migrate_engine.execute(
            'ALTER DATABASE %s DEFAULT CHARACTER SET utf8' %
            migrate_engine.url.database)


def downgrade(migrage_engine):
    raise NotImplementedError('Downgrade is not implemented')
