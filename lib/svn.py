from subprocess import Popen, PIPE
from tornado.log import app_log
from xml import etree
import time


class SVN(object):

    def __init__(self, reporoot, username, password):
        self._reporoot = reporoot
        self._username = username
        self._password = password

    def log(self, branch, version=None):
        if not version:
            command = 'svn log {root}/{branch} -l 10' \
                      ' --username={username} ' \
                      ' --password={password} ' \
                      ' --non-interactive' \
                      ' --no-auth-cache' \
                      ' --xml'.format(
                        root=self._reporoot,
                        branch=branch,
                        username=self._username,
                        password=self._password
                    )
        else:
            command = 'svn log {root}/{branch} -r {version} ' \
                      ' --username={username} ' \
                      ' --password={password} ' \
                      ' --non-interactive ' \
                      ' --no-auth-cache ' \
                      ' --xml'.format(
                      root=self._reporoot,
                      branch=branch,
                      version=version,
                      username=self._username,
                      password=self._password
                    )
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        retcode = 1
        deadline = int(time.time()) + 60
        while True:
            if int(time.time()) < deadline:
                retcode = process.poll()
                if retcode == 0:
                    break
                else:
                    time.sleep(2)
            else:
                process.kill()
                break

        if not retcode:
            xml = process.stdout.read()
            xtree = etree.fromstring(xml)
            result = []
            for logentry in xtree.findall('logentry'):
                version = logentry.attrib['revision']
                author = logentry.find('author').text
                timestamp = logentry.find('date').text
                msg = logentry.find('msg').text
                message = '-'.join([msg, timestamp, author])
                result.append((version, message))
            return result

        else:
            app_log.error(process.stderr.read())
            return False

    def list(self, branch='trunk/'):
        command = 'svn list {root}/{branch} ' \
                      ' --username={username} ' \
                      ' --password={password}' \
                      ' --non-interactive' \
                      ' --no-auth-cache' \
                      ' --xml'.format(
                      root=self._reporoot,
                      branch = branch,
                      username=self._username,
                      password=self._password
                    )
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        deadline = int(time.time()) + 60
        retcode = 1
        while True:
            if int(time.time()) < deadline:
                retcode = process.poll()
                if retcode == 0:
                    break
                else:
                    time.sleep(2)
            else:
                process.kill()
                break

        if not retcode:
            xml = process.stdout.read()
            xtree = etree.fromstring(xml)
            result = []
            for entry in xtree.getchildren()[0].findall('entry'):
                kind = entry.attrib['kind']
                if kind == 'dir':
                    name = entry.find('name').text
                    commit = entry.find('commit')
                    author = commit.find('author').text
                    timestamp = commit.find('date').text
                    message = '-'.join([author, timestamp])
                    result.append((name, message))
            return result
        else:
            return False

    def checkout(self, branch, dst):
        assert branch == '' or dst == ''
        command = 'svn checkout {root}/{branch} {path}' \
                      ' --username={username} ' \
                      ' --password={password}' \
                      ' --non-interactive' \
                      ' --no-auth-cache'.format(
                      root=self._reporoot,
                      branch=branch,
                      path=dst,
                      username=self._username,
                      password=self._password
                    )
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        deadline = int(time.time()) + 60
        retcode = 1
        while True:
            if int(time.time()) < deadline:
                retcode = process.poll()
                if retcode == 0:
                    break
                else:
                    time.sleep(2)
            else:
                process.kill()
                break

        return retcode

    def update(self, branch, dst):
        command = 'svn update {root}/{branch} {path}' \
                      '--username={username} ' \
                      '--password={password}' \
                      '--non-interactive' \
                      '--no-auth-cache' \
                      '--xml'.format(
                      root=self._reporoot,
                      branch=branch,
                      path=dst,
                      username=self._username,
                      password=self._password
                    )
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        deadline = int(time.time()) + 60
        retcode = 1
        while True:
            if int(time.time()) < deadline:
                retcode = process.poll()
                if retcode == 0:
                    break
                else:
                    time.sleep(2)
            else:
                process.kill()
                break

        return retcode

if __name__ == '__main__':
    svn = SVN()