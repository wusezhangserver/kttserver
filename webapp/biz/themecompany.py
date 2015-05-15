#encoding=utf-8
from util.route import Router
from db_util import Session
from util.tools import Log

logger = Log().getLog()

class ThemeCompanyResourceAction():

    #获取当天的股票板块信息#
    @Router.route(url = r"themecompany/dailythemesnews", method = Router._GET|Router._POST)
    def daily_news_themes_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        count = self.daily_news_themes_count()
        data = self.daily_news_themes_data(start,limit)
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def daily_news_themes_data(self,start,limit):
        session = Session('master')
        SQL = " SELECT THEMENEWS.KEYID ,THEMENEWS.LINKURL AS linkUrl," \
              " SUBSTRING(THEMENEWS.PUBDATE,1,16) AS pubDate," \
              " THEMENEWS.TITLE AS title  FROM" \
              " STOCK_POOL_THEME_NEWS_TABLE THEMENEWS" \
              " WHERE 1 = 1" \
              " LIMIT %s,%s"%(start,limit)
        logger.info('查询当天股票板块信息接口...！SQL:'+SQL)
        result = session.select_result(SQL)
        return result


    def daily_news_themes_count(self):
        session = Session('master')
        SQL =" SELECT COUNT(*) AS COUNTS FROM STOCK_POOL_THEME_NEWS_TABLE THEMENEWS" \
             " WHERE 1 = 1"
        result = session.select_resultone(SQL)
        return result


    #获取当天的上市公司信息信息#
    @Router.route(url = r"themecompany/dailycompanynews", method = Router._GET|Router._POST)
    def daily_news_company_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        count = self.daily_news_company_count()
        data = self.daily_news_company_data(start,limit)
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def daily_news_company_data(self,start,limit):
        session = Session('master')
        SQL = " SELECT MAX(COMPANYNEWS.KEYID) AS KEYID," \
              " MAX(COMPANYNEWS.LINKURL) AS linkUrl," \
              " MAX(SUBSTRING(COMPANYNEWS.PUBDATE, 1, 16)) AS pubDate," \
              " MAX(SUBSTRING(COMPANYNEWS.TITLE, 1, 35)) AS title" \
              " FROM" \
              " STOCK_POOL_COMPANY_NEWS_TABLE COMPANYNEWS" \
              " WHERE 1 = 1" \
              " GROUP BY COMPANYNEWS.TITLE" \
              " ORDER BY COMPANYNEWS.PUBDATE DESC" \
              " LIMIT %s,%s"%(start,limit)
        logger.info('查询当天股票板块信息接口...！SQL:'+SQL)
        result = session.select_result(SQL)
        return result


    def daily_news_company_count(self):
        session = Session('master')
        SQL =" SELECT COUNT(*) AS COUNTS FROM (SELECT MAX(KEYID)" \
             " FROM STOCK_POOL_COMPANY_NEWS_TABLE COMPANYNEWS" \
             " WHERE 1 = 1 GROUP BY COMPANYNEWS.TITLE ) AS COMPANYNEWS "
        result = session.select_resultone(SQL)
        return result