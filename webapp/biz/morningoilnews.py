#encoding=utf-8
from util.route import Router
from db_util import Session
from util.tools import Log

logger = Log().getLog()

class MorningOilNewsResourceAction():

      #查询当天早财新闻石油板块信息#
      @Router.route(url = r"morningnews/oilnews", method = Router._GET|Router._POST)
      def oil_morningnews_action(self,req):
          start=req.json_args.get("start")
          limit=req.json_args.get("limit")
          count = self.query_morningnews_count()
          data = self.query_morningnews_data(start,limit)
          currentdata = {'data':data,'count':count['COUNTS']}
          return req.ok(currentdata)

      #查询原油新闻详情通用查询接口#
      def query_morningnews_data(self,start,limit):
          session = Session('master')
          SQL = " SELECT NEWS.TITLE AS title, NEWS.IMAGEURL AS imageUrl, " \
              " SUBSTRING(NEWS.PUBDATE,1,16) AS pubDate, " \
              " NEWS.LINKURL AS linkUrl , " \
              " NEWS.DESCRIPTCONTEXT AS descriptContext " \
              " FROM  MORNING_OILNEWS_RESOURCE_TABLE  NEWS  " \
              " WHERE  1=1 " \
              " ORDER BY  NEWS.PUBDATE DESC  " \
              " LIMIT %s,%s"%(start,limit)
          logger.info('查询原油新闻详情通用查询接口...！SQL:'+SQL)
          result = session.select_result(SQL)
          return result

       #查询原油新闻总条数查询接口#
      def query_morningnews_count(self):
          session = Session('master')
          SQL = " SELECT COUNT(*) AS COUNTS FROM  MORNING_OILNEWS_RESOURCE_TABLE  NEWS  " \
              " WHERE  1=1  "
          logger.info('查询原油新闻总条数查询接口'+SQL)
          result = session.select_resultone(SQL)
          return result
