from tornado.gen import coroutine
from tornado.httpclient import HTTPError
from tornado.ioloop import PeriodicCallback
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import IOLoop
from lib.resolver import resolve
from functools import partial
from lib.cmd import stdout
from client import Client
from lib.sys import SYS
import requests
import json
import time
import os


class Command(object):

    def __init__(self):

        '''
        cid: command id
        cmd: command content
        cmdres: command exec result
        cmdret: command exec retcode
        cmdtype: command type, eg: cmdline, script
        cmdinterval:  command period exec
        cmdstore: command exec result store address, eg: mysql://host:port/database, http://host:port/
        cmdstore way: command exec result store way, eg: mysql, elasticsearch, redis
        :return:
        '''
        self._cid = None
        self._cmd = None
        self._cmdres = None
        self._cmdret = None
        self._cmdsrc = None
        self._cmdtype = None
        self._cmdinterval = None
        self._cmdstore = None
        self._action = None


    def parser(self, data):
        try:
            result = json.loads(data)
            self._cid = result['commandid']
            self._cmd = result['command']
            self._cmdres = result['result']
            self._cmdret = result['retcode']
            self._cmdsrc = result['commandsource']
            self._cmdtype = result['commandtype']
            self._cmdinterval = result['commandinterval']
            self._cmdstore = result['commandstore']
            self._cmdstoreway = result['commandstoreway']

        except TypeError, e:
            return None

    def serialize(self):
        command = {
                   'commandid': self._cid,
                   'command': self._cmd,
                   'result': self._cmdres,
                   'retcode': self._cmdret,
                   'commandsource': self._cmdsrc,
                   'commandtype': self._cmdtype,
                   'commandinterval': self._cmdinterval,
                   'commandstore': self._cmdstore,
                   'commandstoreway': self._cmdstoreway,

                   }
        return json.dumps(command)

    @property
    def commandid(self):
        return self._cid

    @commandid.setter
    def commandid(self, commandid):
        self._cid = commandid

    @property
    def command(self):
        return self._cmd

    @command.setter
    def command(self, command):
        self._cmd = command

    @property
    def result(self):
        return self._cmdres

    @result.setter
    def result(self, result):
        self._cmdres = result

    @property
    def retcode(self):
        return self._cmdret

    @retcode.setter
    def retcode(self, retcode):
        self._cmdret = retcode

    @property
    def commandtype(self):
        return self._cmdtype

    @commandtype.setter
    def commandtype(self, type):
        self._cmdtype = type

    @property
    def commandsource(self):
        return self._cmdsrc

    @commandsource.setter
    def commandsource(self, source):
        self._cmdsrc = source

    @property
    def commandinterval(self):
        return self._cmdinterval

    @commandinterval.setter
    def commandinterval(self, interval):
        self._cmdinterval = interval

    @property
    def commandstore(self):
        return self._cmdstore

    @commandstore.setter
    def commandstore(self, cmdstore):
        self._cmdstore = cmdstore

    @property
    def commandstoreway(self):
        return self._cmdstoreway

    @commandstoreway.setter
    def commandstoreway(self, way):
        self._cmdstoreway = way


class Agent(object):

    def __init__(self, hosts):
        self.period = None
        self.ioloop = IOLoop.current()
        self.client = Client(host=hosts)
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.success = None
        self.sys = SYS()

    @property
    def baseuri(self):
        return '/host/{ip}'.format(ip=resolve(self.sys.iface))

    @coroutine
    def run(self):
        print 'check leader status'
        while True:
            try:
                response = yield self.client.baseurl()
            except HTTPError, e:
                print 'check node status',e
                continue
            else:
                if not json.loads(response.body)['health'] == 'true':
                    continue
                else:
                    break
        print 'start register basic information'
        yield self.register()
        print 'start load period command'
        yield self.load_period_command()
        print 'start listen command node'
        yield self.listen()

    @coroutine
    def register(self):

        value = self.sys.serialize()
        key = self.baseuri + '/basic'
        try:
            print key, value
            response = yield self.client.set(key, value)
            print 'register response: ', response

        except HTTPError, e:
            print 'register http error: ', e
            if e.code == 403:
                    pass

    @coroutine
    def load_period_command(self):
        key = self.baseuri + '/command'
        response = yield self.client.get(key, recursive=True)
        print '<<<<<<<<<period command result>>>>>>>>>>:  ', response.body
        nodes = json.loads(response.body)['node']['nodes']
        for node in nodes:
            cmd = Command()
            cmd.parser(node)
            if cmd.commandinterval:
                callback = partial(self.exec_command, cmd)
                period = PeriodicCallback(callback=callback, callback_time=cmd.commandinterval)
                period.start()
                self.period = period

    @coroutine
    def listen(self):

        while True:
            try:
                key = self.baseuri + '/command'
                response = yield self.client.watch(key, dir=True)
            except HTTPError, e:
                print '<<<<<watch response exception>>>>>>>>>>',e
                if e.code == 404 or e.code == 403:
                    continue
            else:
                print '<<<<<<<<<<watch command body>>>>>>>>>>>>', response.body
                command = json.loads(response.body)['node']['value']
                cmd = Command()
                cmd.parser(command)
                print '<<<<<<<<<command>>>>>>>>>>>', cmd.serialize()
                if cmd.commandinterval:
                        self.period.stop()
                        callback = partial(self.exec_command, cmd)
                        period = PeriodicCallback(callback=callback, callback_time=float(cmd.commandinterval))
                        period.start()
                        self.period = period
                else:
                    self.ioloop.add_future(self.exec_command(cmd), lambda f: f.result())

    @run_on_executor
    def monitor(self, command):
        pass
    
    @run_on_executor
    def exec_command(self, command):
        if command:
            if command.commandtype == 'cmdline':
                retcode, result = self.cmdline(command)
                command.retcode = retcode
                command.result = result
                print 'command exec result: ', command
                self.write(command)

            elif command.commandtype == 'script':
                retcode, result = self.script(command)
                command.retcode = retcode
                command.result = result
                self.write(command)

            else:
                command.retcode = 9
                command.result = 'method not support'
                self.write(command)

    def write(self, command):
        key = self.baseuri + '/result/' + str(command.commandid)
        self.ioloop.add_future(self.client.set(key, command.serialize()), lambda f: f.result())

    def cmdline(self, command):
        for cmd in command.command:
            retcode, result = stdout(cmd)
            print '<<<<<<<<cmdline exec result>>>>>>>>: ', retcode, result
            return retcode, result

    def script(self, command):
        for url in command.command:
            data = requests.get(url)
            if data.status_code == 200:
                filename = os.path.join('/tmp', str(hash(time.time())))
                with open(filename, 'w') as f:
                    f.write(data.content)
                cmd = 'bash %s' % filename
                retcode, result = stdout(cmd)
                return retcode, result

            elif data.status_code == 301 or data.status_code == 302:
                redirect_url = data.headers['location']
                redirect_data = requests.get(redirect_url)
                if redirect_data.status_data == 200:
                    filename = os.path.join('/tmp', str(hash(time.time())))
                    with open(filename, 'w') as f:
                        f.write(redirect_data.content)
                    cmd = 'bash %s' % filename
                    retcode, result = stdout(cmd)
                    return retcode, result

            elif data.status_code == 404:
                retcode = 404
                result = 'command not found'
                return retcode, result

            else:
                retcode = 500
                result = 'server error'
                return retcode, result

    def start(self):
        self.run()
        IOLoop.current().start()


if __name__ == '__main__':
    agent = Agent(hosts='localhost:2379')
    agent.start()

