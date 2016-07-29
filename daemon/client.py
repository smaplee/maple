from random import randint
from tornado.httputil import url_concat
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient


class Client(object):
    _version = 'v2'

    def __init__(self, host, ssl=None):
        assert isinstance(host, str)
        self.members = [node for node in host.split(',')]
        self._base_uri = ''
        self.protocol = 'https' if ssl else 'http'

    def baseurl(self):
        randnum = randint(0, len(self.members)-1)
        url = self.members[randnum]
        health_url = '%s://%s/health' % (self.protocol, url)
        self._base_uri = '%s://%s/v2/keys' % (self.protocol, url)
        return self.send_request(method='GET', url=health_url)

    def set(self, key, value=None, ttl=None, dir=False):
        params = {}
        if dir:
            if value:
                raise SyntaxError('Cannot create a directory with a value')

        if ttl:
            params['ttl'] = ttl

        if dir:
            params['dir'] = True

        if value:
            params['value'] = value

        uri = self._base_uri + '/' + key
        url = url_concat(uri, params)
        return self.send_request(method='PUT', url=url)

    def delete(self, key, dir=False):
        params = {}
        if dir:
            params['dir'] = True
        url = url_concat(self._base_uri, params)
        return self.send_request(method='DELETE', url=url)

    def get(self, key, dir=False, recursive=False):
        params = {}
        if dir:
            params['dir'] = dir
        if recursive:
            params['recursive'] = recursive
        url = url_concat(self._base_uri, params)
        return self.send_request(method='GET', url=url)

    def watch(self, key, dir=None, timeout=0):
        params = {}
        params['wait'] =True
        if dir:
            params['recursive'] = dir

        uri = self._base_uri + '/' + key
        url = url_concat(uri, params)
        return self.send_request(method='GET', url=url, timeout=timeout)

    def send_request(self, method, url, timeout=0):
        request = HTTPRequest(url=url, method=method, connect_timeout=timeout, request_timeout=0, allow_nonstandard_methods=True)
        client = AsyncHTTPClient()
        result = client.fetch(request=request)
        return result
