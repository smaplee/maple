from collections import deque
from torndb import Connection
from tornado.log import app_log


class MysqlPool(object):

    def __init__(self, host='localhost', port=3306, database=None, user='root', password=None, size=10):
        self._pool = deque(maxlen=size)
        for i in xrange(size):
            try:
                dbhost = '%s:%s' %(host, port)
                print dbhost
                conn = Connection(host=dbhost, database=database, user=user, password=password, time_zone="+8:00")
                self._pool.append(conn)
            except Exception, e:
                app_log.error(e)

    def _getconnection(self):
        return self._pool.popleft()

    def _returnconnection(self, conn):
        self._pool.append(conn)

    def _execute(self, func, *parameters, **kwparameters):
        conn = self._getconnection()
        try:
            return getattr(conn, func)(*parameters, **kwparameters)

        finally:
            self._returnconnection(conn)

    def insert(self, *parameters, **kwparameters): return self._execute('insert', *parameters, **kwparameters)

    def update(self, *parameters, **kwparameters): return self._execute('update', *parameters, **kwparameters)

    def insertmany(self, *parameters, **kwparameters): return self._execute('insertmany', *parameters, **kwparameters)

    def updatemany(self, *parameters, **kwparameters): return self._execute('updatemany', *parameters, **kwparameters)

    def query(self, *parameters, **kwparameters): return self._execute('query', *parameters, **kwparameters)

    def get(self, *parameters, **kwparameters): return self._execute('get', *parameters, **kwparameters)

    def execute(self, *parameters, **kwparameters): return self._execute('execute', *parameters, **kwparameters)


class Pool(MysqlPool):
    pass