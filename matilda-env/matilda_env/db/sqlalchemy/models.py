import datetime
import uuid

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import (Column, String)
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import DateTime, Integer, Text, JSON

CONF = cfg.CONF
BASE = declarative_base()


def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')


class MatildaEnvBaseVirt(models.ModelBase):
    metadata = None

    def __copy__(self):
        session = orm.Session()

        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy

    def save(self, session=None):
        from matilda_env.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaEnvBaseVirt, self).save(session=session)

    def delete(self, session=None):
        from matilda_env.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaEnvBaseVirt, self).delete(session=session)

    def __repr__(self):
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ','.join(items))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class SNRequest(BASE, MatildaEnvBaseVirt):

    __tablename__ = 'sn_request'

    request_id = Column(String(50), autoincrement=True,
                        primary_key=True)
    total_ritm_count = Column(String(50))
    received_ritm = Column(String(50))
    status = Column(String(20))
    create_dt = Column(DateTime, default=datetime.datetime.now())
    complete_dt = Column(DateTime, default=datetime.datetime.now())


class SNRitm(BASE, MatildaEnvBaseVirt):

    __tablename__ = 'sn_ritm'

    ritm_no = Column(String(50), primary_key=True, default=uuid.uuid4())
    request_id = Column(String(50))
    status = Column(String(50))
    received_dt = Column(DateTime, default=datetime.datetime.now())
    payload = Column(JSON)


class TaskFlow(BASE, MatildaEnvBaseVirt):

    __tablename__ = 'task_flow'

    task_flow_id = Column(String(50), autoincrement=True,
                        primary_key=True)
    status = Column(String(50))
    task_length = Column(Integer)
    completed_tasks = Column(Integer)
    pending_tasks = Column(Integer)
    description = Column(String(50))
    task_list = Column(String(250))
    taskflow_metadata = Column(JSON)
    create_dt = Column(DateTime, default=datetime.datetime.now())
    complete_dt = Column(DateTime, default=datetime.datetime.now())
    last_updated = Column(DateTime, default=datetime.datetime.now())


class Task(BASE, MatildaEnvBaseVirt):

    __tablename__ = 'task'

    task_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    payload = Column(JSON)
    input_args = Column(String(50))
    priority = Column(String(50))
    depend_task = Column(String(250))
    depend_params = Column(String(50))
    depend_list = Column(JSON)
    status = Column(String(50))
    launch_time = Column(DateTime, default=datetime.datetime.now())
    complete_time = Column(DateTime)
    attempt = Column(Integer)
    max_retries = Column(Integer)
    status_msg = Column(String(50))
    task_flow_id = Column(String(50))
    output = Column(JSON)
    component = Column(String(50))
    action = Column(String(50))

class RITMTask(BASE, MatildaEnvBaseVirt):

    __tablename__ = 'ritm_task'

    task_id = Column(String(50), primary_key=True)
    name = Column(String(50))
    role = Column(String(50))
    ritm_no = Column(String(50))
    req_no = Column(String(50))
    status = Column(String(50))
    msg = Column(String(255))
    output = Column(JSON)
    update_dt = Column(DateTime, default=datetime.datetime.now())

