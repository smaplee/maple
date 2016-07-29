from tornado.web import MissingArgumentError
from tornado.options import options
from core.base import BaseHandler
from fcntl import F_EXLCK, fcntl
import os


class Service(BaseHandler):

    def add(self, *args, **kwargs):
        try:
            project = self.get_argument('project')
            baseurl = self.get_argument('baseurl')
            devbranch = self.get_argument('devbranch')
            qabranch = self.get_argument('qabranch')
            defbranch = self.get_argument('defbranch')
            username = self.get_argument('username')
            password = self.get_argument('password')
            checkout = self.get_argument('checkout')
            deploy = self.get_argument('deploy')
            # pre build script
            pre_build_script_content = self.get_argument('pre_build_script_content')
            build_script_content = self.get_argument('build_script_content')
            post_build_script_content = self.get_argument('post_build_script_content')
            pre_deploy_script_content = self.get_argument('pre_deploy_script_content')
            post_deploy_script_content = self.get_argument('post_deploy_script_content')
        except MissingArgumentError, e:
            print e.log_message
            return {'retcode': 9, 'result': e.log_message}
        if pre_build_script_content:
            pre_build_script = os.path.join(project, 'pre_build_script')
            self.touch(pre_build_script, pre_build_script_content)

        # build script
        if build_script_content:
            build_script = os.path.join(project, 'build_script')
            self.touch(build_script, build_script_content)

        # post build script
        if post_build_script_content:
            post_build_script = os.path.join(project, 'post_build_script')
            self.touch(post_build_script, post_build_script_content)

        # pre deploy script
        if pre_deploy_script_content:
            pre_deploy_script = os.path.join(project, 'pre_deploy_script')
            self.touch(pre_deploy_script, pre_deploy_script_content)

        # post deploy script persist
        if post_deploy_script_content:
            post_deploy_script = os.path.join(project, 'post_deploy_script')
            self.touch(post_deploy_script, post_deploy_script_content)

        database = self.application.settings.get('database')
        sid = database.insert('insert into project '
                             '(project, baseurl, devbranch, qabranch, defbranch, username, password, checkout, deploy,pre_build_script,build_script,post_build_script,pre_deploy_script,post_deploy_script)'
                             'value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                              project, baseurl, devbranch, qabranch, defbranch, username, password, checkout, deploy,pre_build_script,build_script,post_build_script,pre_deploy_script,post_deploy_script
                             )

        return {'retcode':0,'result': sid}

    def remove(self, *args, **kwargs):
        pid = self.get_argument('pid')
        database = self.application.settings.get('database')
        database.execute('delete from project where sid = %s', pid)
        return {'result': 0}

    def update(self, *args, **kwargs):
        pid = self.get_argument('pid')
        project = self.get_argument('project')
        baseurl = self.get_argument('baseurl')
        devbranch = self.get_argument('devbranch')
        qabranch = self.get_argument('qabranch')
        defbranch = self.get_argument('defbranch')
        username = self.get_argument('username')
        password = self.get_argument('password')
        checkout = self.get_argument('checkout')
        deploy = self.get_argument('deploy')
        pre_build_script = self.get_argument('pre_build_script', default='')
        pre_build_script_content = self.get_argument('pre_build_script_content', default='')
        if pre_build_script and pre_build_script_content:
            self.touch(pre_build_script, pre_build_script_content)
        else:
            self.rm(pre_build_script)

        build_script = self.get_argument('build_script')
        build_script_content = self.get_argument('build_script_content')
        if build_script and build_script_content:
            self.touch(build_script, build_script_content)

        else:
            self.rm(build_script)

        post_build_script = self.get_argument('post_build_script')
        post_build_script_content = self.get_argument('post_build_script_content')
        if post_build_script and post_build_script_content:
            self.touch(post_build_script, post_build_script_content)
        else:
            self.rm(post_build_script)

        pre_deploy_script = self.get_argument('pre_deploy_script')
        pre_deploy_script_content = self.get_argument('pre_deploy_script_content')
        if pre_deploy_script and pre_deploy_script_content:
            self.touch(pre_deploy_script, pre_deploy_script_content)
        else:
            self.rm(pre_deploy_script)

        post_deploy_script = self.get_argument('post_deploy_script')
        post_deploy_script_content = self.get_argument('post_deploy_script_content')
        if post_deploy_script and post_deploy_script_content:
            self.touch(post_deploy_script, post_deploy_script_content)
        else:
            self.rm(post_deploy_script)

        database = self.application.settings.get('database')
        retcode = database.update('update project '
                                   'set project=%s, baseurl=%s, devbranch=%s, qabranch=%s, defbranch=%s,'
                                  ' username=%s, password=%s, checkout=%s, deploy=%s ,pre_build_script=%s ,'
                                  'build_script=%s,post_build_script=%s,pre_deploy_script=%s,post_deploy_script=%s'
                                   ' where pid = %s', project, baseurl, devbranch, qabranch, defbranch,
                                  username, password, checkout, deploy,pre_build_script,build_script,
                                  post_build_script,pre_deploy_script,post_deploy_script, pid)

        return {'result': retcode}

    def query(self, *args, **kwargs):
        pid = self.get_argument('pid', default='')
        database = self.application.settings.get('database')
        if pid:
            query_sql = 'select * from porject where pid = %s'
            result = database.query(query_sql, pid)
        else:
            query_sql = 'select project from project'
            result = database.query(query_sql)

        return {'retcode':0, 'result': result}

    def touch(self, script, content):
        filename = os.path.join(options.script, script)
        parent = os.path.dirname(filename)
        if not os.path.exists(parent):
            os.makedirs(parent)
        with open(filename, 'w') as f:
            fcntl(f, F_EXLCK)
            f.write(content.replace('\r', ''))

    def rm(self, script):
        filename = os.path.join(options.script, script)
        os.remove(filename)