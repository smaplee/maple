from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import run_on_executor
from tornado.httputil import HTTPServerRequest
from tornado.web import RequestHandler
from tornado.web import authenticated
from tornado.gen import coroutine


class BaseHandler(RequestHandler):

    def initialize(self):
        self.executor = self.application.settings.get('threads')

    @coroutine
    def prepare(self):
        # request = HTTPServerRequest(method='post', uri='/auth', headers=self.request.headers)
        # httpc = AsyncHTTPClient()
        # user = yield httpc.fetch(request=request)
        # if user:
            self.current_user = 'root'

    @coroutine
    @authenticated
    def put(self, *args, **kwargs):
        result = yield self._add(*args, **kwargs)
        self.write(result)

    @coroutine
    @authenticated
    def delete(self, *args, **kwargs):
        result = yield self._remove(*args, **kwargs)
        self.write(result)

    @coroutine
    @authenticated
    def post(self, *args, **kwargs):
        result = yield self._update(*args, **kwargs)
        self.write(result)

    @coroutine
    @authenticated
    def get(self, *args, **kwargs):
        result = yield self._query(*args, **kwargs)
        self.write(result)

    @run_on_executor
    def _add(self,*args, **kwargs):
        return self.add(*args, **kwargs)

    @run_on_executor
    def _remove(self, *args, **kwargs):
        return self.remove(*args, **kwargs)

    @run_on_executor
    def _update(self, *args, **kwargs):
        return self.update(*args, **kwargs)

    @run_on_executor
    def _query(self, *args, **kwargs):
        return self.query(*args, **kwargs)

    def add(self, *args, **kwargs): pass

    def remove(self, *args, **kwargs): pass

    def update(self, *args, **kwargs): pass

    def query(self, *args, **kwargs): pass

