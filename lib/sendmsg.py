# *coding: utf-8

from tornado.httputil import HTTPServerRequest
from tornado.httpclient import HTTPClient
from tornado.options import options
from email.utils import formatdate
from tornado.log import app_log
from email.header import Header
from email import MIMEText
import smtplib
import time


def sendmail(content):
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = '{time} 项目发布'.format(time=time.strftime('%Y-%m-%d %H:%M:%S'))
    msg['From'] = ("%s<"+options.mail_user+">") % (Header('发布任务','utf-8'),)
    msg['To'] = options.to_user
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    msg['Date'] = formatdate()
    server = smtplib.SMTP()
    try:
        server.connect(options.mail_server)
        server.login(options.mail_user,options.mail_password)
        server.sendmail(options.mail_user, options.to_user, msg.as_string())
        app_log.error('send mail successfully')
    except Exception, e:
        app_log.info('send mail error: %s', e)
    finally:

        server.close()


def sendsms(content, phone):
    '''
    :param content:  content format: '&mobile=$mob&content=$msg'
    :return:
    '''
    surl = options.sms or ' http://sdk2.entinfo.cn:8061/mdsmssend.ashx'
    stoken = options.token or 'SDK-BBX-010-20970'
    spwd = options.pwd or '87F9268688CDF4109CA73340D03C8CAA'
    body = {'sn': stoken, 'pwd': spwd,'mobile': phone, 'content':phone}
    request = HTTPServerRequest(method='GET', uri=surl, body=body)
    HTTPClient().fetch(request=request)


def sendQQ(content, QQ):
    pass