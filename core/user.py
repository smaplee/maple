from core.base import BaseHandler
from ldap3 import Server, \
    Connection, \
    AUTO_BIND_NO_TLS, \
    SUBTREE, \
    ALL_ATTRIBUTES, \
    BASE, \
    LEVEL


class User(BaseHandler):

    def add(self, *args, **kwargs):
        pass

    def remove(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def query(self, *args, **kwargs):
        pass
