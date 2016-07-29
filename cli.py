from tornado.httpclient import HTTPRequest, HTTPClient
import json

URL='http://localhost:2379/v2/keys/host?dir=true&recursive=true'
request = HTTPRequest(method='GET', url=URL, body=None, allow_nonstandard_methods=True, request_timeout=0, follow_redirects=True)
response = HTTPClient().fetch(request=request)
print json.dumps(json.loads(response.body), indent=2)
