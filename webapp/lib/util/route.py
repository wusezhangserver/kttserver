#!/usr/bin/python
#coding=utf-8
# author Rowland
# edit 2014-03-19 14:16:32
import os, inspect, sys, re, time, random

import tornado.ioloop, tornado.web
from concurrent import futures

import util.tools
logger = util.tools.Log().getLog()


MAX_WORKERS = 16
SORTING_PERIOD = 900 * 1000

executor = futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)



def _call_wrap(call, params):
    handler = params[0]
    try:
        logger.info('request: %s %s', handler.request.path, handler.json_args or {})
        ret = call(*params)
    except Exception as ex:
        logger.exception('system error: %s', handler.esun_session)
        tornado.ioloop.IOLoop.instance().add_callback(lambda: params[0].send_error())
    tornado.ioloop.IOLoop.instance().add_callback(lambda: params[0].finish(ret))


def sort_the_mapper():
    Router.mapper.sort(key=lambda x: x['times'], reverse=True)


class Router(object):
    '''dispather and decortor'''
    _GET = 0x001
    _POST = 0x002
    _PUT = 0x004
    _DELETE = 0x008
    _OPTIONS = 0x016
    mapper = []

    @classmethod
    def set_up(cls):
        #automic scan dirs
        import path
        files_list = os.listdir(path._BIZ_PATH)
        files_list = set([x[:x.rfind(".")] for x in files_list if x.endswith(".py")])
        map(__import__, files_list)
        tornado.ioloop.PeriodicCallback(sort_the_mapper, SORTING_PERIOD).start()

    @classmethod
    def route(cls, **deco):
        def foo(func):
            url = deco.get('url') or '/'
            if len([x for x in Router.mapper if x.get('url') == url]) == 0:
                method = deco.get('method') or Router._GET
                mapper_node = {
                    'eUrl': re.compile('^' + url + '$', re.IGNORECASE),
                    'method': method,
                    'callName': func.__name__,
                    'className': inspect.stack()[1][3],
                    'moduleName': func.__module__,
                    'times': 0l
                }
                Router.mapper.append(mapper_node)
            return func

        return foo

    @classmethod
    def get(cls, path, reqhandler):
        Router.emit(path, reqhandler, Router._GET)

    @classmethod
    def post(cls, path, reqhandler):
        Router.emit(path, reqhandler, Router._POST)

    @classmethod
    def put(cls, path, reqhandler):
        Router.emit(path, reqhandler, Router._PUT)

    @classmethod
    def delete(cls, path, reqhandler):
        Router.emit(path, reqhandler, Router._DELETE)

    @classmethod
    def options(cls, path, reqhandler):
        Router.emit(path, reqhandler, Router._OPTIONS)

    @classmethod
    def verify_passport(cls, eUrl):
        '''
        @param cls:
        @param eUrl:
        @return:
        密度 C = 当前排队的任务 / 线程数量
        密度大于80% 开始有选择性的拒绝服务
            选择策略：
                选取优先级队列中后面 C 个的url进行 C 概率随机拒绝服务以保障优先级高的请求得到响应
        '''
        capacity = 0 if len(executor._threads) == 0 else executor._work_queue.qsize() / (len(executor._threads))
        if capacity >= 1.0:
            #排队满，拒绝受理请求
            return False
        capacity = 1.0 if capacity > 1.0 else capacity
        if 0.8 < capacity:
            index = len(Router.mapper) - 1
            for i in range(len(Router.mapper)):
                if Router.mapper[i]['eUrl'] == eUrl:
                    index = i
            if random.random() < capacity and 1 - capacity < float(index) / len(Router.mapper):
                return False
        return True

    @classmethod
    def emit(cls, path, reqhandler, method_flag):
        mapper = Router.mapper
        for mapper_node in mapper:
            urlExp = mapper_node['eUrl']
            m = urlExp.match(path)
            if m:
                params = (reqhandler,)
                for items in m.groups():
                    params += (items,)
                    # mapper_node = mapper.get(urlExp)
                method = mapper_node.get('method')
                if method_flag != method_flag & method:
                    logger.warn("method refuse!uri=%s,method=%d,parameters=|%s|", path, method_flag,
                                reqhandler.request.arguments or "")
                    raise tornado.web.HTTPError(405)
                callName = mapper_node.get('callName')
                className = mapper_node.get('className')
                moduleName = mapper_node.get('moduleName')
                # -----------------------------
                module = __import__(moduleName)
                clazz = getattr(module, className)
                try:
                    obj = clazz()
                except Exception, e:
                    logger.exception("error occured when creating instance of %s" % className)
                    raise tornado.web.HTTPError(500)
                call = getattr(obj, callName)
                if not call:
                    raise tornado.web.HTTPError(405)
                    # -----------------------------
                # 在提交任务到线程池之前判断线程池压力，如果压力过大，只提交优先级高的作业，对于优先级低的作业
                # 直接拒绝服务503
                if Router.verify_passport(urlExp):
                    mapper_node['times'] += 1
                    executor.submit(_call_wrap, call, params)
                else:
                    logger.warn("服务器压力过大 线程数[%d] 任务数[%d] 拒绝服务[%s] url队列(总数%d)中排名{%d] ",
                                len(executor._threads),
                                executor._work_queue.qsize(),
                                path,
                                len(Router.mapper),
                                Router.mapper.index([x for x in Router.mapper if x['eUrl'] == urlExp].pop()))
                    raise tornado.web.HTTPError(503)
                break
        else:
            logger.warn("not found!uri=%s,method=%d,parameters=|%s|", path, method_flag,
                        reqhandler.request.arguments or "")
            raise tornado.web.HTTPError(404)
            


