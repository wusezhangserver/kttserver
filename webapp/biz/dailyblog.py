#encoding=utf-8
from util.route import Router
from db_util import Session
from util.tools import Log

logger = Log().getLog()

class  DailyBlogResourceAction(object):

    #通过blog日子类型查询相应的日志列表#
    @Router.route(url = r"dailyblog/byresourcetype", method = Router._GET|Router._POST)
    def byresourcetype_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        bzfl =req.json_args.get("bzfl")
        bzname =req.json_args.get("bzname").strip()
        data = self.byresourcetype_resource(bzfl,start,limit,bzname)
        count = self.byresourcetype_count(bzfl,bzname)
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def byresourcetype_resource(self,bzfl,start,limit,bzname):
        session = Session('master')
        SQL = " SELECT A.BZ_NAME AS bzname, A.BZ_INTRODUCE AS bzintroduce, A.BZ_FL AS bzfl," \
              " SUBSTRING(A.CREATEDATE,1,16)  AS createDate ,A.SRC_NAME AS srcname, A.ID AS id " \
              " FROM DAILYBLOG_AUTHOR_RESOURCE_TABLE A WHERE 1 = 1" \
              " AND A.BZ_FL=%s "%(bzfl)
        if(''!=bzname):
           SQL +="AND A.BZ_NAME LIKE '%"+bzname+"%'"
        SQL += " ORDER BY  POPULATION_FLAG  DESC  LIMIT %s,%s"%(start,limit)
        logger.info('查询财经作者列表信息...！'+SQL)
        resources = session.select_result(SQL)
        return resources

    def byresourcetype_count(self,bzfl,bzname):
        session = Session('master')
        SQL = " SELECT COUNT(ID) AS COUNTS " \
              " FROM DAILYBLOG_AUTHOR_RESOURCE_TABLE A WHERE 1 = 1" \
              " AND A.BZ_FL=%s "%(bzfl)
        if(''!=bzname):
           SQL +="AND A.BZ_NAME LIKE '%"+bzname+"%'"
        logger.info('查询财经作者列表信息...！'+SQL)
        resources = session.select_resultone(SQL)
        return resources

    #通过作者ID查找当前作者所有文章的明细记录.
    @Router.route(url = r"dailyblog/authorarticles", method = Router._GET|Router._POST)
    def authorarticles_detailbyid_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        id = req.json_args.get("id")
        data = self.authorarticles_detailbyid_resource(id,start,limit)
        count =self.authorarticles_detailbyid_count(id)
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def authorarticles_detailbyid_resource(self,id,start,limit):
        session = Session('master')
        SQL =" SELECT CJXJ_DETAIL.TITLE AS title , CJXJ.SRC_NAME AS imageUrl ," \
             " SUBSTRING(CJXJ_DETAIL.PUBDATE,1,16)  AS pubDate , CJXJ_DETAIL.LINKURL AS linkUrl," \
             " CJXJ.ID AS id FROM" \
             " DAILYBLOG_RESOURCE_DETAIL_TABLE CJXJ_DETAIL , DAILYBLOG_AUTHOR_RESOURCE_TABLE CJXJ" \
             " WHERE 1=1 AND CJXJ_DETAIL.ID = %s AND  CJXJ.ID = CJXJ_DETAIL.ID" \
             " ORDER BY CJXJ_DETAIL.PUBDATE DESC LIMIT %s,%s"%(id,start,limit)
        logger.info('查找当前作者所有文章的明细记录...！'+SQL)
        resources = session.select_result(SQL)
        return resources

    def authorarticles_detailbyid_count(self,id):
        session = Session('master')
        SQL = " SELECT COUNT(ID) AS COUNTS " \
              " FROM DAILYBLOG_RESOURCE_DETAIL_TABLE CJXJ_DETAIL" \
              " WHERE 1=1 AND CJXJ_DETAIL.ID = %s"%(id)
        logger.info('查找当前作者所有文章的明细记录总条数...！'+SQL)
        resources = session.select_resultone(SQL)
        return resources

    #国内股票经济评论家当天的所有文章的明细记录.
    @Router.route(url = r"dailyblog/dailyarticles", method = Router._GET|Router._POST)
    def dailyarticles_finance_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        data = self.dailyarticles_finance_resource(start,limit)
        count =self.dailyarticles_finance_count()
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def dailyarticles_finance_resource(self,start,limit):
        session = Session('master')
        SQL ="SELECT CJXJ_DETAIL.TITLE AS title , CJXJ.SRC_NAME AS imageUrl ," \
             " SUBSTRING(CJXJ_DETAIL.PUBDATE,1,16) AS pubDate , CJXJ_DETAIL.LINKURL AS linkUrl," \
             " CJXJ.ID AS id FROM" \
             " DAILYBLOG_RESOURCE_DETAIL_TABLE CJXJ_DETAIL , DAILYBLOG_AUTHOR_RESOURCE_TABLE CJXJ" \
             " WHERE 1=1" \
             " AND  CJXJ.ID = CJXJ_DETAIL.ID" \
             " AND  CJXJ.BZ_FL = 0" \
             " AND  DATE(CJXJ_DETAIL.PUBDATE) = CURDATE()" \
             " ORDER BY CJXJ_DETAIL.PUBDATE DESC" \
             " LIMIT %s,%s"%(start,limit)
        logger.info('国内股票经济评论家当天的所有文章明细记录...！'+SQL)
        resources = session.select_result(SQL)
        return resources

    def dailyarticles_finance_count(self):
        session = Session('master')
        SQL = "  SELECT  COUNT(ID) AS COUNTS FROM  DAILYBLOG_RESOURCE_DETAIL_TABLE CJXJ_DETAIL" \
              "  WHERE DATE(CJXJ_DETAIL.PUBDATE) = CURDATE()"
        logger.info('查找当前作者所有文章的明细记录总条数...！'+SQL)
        resources = session.select_resultone(SQL)
        return resources


    #通过作者ID查找当前外汇评论家作者所有文章的明细记录.
    @Router.route(url = r"dailyblog/forexarticlesbyid", method = Router._GET|Router._POST)
    def authorforexarticles_detailbyid_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        id = req.json_args.get("id")
        data = self.authorforexarticles_detailbyid_resource(id,start,limit)
        count =self.authorforexarticles_detailbyid_count(id)
        currentdata = {'data':data,'count':count['COUNTS']}
        return req.ok(currentdata)

    def authorforexarticles_detailbyid_resource(self,id,start,limit):
        session = Session('master')
        SQL ="SELECT HSHY_RESOURCE.TITLE AS title ," \
             " SUBSTRING(HSHY_RESOURCE.PUBDATE,1,16) AS pubDate , HSHY_RESOURCE.LINKURL AS linkUrl," \
             " HSHY_RESOURCE.DESCRIPTCONTEXT AS descriptContext , HSHY_RESOURCE.IMAGEURL AS imageUrl," \
             " HSHY_RESOURCE.ID AS id " \
             " FROM" \
             " DAILYBLOG_FOREXRESOURCE_DETAIL_TABLE HSHY_RESOURCE , DAILYBLOG_AUTHOR_RESOURCE_TABLE CJXJ" \
             " WHERE 1=1" \
             " AND HSHY_RESOURCE.ID = %s " \
             " AND  CJXJ.ID = HSHY_RESOURCE.ID" \
             " ORDER BY HSHY_RESOURCE.PUBDATE DESC  LIMIT %s,%s "%(id,start,limit)
        logger.info('通过ID查找当前外汇作者所有文章的明细记录...！'+SQL)
        resources = session.select_result(SQL)
        return resources

    def authorforexarticles_detailbyid_count(self,id):
        session = Session('master')
        SQL = " SELECT COUNT(ID) AS COUNTS  FROM" \
              " DAILYBLOG_FOREXRESOURCE_DETAIL_TABLE HSHY_RESOURCE WHERE 1=1" \
              " AND HSHY_RESOURCE.ID IN ('"+id+"')"
        logger.info('通过ID查找当前外汇作者所有文章的明细总条数...！'+SQL)
        resources = session.select_resultone(SQL)
        return resources




