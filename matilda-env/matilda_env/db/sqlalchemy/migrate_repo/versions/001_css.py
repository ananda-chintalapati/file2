import datetime
import logging

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Enum, Float
from sqlalchemy import dialects
from sqlalchemy import ForeignKey, Index, Integer, MetaData, String, Table, JSON
from sqlalchemy import Text
from sqlalchemy.types import NullType

log = logging.getLogger(__name__)


def MediumText():
    return Text().with_variant(dialects.mysql.MEDIUMTEXT(), 'mysql')


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    infra_req = Table('infra_req', meta,
                      Column('request_id', Integer,
                             autoincrement=True,
                             primary_key=True, nullable=False),
                      Column('cloud_id', String(length=50),
                             nullable=False),
                      Column('provider', String(length=50),
                             nullable=False),
                      Column('cloud_type', String(length=20),
                             nullable=False),
                      Column('req_name', String(length=50)),
                      Column('status', String(length=20),
                             nullable=False),
                      Column('time_stamp', DateTime(timezone=False),
                             default=datetime.datetime.now()),
                      Column('datacenter', String(length=50)),
                      Column('project', String(length=50)),
                      Column('cluster', String(length=50)),
                      mysql_engine='InnoDB',
                      mysql_charset='utf8')

    infra_req_payload = Table('infra_req_payload', meta,
                           Column('cloud_id', String(length=50),
                                  primary_key=True),
                           Column('payload', JSON),
                           mysql_engine='InnoDB',
                           mysql_charset='utf8'
                           )

    infra_req_metadata = Table('infra_req_metadata', meta,
                               Column('id', Integer, primary_key=True,
                                      autoincrement=True),
                               Column('cloud_id', String(length=50),
                                      nullable=False),
                               Column('name', String(length=30)),
                               Column('tenant_name', String(length=20)),
                               Column('user_name', String(length=20)),
                               Column('password', String(length=50)),
                               Column('auth_url', String(length=100)),
                               Column('region', String(length=20)),
                               mysql_engine='InnoDB',
                               mysql_charset='utf8')

    infra_req_cluster = Table('infra_req_cluster', meta,
                              Column('cloud_id', String(length=50),
                                     primarykey=True, nullable=False),
                              Column('cluster_name', String(length=20)),
                              Column('vm_name', String(length=20)),
                              Column('count', Integer),
                              Column('image', String(length=30)),
                              Column('flavor', String(length=20)),
                              mysql_engine='InnoDB',
                              mysql_charset='utf8'
                              )


    infra_req_firewall = Table('infra_req_firewall', meta,
                               Column('id', Integer, primary_key=True,
                                      autoincrement=True),
                               Column('cloud_id', String(length=50),
                                      nullable=False),
                               Column('protocol', String(length=10)),
                               Column('allow_from', String(length=25)),
                               Column('port_from'), Integer,
                               Column('port_to'), Integer,
                              mysql_engine='InnoDB',
                              mysql_charset='utf8')

    infra_req_monitor = Table('infra_req_monitor', meta,
                              Column('id', Integer, primary_key=True,
                                     autoincrement=True),
                              Column('cloud_id', String(length=50),
                                     nullable=False),
                              Column('add_monitor', String(length=6)),
                              Column('install_agent', String(length=6)),
                              Column('install_snmp', String(length=6)),
                              Column('snmp_pub_string', String(length=25)),
                              mysql_engine='InnoDB',
                              mysql_charset='utf8'
                              )

    infra_req_volume = Table('infra_req_volume', meta,
                             Column('id', Integer, primary_key=True,
                                    autoincrement=True),
                             Column('cloud_id', String(length=50),
                                    nullable=False),
                             Column('volume_name', String(length=50)),
                             Column('size'), String(length=10),
                             Column('mnt_dir'), String(length=20),
                             Column('provider'), String(length=20),
                              mysql_engine='InnoDB',
                              mysql_charset='utf8')

    infra_vm_data = Table('infra_vm_data', meta,
                          Column('vm_id', Integer,
                                 primary_key=True, autoincrement=True),
                          Column('cloud_id', String(length=50)),
                          Column('instance_type', String(length=20)),
                          Column('name', String(length=50)),
                          Column('private_ip', String(length=20)),
                          Column('public_ip', String(length=20)),
                          Column('role', String(length=20)),
                          Column('host_name', String(length=50)),
                          Column('fqdn', String(length=50)),
                          Column('status', String(length=20)),
                          Column('image_id', String(length=50)),
                          Column('distribution', String(length=20)),
                          Column('version', String(length=20)),
                          Column('provider', String(length=20)),
                          Column('datacenter', String(length=50)),
                          Column('project', String(length=50)),
                          Column('cluster', String(length=50)),
                          mysql_engine='InnoDB',
                          mysql_charset='utf8')

    infra_cluster_data = Table('infra_cluster_data', meta,
                               Column('cluster_id', Integer,
                                      primary_key=True, autoincrement=True),
                               Column('cloud_id', String(length=50)),
                               Column('name', String(length=50)),
                               Column('datacenter'), String(length=50),
                               Column('project'), String(length=50),
                               Column('role'), String(length=50),
                               Column('master_ip'), String(length=50),
                               Column('master_status'), String(length=20),
                               Column('master_services'), String(length=20),
                               mysql_engine='InnoDB',
                               mysql_charset='utf8')


    infra_image = Table('infra_image', meta,
                        Column('image_id', Integer,
                               primary_key=True, autoincrement=True),
                        Column('name', String(length=20)),
                        Column('os', String(length=20)),
                        Column('distribution', String(length=20)),
                        Column('version', String(length=20)),
                        Column('public', String(length=3)),
                        Column('provider', String(length=10)),
                        Column('project', String(length=20)),
                        Column('architecture', String(length=10)),
                        Column('min_ram', Integer),
                        Column('min_vcpus', Integer),
                        Column('min_disk', Integer)
                        )

    infra_history = Table('infra_history', meta,
                          Column('id', Integer, primary_key=True,
                                 autoincrement=True),
                          Column('cloud_id', String(length=50),
                                 nullable=False),
                          Column('action', String(length=255)),
                          Column('status', String(length=50)),
                          Column('msg', String(length=255)),
                          Column('notifier', String(length=255)),
                          Column('notified', String(length=5)),
                          Column('time_stamp', DateTime(timezone=False),
                                 default=datetime.datetime.now()),
                          Column('vm_public_ip', String(length=20)),
                          Column('datacenter', String(length=50)),
                          Column('project', String(length=50)),
                          mysql_engine='InnoDB',
                          mysql_charset='utf8')

    infra_details = Table('infra_details', meta,
                          Column('id', Integer, primary_key=True,
                                 autoincrement=True),
                          Column('cloud_id', String(length=50),
                                 nullable=False),
                          Column('service', String(length=50)),
                          Column('state', String(length=20)),
                          mysql_engine='InnoDB',
                          mysql_charset='utf8')

    infra_req_netdata = Table('infra_req_netdata', meta,
                              Column('cloud_id', String(50), primary_key=True),
                              Column('private_net', String(50)),
                              Column('public_net', String(50)),
                              Column('private_cidr', String(30)),
                              Column('gateway', String(20)),
                              Column('private_net_start', String(20)),
                              Column('private_net_end', String(20)),
                              Column('dns', String(20)),
                              )

    infra_flavor = Table('infra_flavor', meta,
                         Column('id', Integer, primary_key=True, autoincrement=True),
                         Column('name', String(20)),
                         Column('ram', Integer),
                         Column('vcpus', Integer),
                         Column('disk', Integer),
                         )

    infra_task_flow = Table('infra_task_flow', meta,
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('cloud_id', String(50)),
                            Column('task', String(50)),
                            Column('status', String(20)),
                            Column('priority', Integer),
                            Column('retries', Integer))

    serv_list = Table('serv_list', meta,
                      Column('id', Integer, primary_key=True,
                             autoincrement=True),
                      Column('serv_id', String(length=50),
                             nullable=False),
                      Column('name', String(length=50)),
                      Column('version', String(length=20)),
                      Column('supporting_os', String(length=200)),
                      mysql_engine='InnoDB',
                      mysql_charset='utf8')

    serv_status = Table('serv_status', meta,
                        Column('id', Integer, primary_key=True,
                               autoincrement=True),
                        Column('cloud_id', String(length=50)),
                        Column('vm_id', String(length=20)),
                        Column('serv_id', String(length=50),
                               nullable=False),
                        Column('status', String(length=20)),
                        mysql_engine='InnoDB',
                        mysql_charset='utf8')

    serv_endpoints = Table('serv_endpoints', meta,
                           Column('id', Integer, primary_key=True,
                                  autoincrement=True),
                           Column('cloud_id', String(length=50),
                                  nullable=False),
                           Column('serv_id', String(length=50),
                                  nullable=False),
                           Column('helper', String(length=20)),
                           Column('user_name', String(length=100)),
                           Column('password', String(length=50)),
                           Column('api_token', String(length=50)),
                           mysql_engine='InnoDB',
                           mysql_charset='utf8')

    serv_history = Table('serv_history', meta,
                         Column('id', Integer, primary_key=True,
                                autoincrement=True),
                         Column('cloud_id', String(length=50),
                                nullable=False),
                         Column('serv_id', String(length=50),
                                nullable=False),
                         Column('action', String(length=20)),
                         Column('msg', String(length=255)),
                         Column('time_stamp', DateTime(timezone=False)),
                         mysql_engine='InnoDB',
                         mysql_charset='utf8')

    exec_req = Table('exec_req', meta,
                     Column('id', Integer, primary_key=True,
                            autoincrement=True),
                     Column('exec_req_id', String(length=50)),
                     Column('cloud_id', String(length=50)),
                     Column('time_stamp', DateTime(timezone=False)),
                     mysql_engine='InnoDB',
                     mysql_charset='utf8')

    exec_req_metadata = Table('exec_req_metadata', meta,
                              Column('id', Integer, primary_key=True,
                                     autoincrement=True),
                              Column('exec_req_id', String(length=50)),
                              Column('cloud_id', String(length=50)),
                              Column('serv_id', String(length=100)),
                              Column('status', String(length=50)),
                              mysql_engine='InnoDB',
                              mysql_charset='utf8')

    exec_req_history = Table('exec_req_history', meta,
                             Column('id', Integer, primary_key=True,
                                    autoincrement=True),
                             Column('exec_req_id', String(length=50)),
                             Column('cloud_id', String(length=50)),
                             Column('serv_id', String(length=100)),
                             Column('action', String(length=255)),
                             Column('time_stamp', DateTime(timezone=False)),
                             mysql_engine='InnoDB',
                             mysql_charset='utf8')

    master_node = Table('master_node', meta,
                        Column('proj_id', String(length=50)),
                        Column('master_ip', String(length=15)),
                        mysql_engine='InnoDB',
                        mysql_charset='utf8')

    node_ip_role = Table('node_role', meta,
                         Column('id', Integer, primary_key=True,
                                    autoincrement=True),
                         Column('ip', String(length=15)),
                         Column('role', String(length=255)),
                         mysql_engine='InnoDB',
                         mysql_charset='utf8'
                         )

    alerts = Table('alerts', meta,
                   Column('id', Integer, primary_key=True,
                          autoincrement=True),
                   Column('host', String(50)),
                   Column('ip', String(15)),
                   Column('msg', String(255)),
                   Column('created_dt', DateTime,
                          default=datetime.datetime.now()),
                   Column('source', String(30)),
                   Column('status', String(30)),
                   Column('severity', String(30)),
                   Column('closed_dt', DateTime),
                   mysql_engine='InnoDB',
                   mysql_charset='utf8')

    tables = [infra_req, infra_req_metadata, infra_history, infra_details, infra_cluster_data,
              infra_vm_data, infra_req_netdata, infra_flavor,infra_image, infra_task_flow,
              infra_req_payload, infra_req_cluster, infra_req_firewall, infra_req_monitor, infra_req_volume,
              serv_list, serv_status, serv_endpoints, serv_history,
              exec_req, exec_req_metadata, exec_req_history, master_node, node_ip_role,
              alerts]

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
