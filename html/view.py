from tornado.web import MissingArgumentError
from tornado.web import authenticated
from core.base import BaseHandler
import os

class IndexView(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        print 'index'
        self.render('index.html')


class ScreenView(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        self.render('screen.html')


class CommandView(BaseHandler):

    # @authenticated
    def get(self, *args, **kwargs):
        self.render('command.html')


class VNC(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        self.render('vnc_auto.html')


class XSHELL(BaseHandler):

    @authenticated
    def get(self, *args, **kwargs):
        self.render('vnc.html')


class Script(BaseHandler):

    def get(self, *args, **kwargs):
        try:
            script = self.get_argument('name')
        except MissingArgumentError:
            self.finish()
            return
        else:
            filename = os.path.basename(script)
            if not os.path.exists(script):
                self.write_error(404)
            else:
                self.set_header ('Content-Type', 'application/octet-stream')
                self.set_header ('Content-Disposition', 'attachment; filename='+filename)
                with open(script, 'rb') as f:
                    while True:
                        data = f.read(1000)
                        if not data:
                            break
                        self.write(data)
                self.finish()
