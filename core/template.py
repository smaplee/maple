from core.base import BaseHandler
from daemon.agent import Command
from daemon.client import Client
from tornado.ioloop import IOLoop


class Template(BaseHandler):

    def add(self, *args, **kwargs):
        ip = self.get_argument('ip')
        template_name = self.get_argument('template_name')
        item_name = self.get_argument('item_name')
        item_script = self.get_argument('item_script')
        item_script_content = self.get_argument('item_script_content')
        item_interval = self.get_argument('item_interval')
        item_action = self.get_argument('item_action')
        item_condition = self.get_argument('item_condition')
        database = self.application.settings.get('database')
        database.insert('insert into template (template, name, script, interval, condition, action) '
                        'value (%s, %s, %s, %s, %s, %s)',
                        template_name, item_name, item_script, item_interval, item_condition, item_action
                        )
        database.update('update host set template=%s where ip=%s', template_name, ip)
        return {'retcode': 0, 'result': template_name}

    def update(self, *args, **kwargs):
        ip = self.get_argument('ip')
        template_name = self.get_argument('template_name')
        item_name = self.get_argument('item_name')
        item_script = self.get_argument('item_script')
        item_script_content = self.get_argument('item_script_content')
        item_interval = self.get_argument('item_interval')
        item_action = self.get_argument('item_action')
        item_condition = self.get_argument('item_condition')
        database = self.application.settings.get('database')
        database.update('update template set name=%s, script=%s, interval=%s, condition=%s, action=%s where template=%s and name=%s',
                        template_name, item_script, item_interval,  item_condition, item_action, template_name, item_name
                        )
        database.update('update host set template=%s where ip=%s', template_name, ip)
        return {'retcode': 0, 'result': template_name}

    def query(self, *args, **kwargs):
        template = self.get_argument('template_name')
        database = self.application.setting.get('database')
        result = database.query('select * from template where template = %s', template)
        return {'retcode': 0, 'result': result}