import json
from tornado.options import options
from tornado.httpclient import HTTPRequest
from tornado.httpclient import AsyncHTTPClient


def doPost(model):
    def warp(func):
        def do(obj, *args, **kwargs):
            server = options.saltserver or kwargs['server']
            port = options.saltport or kwargs['port']
            username = options.saltuser or kwargs['username']
            password = options.saltpasswd or kwargs['password']
            expr_form = kwargs['expr_form'] or 'list'
            url = 'http://{ip}:{port}/run'.format(ip=server, port=port)
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
            hostname = kwargs['hostname']
            function = '{model}.{func}'.format(model=model, func=func.func_name)
            body = {"username": username, "password": password, "eauth":"pam", 'client': 'local', 'tgt': hostname, 'fun': function, 'arg': args, 'expr_form': expr_form}
            request = HTTPRequest(url=url, method='POST', headers=headers, body=json.dumps(body), request_timeout=60)

            def inner(response):
                 if response.body:
                        response = json.loads(response.body)['return']
                 else:
                        response = []
                 kwargs.update({'response': response})
                 func(obj, *args, **kwargs)
            AsyncHTTPClient().fetch(request, inner)
        return do
    return warp

