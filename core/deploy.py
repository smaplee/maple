# *coding: utf-8

from tornado.options import options
from core.base import BaseHandler
from tornado.ioloop import IOLoop
from functools import partial
from lib.cmd import retcode
from lib.sendmsg import sendmail
from tornado.log import app_log
from copy import deepcopy
import os


class DeployTask(BaseHandler):

    def put(self, *args, **kwargs):
        jobname = self.get_argument('jobname')
        jobtime = self.get_argument('jobtime')
        job = self.get_argument('job')
        jobbranch = self.get_argument('jobbranch')
        jobversion = self.get_argument('jobversion')
        jobmanager = self.get_argument('jobmanager')
        engineer = self.get_argument('engineer')
        hosts = self.get_argument('hosts')
        tid = self.application.settings.get('database').insert('insert into task '
                             '(jobname, jobtime, job, jobbranch, jobversion, jobmanager, engineer, hosts)'
                             'value (%s, %s, %s, %s, %s, %s, %s, %s)',
                             jobname, jobtime, job, jobbranch, jobversion, engineer, jobmanager, hosts
                             )
        callback = partial(self.start, tid)
        IOLoop.current().add_timeout(deadline=jobtime, callback=callback)
        return tid

    def post(self, *args, **kwargs):
        tid = self.get_argument('tid')
        try:
            self.application.settings.get('database').update('update task set jobstatus=-9 where tid=%s', tid)
        except Exception, e:
            app_log.error(e)
            return {'return': 1}
        else:
            return {'return': 0}

    def query(self, *args, **kwargs):
        jobname = self.get_argument('jobname')
        result = self.application.settings.get('database').query('select * from task where jobname=%s', jobname)
        return {'return': 0, 'result': result}

    def sendmsg(self, task):
        if task['jobstatus'] == 0:
            desc = '开始发布'

        if task['jobstatus'] == 10:
            desc = '发布完成'

        if task['jobstatus'] == -1:
            desc = '发布失败'

        message = '''
                Hi, ALL:
                    定于 {time} 的发布任务, {desc}, 发布详情链接：{url}
                    发布任务详情:
                       任务名: {taskname}
                       项目名: {job}
                       项目分支: {branch}
                       项目版本: {version}
                       项目负责人: {manager}
                       开发工程师: {engineer}
            '''.format(
                    time=task['jobtime'],
                    desc=desc,
                    url='',
                    taskname=task['jobname'],
                    job=task['job'],
                    branch=task['jobbranch'],
                    version=task['jobversion'],
                    manager=task['jobmanager'],
                    engineer = task['engineer']
                )
        sendmail(message)

    def start(self, tid, *args):
        database = self.application.settings.get('database')
        task = database.get('select * from task where tid=%s', tid)
        if task['jobstatus'] == 0:
            return
        else:

            # deploy start, send mail
            self.sendmsg(task)
            # get project config
            config = database.get('select * from config where name=%s', task['job'] )
            env = deepcopy(os.environ)
            env.update(config)
            # build java project
            if self.pre_build(task, env) == 0:
                if self.build(task, env) == 0:
                    if self.post_build(task, env) == 0:
                        # deploy java project
                        if self.pre_deploy(task, env) == 0:
                            self.deploy(task, env)

    def build(self, task, env):
        script = env['build_script']
        if os.path.isabs(script):
            return retcode(script, env=env)
        else:
            script = os.path.join(options.ROOT, script)
            return retcode(script, env=env)

    def pre_build(self, task, env):
        script = env['pre_build_script']
        if os.path.isabs(script):
            return retcode(script, env=env)
        else:
            script = os.path.join(options.ROOT, script)
            return retcode(script, env=env)

    def post_build(self, task, env):
        script = env['post_build_script']
        if os.path.isabs(script):
            return retcode(script, env=env)
        else:
            script = os.path.join(options.ROOT, script)
            return retcode(script, env=env)

    def pre_deploy(self, task, env):
        script = env['pre_deploy_script']
        if os.path.isabs(script):
            return retcode(script, env=env)
        else:
            script = os.path.join(options.ROOT, script)
            return retcode(script, env=env)

    def deploy(self, task, env):
        '''
            retcode = bash(hosts, command)
            retcode = script(hosts, script)
            :param task:  include hosts list and jobinfo
            :param env:  include config detail information
            :return:
        '''
        pass

    def bash(self):
        pass
