# *coding: utf-8
from concurrent.futures import ThreadPoolExecutor
from tornado.ioloop import PeriodicCallback
from tornado.httpserver import HTTPServer
from tornado.options import options
from tornado.web import Application
from tornado.ioloop import IOLoop
from lib.parse import parser
from lib.db import Pool
import os

########## View ##################
from html.view import CommandView
from html.view import IndexView
from html.view import XSHELL
from html.view import VNC
from html.view import Script

######### Model ##################
from core.template import Template
from core.version import Version
from core.auth import Authenticate
from core.deploy import DeployTask
from core.service import Service
from core.command import CMD
from core.host import Host
from core.user import User



def app():
    app = Application([

        # Basic
        ('/auth', Authenticate),

        # View
        ('^/(|index.html)$', IndexView),
        ('/view/command.html', CommandView),
        ('/view/bash.html', XSHELL),
        ('/view/vnc.html', VNC),

        # Model
        ('/host', Host),
        ('/user', User),
        ('/service', Service),
        ('/template', Template),
        ('/deploy', DeployTask),
        ('/version', Version),
        ('/command', CMD),

        # VNC
        ('/VNC', VNC),

        # XSHELL
        ('/xshell', XSHELL),

        # script
        ('/script', Script)
        ],
        template_path=os.path.join(os.path.dirname(__file__), 'template'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        compiled_template_cache=False,
        threads=ThreadPoolExecutor(max_workers=8),
        database=Pool(
            host=options.dbhost,
            user=options.dbuser,
            password=options.dbpass,
            database=options.db,
            size=10
        )
    )
    return app

if __name__ == '__main__':
    parser()
    app = app()
    server = HTTPServer(app)
    server.bind(80)
    server.start(2)
    IOLoop.current().start()