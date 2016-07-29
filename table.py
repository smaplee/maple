# coding: utf-8
from sqlalchemy import Table, String, Integer, TEXT, Column, Enum, Boolean, TIMESTAMP, Index, UniqueConstraint, Text
from sqlalchemy import MetaData
from sqlalchemy.engine import create_engine


engine = create_engine("mysql://root@localhost/maple?charset=utf8", encoding='utf8', echo=True)
metadata = MetaData()


relate = Table('related', metadata,
    Column('rid',Integer, primary_key=True, autoincrement=True),
    Column('ip', String(128)),
    Column('project', String(128)),
    Column('template', String(128)),
    Column('user', String(128))
)

project = Table('project', metadata,
    Column('pid',Integer, primary_key=True, autoincrement=True),
    Column('project', String(128)),
    Column('resource', String(128)),
    Column('baseurl', String(128)),
    Column('devbranch', String(128)),
    Column('qabranch', String(128)),
    Column('defbranch', String(128)),
    Column('username', String(128)),
    Column('password', String(128)),
    Column('checkout', String(128)),
    Column('deploy', String(128)),
    Column('pre_build_script', String(128)),
    Column('post_build_script', String(128)),
    Column('build_script', String(128)),
    Column('pre_deploy_script', String(128)),
    Column('post_deploy_script', String(128)),

)

config = Table('config', metadata,
    Column('project', String(128)),
    Column('env', String(128)),
    Column('filename', String(128)),
)

host = Table('host', metadata,
    Column('hid',Integer, primary_key=True, autoincrement=True),
    Column('env', String(128)),
    Column('hostname', String(128)),
    Column('house', String(128)),
    Column('device', String(128)),
    Column('frame', String(128)),
    Column('ip', String(128)),
    Column('iface',String(128)),
    Column('cpu',String(128)),
    Column('cores',String(128)),
    Column('os',String(128)),
    Column('kernel',String(128)),
    Column('disk',String(128)),
    Column('memory',String(128)),
    Column('ipmi',String(128)),
    Column('project',String(128)),
    Column('group',String(128)),
    Column('template',String(128)),
    Column('status',String(128)),
    Column('remark',String(128)),
    Column('status',String(128)),
    Column('createdIndex',String(128)),
)

item = Table('item', metadata,
    Column('itemid',Integer, primary_key=True, autoincrement=True),
    Column('template',String(128)),
    Column('item',String(128)),
    Column('script',String(128)),
    Column('condition',String(128)),
    Column('action',String(128)),
    Column('period',String(128)),
    Column('itemkey',String(128))

)

house = Table('house', metadata,
    Column('hid',Integer, primary_key=True, autoincrement=True),
    Column('house',String(128)),
    Column('address',String(128)),
    Column('people',String(128)),
    Column('mail',String(128)),
    Column('phone',String(128)),

)

user = Table('user', metadata,
    Column('uid',Integer, primary_key=True, autoincrement=True),
    Column('username',String(128), unique=True),
    Column('password',String(128)),
    Column('token',String(128)),
    Column('email',String(128)),
    Column('phone',String(128)),
    Column('qq',String(128)),

)

task = Table('task', metadata,
    Column('tid',Integer, primary_key=True, autoincrement=True),
    Column('taskname',String(128)),
    Column('project',String(128)),
    Column('version',String(128)),
    Column('branch',String(128)),
    Column('starttime',String(128)),
    Column('publisher',String(128)),
    Column('engineer',String(128)),
    Column('hosts',String(256)),
)

version = Table('version', metadata,
    Column('vid',Integer, primary_key=True, autoincrement=True),
    Column('project',String(128)),
    Column('project',String(128)),
    Column('version',String(128)),
    Column('branch',String(128)),
    Column('starttime',String(128)),
    Column('publisher',String(128)),
    Column('engineer',String(128)),
    Column('hosts',String(256)),
)
metadata.drop_all(engine)
metadata.create_all(engine)



















