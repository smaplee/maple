from tornado.options import define
from tornado.options import parse_config_file


def parser():
    define('script', default='/var/maple/')
    define('dbhost', default='localhost')
    define('dbuser', default='root')
    define('dbpass', default='')
    define('db', default='maple')
    parse_config_file('/etc/maple/default.conf')