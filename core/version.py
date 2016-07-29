from core.base import BaseHandler
from lib.svn import SVN


class Version(BaseHandler):

    def query(self, *args, **kwargs):
        project = self.get_argument('project')
        branch = self.get_argument('branch')
        database = self.application.settings.get('database')
        information = database.get('select * from project where project=%s', project)
        if information['resource'] == 'svn':
            result = self.svn(information, branch)
            return {'result': result}

        if information['resource'] == 'git':
            result = self.git(information, branch)
            return {'result': result}

    def svn(self, information, branch):
        baseurl = information['baseurl']
        username = information['username']
        password = information['password']
        branch = information[branch]
        svn = SVN(reporoot=baseurl, username=username, password=password)
        return svn.log(branch=branch)

    def git(self, information, branch):
        return ''