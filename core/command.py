from tornado.web import MissingArgumentError
from tornado.web import HTTPError
from tornado.gen import coroutine
from tornado.options import options
from core.base import BaseHandler
from daemon.client import Client
from daemon.agent import Command
import time
import json


class CMD(BaseHandler):

    @coroutine
    def put(self, *args, **kwargs):
        try:
            content = self.get_argument('command')
            hosts = self.get_arguments('hosts')
        except MissingArgumentError, e:
            self.write({'retcode': 9, 'result': e.log_message})
            self.finish()

        else:
            command = Command()
            commandid = hash(time.time())
            command.commandid = commandid
            command.command = content
            command.commandsource = ''
            command.commandtype = 'cmdline'
            value = command.serialize()
            client = Client(host=options.ehosts)
            try:
                yield client.baseurl()
            except HTTPError, e:
                self.write({'retcode': e.status_code, 'result': e.log_message})
                self.finish()
            else:
                try:
                    yield [ client.set('/host/{host}/command/{commandid}'.format(host=host, commandid=commandid), value) for host in hosts ]
                except HTTPError, e:
                    self.write({'retcode': e.status_code, 'result': e.log_message})
                    self.finish()
                else:
                    self.write({'retcode': 0, 'result': 'success'})

    @coroutine
    def post(self, *args, **kwargs):
        try:
            hosts = self.get_argument('hosts')
            commandid = self.get_argument('commandid')
        except MissingArgumentError, e:
            self.write({'retcode': 9, 'result': e.log_message})
        else:
            results = []
            false = 1
            client = Client(host=options.ehosts)
            try:
                yield [client.get('/host/{host}/result/{commandid}'.format(host=host, commandid=commandid)) for host in hosts]
            except HTTPError, e:
                self.write({'retcode': e.status_code, 'result': e.log_message})
                self.finish()
            else:
                self.write({'retcode': 0, 'result': 'success'})

