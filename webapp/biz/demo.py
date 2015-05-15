#encoding=utf-8
import datetime
from util.route import Router
from entity import resModel
from db_util import Session
from util.tools import Log

logger = Log().getLog()



class KtResourceAction(object):
    """映射http的方法类似于action层，不要写业务代码！"""
    @Router.route(url = r"me/what", method = Router._GET|Router._POST) 
    def offer_resources(self,req):
        resource_entity = self.get_resource("http://upload.cnforex.com/images/2014/3/10/140310140521521.jpg.cnforex")
        resource_entity = resource_entity[0]
        resource_entity['CREATEDATE'] =resource_entity['CREATEDATE'].strftime('%Y-%m-%d %H:%M:%S')
        return req.ok(resource_entity)

    """在单独的业务方法里面写"""
    def get_resource(self, id):
        session = Session('master')
        logger.info('begin tx')
        resources = session.select(resModel.Resource, {"ID":id})
        return resources
