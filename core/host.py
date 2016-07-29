# *coding: utf-8
from tornado.web import MissingArgumentError
from core.base import BaseHandler
from tornado.log import app_log


class Host(BaseHandler):

    def add(self, *args, **kwargs):
        try:
            env = str(self.get_argument('env', 'qa'))
            hostname = str(self.get_argument('hostname'))
            owner = self.get_argument('owner')
            vncport = self.get_argument('vncport')
            ip = str(self.get_argument('ip'))
            ipmi = str(self.get_argument('ipmi', ' '))
            mac = str(self.get_argument('mac', ' '))
            house = self.get_argument('house', ' ')
            device = str(self.get_argument('device', ' '))
            frame = str(self.get_argument('frame', ' '))
            os = str(self.get_argument('os', ' '))
            cpu = str(self.get_argument('cpu', ' '))
            cores = str(self.get_argument('cores', ' '))
            mem = str(self.get_argument('mem', ' '))
            osrelease = str(self.get_argument('osrelease', ' '))
            disk = str(self.get_argument('disk', ' '))
            sn = str(self.get_argument('sn', ' '))
            status = str(self.get_argument('status', default='offline'))
            remark = str(self.get_argument('remark', ' '))
        except MissingArgumentError, e:
            return {'result': 1, 'msg': 'MissingArgument'}

        else:
            try:
                hid = self.application.settings.get('database').insert('insert into host '
                                                             '(env, hostname, ip, ipmi, mac, house, device, frame, os, cpu, cores, mem, osrelease, disk, sn, status, remark, owner, vncport)'
                                                             'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                                             env, hostname, ip, ipmi, mac, house, device, frame, os, cpu, cores, mem, osrelease, disk, sn, status, remark, owner, vncport
                                                             )
            except Exception, e:
                app_log.error(e)
                return {'result': 1, 'msg': 'please check data or mysql connect'}
            return {'result': hid}

    def post(self, *args, **kwargs):
        pass

    def remove(self, *args, **kwargs):
        hid = self.get_argument('hid')
        self.application.settings.get('database').execute('delete from host where hid=%s', hid)
        return {'result': 0}

    def query(self, *args, **kwargs):
        print 'query'
        result = self.application.settings.get('database').query('select * from host')
        return {'result': result}