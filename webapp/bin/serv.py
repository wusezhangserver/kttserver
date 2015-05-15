#!/usr/bin/python
#coding=utf-8
#app path build-ups
# author Rowland
# edit 2014-03-19 14:17:30

import os
import sys
import json
import getopt
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'lib'))

import tornado.ioloop
import tornado.web
from tornado.log import access_log, gen_log

import path
from util.route import Router
from util.tools import Log
import c


class Xroute(tornado.web.RequestHandler):
    '''doorlet'''
    def prepare(self):
        # 获得正确的客户端ip
        ip = self.request.headers.get("X-Real-Ip", self.request.remote_ip)
        ip = self.request.headers.get("X-Forwarded-For", ip)
        ip = ip.split(',')[0].strip()
        self.request.remote_ip = ip
        # 允许跨域请求
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Allow", "GET,HEAD,POST")
        if self.request.method == "OPTIONS":
            self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.set_header("Access-Control-Allow-Headers", "Accept, Cache-Control, Content-Type")
            self.finish()
            return
        else:
            self.set_header("Cache-Control", "no-cache")
        # 分析请求参数
        self._data_type = self.get_argument('data_type', None)
        self._data_key = self.get_argument('data_key', None)
        self.json_args = {}
        self.data_cipher = None
        self.esun_session = None
        # json格式请求
        if self.request.headers.get('Content-Type', '').find("application/json") >= 0:
            try:
                self.json_args = json.loads(self.request.body)
                return
            except Exception as ex:
                self.send_error(400)
                return
        # 普通参数请求
        if not (self._data_key and self._data_type):
            self.json_args = dict((k, v[-1]) for k, v in self.request.arguments.items())
            return

    def ok(self, data):
        """组织处理成功的返回报文内容
        """
        ret = json.dumps({
                'message': 'OK',
                'data': data,
            }, ensure_ascii=False, indent=2)

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        return ret

    @tornado.web.asynchronous
    def get(self, path):
        Router.get(path, self)
        
    @tornado.web.asynchronous
    def post(self, path):
        Router.post(path, self)
        
    @tornado.web.asynchronous
    def put(self, path):
        Router.put(path, self)
        
    @tornado.web.asynchronous
    def delete(self, path):
        Router.delete(path, self)


def get_application():
    return tornado.web.Application([(r"^/([^\.|]*)(?!\.\w+)$", Xroute)],
                log_function=log_request)


def init_application(conf_file):
    c.set_up(conf_file)
    Log.set_up()
    Router.set_up()


def log_request(handler):
    """http日志函数
    """
    if handler.get_status() < 400:
        log_method = access_log.info
    elif handler.get_status() < 500:
        log_method = access_log.warning
    else:
        log_method = access_log.error
    req = handler.request
    log_method('"%s %s" %d %s %.6f',
               req.method, req.uri, handler.get_status(),
               req.remote_ip, req.request_time() )


if __name__=="__main__":
    # init
    port = 8888
    includes = None
    opts, argvs = getopt.getopt(sys.argv[1:], "c:p:h")
    for op, value in opts:
        if op == '-c':
            includes = value
        elif op == '-p':
            port = int(value)
        elif op == '-h':
            print u'''使用参数启动:
                        usage: [-p|-c]
                        -p [prot] ******启动端口,默认端口:%d
                        -c <file> ******加载配置文件
                   ''' % port
            sys.exit(0)
    if not includes:
        includes = os.path.join(path._ETC_PATH, 'includes_dev.json')
        print "no configuration found!,will use [%s] instead" % includes
    # main
    init_application(includes)
    logger = Log().getLog()
    logger.info("starting..., listen [%d], configurated by (%s)", port, includes)
    application = get_application()
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

