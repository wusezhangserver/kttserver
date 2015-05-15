#encoding=utf-8
from util.route import Router
from db_util import Session
from util.tools import Log

logger = Log().getLog()

class  DataCenterResourceAction(object):

    #获取数据数据中心的交易情绪指标接口#
    @Router.route(url = r"datacenter/tradeactivity", method = Router._GET|Router._POST)
    def tradeactivity_action(self,req):
        resource_entity = self.tradeactivity_resource()
        currentdate = []
        currentvalue = []
        for current_dict in  resource_entity:
            for (key,value) in current_dict.iteritems():
                if('STARTDATE'==key):
                    currentdate.append(value)
                elif('CURRENTVALUE'==key):
                    currentvalue.append(value)
        resource_entity = {'currentdate':currentdate,'currentvalue':currentvalue}
        return req.ok(resource_entity)

    #数据中心交易情绪查询操作方法#
    def tradeactivity_resource(self):
        session = Session('master')
        logger.info('数据中心交易情绪查询查询...！')
        sql = " SELECT " \
              " CONCAT(SUBSTRING(DATACENTER.STARTDATE,1,10),'-',SUBSTRING(DATACENTER.ENDDATE,1,10)) AS STARTDATE," \
              " DATACENTER.CURRENTVALUE AS CURRENTVALUE " \
              " FROM " \
              " DATACENTER_TRADEACTIVITY_RESOURCE_TABLE DATACENTER " \
              " WHERE 1 = 1 ORDER BY DATACENTER.STARTDATE DESC LIMIT 0,20"
        resources = session.select_result(sql)
        return resources


    #获取数据中心市场交易活跃度指标接口#
    @Router.route(url = r"datacenter/marketsentiment", method = Router._GET|Router._POST)
    def marketsentiment_action(self,req):
         current_resource = self.marketsentiment_resource()
         currentdate = []
         currentvalue = []
         for current_dict in current_resource:
             for (key,value) in current_dict.iteritems():
                 if('CURRENTDATE'==key):
                     currentdate.append(value)
                 elif('CURRENTVALUE'==key):
                     currentvalue.append(value)
         currentdata ={'currentdate':currentdate,'currentvalue':currentvalue}
         return req.ok(currentdata)


    #数据中心市场交易活跃度查询方法#
    def marketsentiment_resource(self):
        session = Session('master')
        logger.info('数据中心市场交易活跃度查询...！')
        sql = "SELECT SUBSTRING(DATACENTER.CURRENTDATE,1,10) AS CURRENTDATE," \
              " DATACENTER.CURRENTVALUE AS CURRENTVALUE" \
              " FROM " \
              " DATACENTER_MARKETSENTIMENT_RESOURCE_TABLE DATACENTER" \
              " WHERE 1 = 1 " \
              " ORDER BY DATACENTER.CURRENTDATE DESC LIMIT 0,15"
        result = session.select_result(sql)
        return result



    #获取数据中心融资融券余额指标接口  #
    @Router.route(url = r"datacenter/margintrade", method = Router._GET|Router._POST)
    def margintrade_action(self,req):
        start=req.json_args.get("start")
        limit=req.json_args.get("limit")
        current_resource = self.margintrade_resource(start,limit)
        current_jyrq=[]
        current_rzye = []
        current_rqye = []
        current_rzrqye = []
        for current_dict in current_resource:
             for (key,value) in current_dict.iteritems():
                 if('JYRQ'==key):
                     current_jyrq.append(value)
                 elif('RZYE'==key):
                     current_rzye.append(value)
                 elif('RQYE'==key):
                     current_rqye.append(value)
                 elif('RZRQYE'==key):
                     current_rzrqye.append(value)
        currentdata ={'jyrq':current_jyrq,'rzye':current_rzye,'rqye':current_rqye,'rzrqye':current_rzrqye}
        return req.ok(currentdata)

    #融资融券余额查询#
    def margintrade_resource(self,start,limit):
        session = Session('master')
        logger.info('融资融券余额查询...！')
        sql = " SELECT SUBSTRING(RESOURCE.JYRQ,1,10) AS JYRQ,RESOURCE.RZYE AS RZYE,RESOURCE.RQYE AS RQYE,RESOURCE.RZRQYE AS RZRQYE" \
              " FROM DATACENTER_MARGINTRADE_RESOURCE_TABLE RESOURCE" \
              " ORDER BY RESOURCE.JYRQ DESC" \
              " LIMIT %s,%s"%(start,limit)
        result = session.select_result(sql)
        return result


    #数据中心期指期货多空双方持仓统计
    @Router.route(url = r"datacenter/stockfuture", method = Router._GET|Router._POST)
    def stockfuture_action(self,req):
        current_bull_resource = self.stockfuture_resource('BULL')
        current_bear_resource = self.stockfuture_resource('BEAR')
        currentdata ={'bear':current_bear_resource['TOTALVALUE'],'bull':current_bull_resource['TOTALVALUE']}
        return req.ok(currentdata)



    #数据中心期指期货多空双方持仓查询#
    def stockfuture_resource(self,dataflag):
        session = Session('master')
        logger.info('数据中心期指期货多空双方持仓查询...！')
        sql = "SELECT SUM(TOTALVALUE) AS TOTALVALUE " \
              "FROM DATACENTER_STOCKFUTURE_RESOURCE_TABLE DATACENTER " \
              "WHERE 1=1 AND DATACENTER.DATAFLAG ='%s'"%dataflag
        result = session.select_resultone(sql)
        return result
      
      
    #国家黄金外汇储备经济指标#
    @Router.route(url = r"datacenter/forexgold", method = Router._GET|Router._POST) 
    def forexgold_action(self,req):
        current_resource = self.forexgold_resource()
        #当前时间#
        currentdate = []
        #当前时间外汇值#
        forexdata = []
        #当前时间黄金储备量#
        golddata = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('CURRENTDATE'==key):
                    currentdate.append(value)
                elif('FOREXSTORA'==key):
                    forexdata.append(value)
                elif('GOLDSTORA'==key):
                    golddata.append(value)
        currentdata ={'currentdate':currentdate,'forexdata':forexdata,'golddata':golddata}
        return req.ok(currentdata)
    
    #国家黄金外汇储备查询#
    def forexgold_resource(self):
        session = Session('master')
        logger.info('国家黄金外汇储备查询...！')
        sql = " SELECT  SUBSTRING(DATACENTER.CURRENTDATE,1,10) AS CURRENTDATE," \
              " DATACENTER.FOREXSTORA AS FOREXSTORA, " \
              " DATACENTER.GOLDSTORA AS GOLDSTORA " \
              " FROM " \
              " DATACENTER_GOLDFOREX_RESOURCE_TABLE DATACENTER " \
              " WHERE  1 = 1 ORDER BY DATACENTER.CURRENTDATE DESC LIMIT 0,25"
        result = session.select_result(sql)
        return result
     
    #波罗地海航运干货指数#
    @Router.route(url = r"datacenter/bulkcargotrans", method = Router._GET|Router._POST)
    def bulkcargotrans_action(self,req):
        current_resource = self.bulkcargotrans_resource()
        currenttime= []
        indexvalue = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('CURRENTTIME'==key):
                    currenttime.append(value)
                elif('INDEXVALUE'==key):
                    indexvalue.append(value)
        currentdata ={'currenttime':currenttime,'indexvalue':indexvalue}
        return req.ok(currentdata)
                    
    #波罗地海航运干货指数查询#
    def bulkcargotrans_resource(self):
        session = Session('master')
        logger.info('波罗地海航运干货指数查询...！')
        sql = " SELECT SUBSTRING(DATACENTER.CURRENTTIME,1,10) AS CURRENTTIME," \
              " DATACENTER.INDEXVALUE AS INDEXVALUE " \
              " FROM  DATACENTER_BULKCARGOTRANS_RESOURCE_TABLE DATACENTER  " \
              " WHERE 1=1 " \
              " ORDER BY DATACENTER.CURRENTTIME DESC LIMIT 0,25"
        result = session.select_result(sql)
        return result

    #股票账户信息指标信息查询接口#
    @Router.route(url = r"datacenter/stockaccount", method = Router._GET|Router._POST)
    def stockaccount_action(self,req):
        current_resource = self.stockaccount_resource()
        currentdate=[]
        finaleffaccnum=[]
        addaccnum=[]
        addshaccnum=[]
        addszaccnum=[]
        finalaccnum=[]
        finalszsleepnum=[]
        finalshsleepnum=[]
        finalsleepnum=[]
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('STARTDATE'==key):
                    currentdate.append(value)
                elif('ADDSUMACCNUM'==key):
                    addaccnum.append(value)
                elif('FINALSUMEFFACCNUM'==key):
                    finaleffaccnum.append(value)
                elif('ADDSHACCNUM'==key):
                    addshaccnum.append(value)
                elif('ADDSZACCNUM'==key):
                    addszaccnum.append(value)
                elif('FINALSUMACCNUM'==key):
                    finalaccnum.append(value)
                elif('FINALSUMSLEEPACCNUM'==key):
                    finalsleepnum.append(value)
                elif('FINALSZSLEEPACCNUM'==key):
                    finalszsleepnum.append(value)
                elif('FINALSHSLEEPACCNUM'==key):
                    finalshsleepnum.append(value)
        currentdata ={'currentdate':currentdate,'finaleffaccnum':finaleffaccnum,
                      'addaccnum':addaccnum,'addshaccnum':addshaccnum,
                     'addszaccnum':addszaccnum,'finalaccnum':finalaccnum,
                     'finalszsleepnum':finalszsleepnum,'finalshsleepnum':finalshsleepnum,
                     'finalsleepnum':finalsleepnum}
        return req.ok(currentdata)

    #股票账户信息指标信息查询#
    def stockaccount_resource(self):
        session = Session('master')
        logger.info('股票账户信息指标信息查询...！')
        sql=" SELECT " \
            " CONCAT(SUBSTRING(DATACENTER.STARTDATE,1,10),'-',SUBSTRING(DATACENTER.ENDDATE,1,10)) AS STARTDATE, " \
            " DATACENTER.FINALSHEFFACCNUM AS FINALSHEFFACCNUM, " \
            " DATACENTER.FINALSZEFFACCNUM AS FINALSZEFFACCNUM, " \
            " DATACENTER.FINALSUMEFFACCNUM AS FINALSUMEFFACCNUM," \
            " DATACENTER.ADDSHACCNUM AS ADDSHACCNUM, " \
            " DATACENTER.ADDSZACCNUM AS ADDSZACCNUM, " \
            " DATACENTER.ADDSUMACCNUM AS ADDSUMACCNUM, " \
            " DATACENTER.FINALSHACCNUM AS FINALSHACCNUM, " \
            " DATACENTER.FINALSZACCNUM AS FINALSZACCNUM, " \
            " DATACENTER.FINALSUMACCNUM AS FINALSUMACCNUM, " \
            " DATACENTER.FINALSZSLEEPACCNUM AS FINALSZSLEEPACCNUM," \
            " DATACENTER.FINALSHSLEEPACCNUM AS FINALSHSLEEPACCNUM, " \
            " DATACENTER.FINALSUMSLEEPACCNUM AS FINALSUMSLEEPACCNUM " \
            "FROM " \
            "DATACENTER_STOCKACCOUNT_RESOURCE_TABLE DATACENTER " \
            "WHERE " \
            "1 = 1 ORDER BY DATACENTER.STARTDATE DESC LIMIT 0,25"
        result = session.select_result(sql)
        return result


    #隔夜银行拆借利率查询接口#
    @Router.route(url = r"datacenter/shibor", method = Router._GET|Router._POST)
    def shibor_action(self,req):
        current_resource = self.shibor_resource()
        currenttime=[]
        shiboron = []
        shibor1w =[]
        shibor2w=[]
        shibor1m=[]
        shibor3m=[]
        shibor6m=[]
        shibor9m=[]
        shibor1y=[]
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('CURRENTTIME'==key):
                    currenttime.append(value)
                elif('SHIBORON'==key):
                    shiboron.append(value)
                elif('SHIBOR1W'==key):
                    shibor1w.append(value)
                elif('SHIBOR2W'==key):
                    shibor2w.append(value)
                elif('SHIBOR1M'==key):
                    shibor1m.append(value)
                elif('SHIBOR3M'==key):
                    shibor3m.append(value)
                elif('SHIBOR6M'==key):
                    shibor6m.append(value)
                elif('SHIBOR9M'==key):
                    shibor9m.append(value)
                elif('SHIBOR1Y'==key):
                    shibor1y.append(value)
        currentdata ={'currenttime':currenttime,'shiboron':shiboron,
                      'shibor1w':shibor1w,'shibor2w':shibor2w,
                     'shibor1m':shibor1m,'shibor3m':shibor3m,
                     'shibor6m':shibor6m,'shibor9m':shibor9m,
                     'shibor1y':shibor1y}
        return req.ok(currentdata)

    #隔夜银行拆借利率查询#
    def shibor_resource(self):
        session = Session('master')
        logger.info('上海银行同业拆借利率查询...!')
        SQL = " SELECT  SUBSTRING(RESOURCE.CURRENTTIME,1,10) AS CURRENTTIME , RESOURCE.SHIBORON AS SHIBORON, " \
              " RESOURCE.SHIBOR1W AS SHIBOR1W, " \
              " RESOURCE.SHIBOR2W AS SHIBOR2W, RESOURCE.SHIBOR1M AS SHIBOR1M, " \
              " RESOURCE.SHIBOR3M AS SHIBOR3M, RESOURCE.SHIBOR6M AS SHIBOR6M, " \
              " RESOURCE.SHIBOR9M AS SHIBOR9M, RESOURCE.SHIBOR1Y AS SHIBOR1Y " \
              " FROM  DATACENTER_SHIBOR_RESOURCE_TABLE AS RESOURCE LIMIT 0,25"
        result = session.select_result(SQL)
        return result

    #一年期贷款利率查询接口#
    @Router.route(url = r"datacenter/lrp", method = Router._GET|Router._POST)
    def lrp_action(self,req):
        current_resource = self.lrp_resource()
        lrp1y = []
        currenttime = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('CURRENTTIME'==key):
                    currenttime.append(value)
                elif('LRPIY'==key):
                    lrp1y.append(value)
        currentdata ={'currenttime':currenttime,'lrp1y':lrp1y}
        return req.ok(currentdata)

    #一年期贷款利率查询#
    def lrp_resource(self):
        session = Session('master')
        logger.info('一年期贷款利率查询...!')
        SQL ="SELECT  RESOURCE.LRPIY AS  LRPIY , SUBSTRING(RESOURCE.CURRENTTIME,1,10) AS CURRENTTIME " \
             "FROM  DATACENTER_LPR_RESOURCE_TABLE AS RESOURCE"
        result = session.select_result(SQL)
        return result


    #社会用电量查询接口#
    @Router.route(url = r"datacenter/socialpower", method = Router._GET|Router._POST)
    def socialpower_action(self,req):
        current_resource = self.socialpower_resource()
        socialpower = []
        currenttime = []
        changeratio = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('CURRENTTIME'==key):
                    currenttime.append(value)
                elif('SOCIALPOWER'==key):
                    socialpower.append(value)
                elif('CHANGERATIO' == key):
                    changeratio.append(value)
        currentdata ={'currenttime':currenttime,'socialpower':socialpower,'changeratio':changeratio}
        return req.ok(currentdata)


    #社会用电量查询#
    def socialpower_resource(self):
        session = Session('master')
        logger.info('社会用电量查询..!')
        SQL = " SELECT SUBSTRING(RESOURCE.CURRENTTIME,1,10) AS CURRENTTIME, " \
              " RESOURCE.SOCIALPOWER AS SOCIALPOWER, " \
              " RESOURCE.CHANGERATIO AS CHANGERATIO " \
              " FROM " \
              " DATACENTER_SOCIALPOWER_RESOURCE_TABLE AS RESOURCE"
        result = session.select_result(SQL)
        return result


    #汇丰PMI制造业指数查询接口#
    @Router.route(url = r"datacenter/pmi", method = Router._GET|Router._POST)
    def pmi_action(self,req):
        current_resource = self.pmi_source()
        statistics = []
        chinamultiplepmi = []
        hsbcmanufacturingpmi = []
        hsbcservicepmi = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if('STATISTICS'==key):
                    statistics.append(value)
                elif('CHINAMULTIPLEPMI'==key):
                    chinamultiplepmi.append(value)
                elif('HSBCMANUFACTURINGPMI' == key):
                    hsbcmanufacturingpmi.append(value)
                elif('HSBCSERVICEPMI' == key):
                    hsbcservicepmi.append(value)
        currentdata ={'statistics':statistics,'chinamultiplepmi':chinamultiplepmi,
                      'hsbcmanufacturingpmi':hsbcmanufacturingpmi,
                      'hsbcservicepmi':hsbcservicepmi}
        return req.ok(currentdata)

    #汇丰PMI制造业指数#
    def pmi_source(self):
        session = Session('master')
        SQL = " SELECT RESOURCE.STATISTICS AS STATISTICS, " \
              " RESOURCE.CHINA_MULTIPLEP_MI AS CHINAMULTIPLEPMI, " \
              " RESOURCE.HSBC_MANUFACTURING_PMI AS HSBCMANUFACTURINGPMI, " \
              " RESOURCE.HSBC_SERVICE_PMI AS HSBCSERVICEPMI " \
              " FROM DATACENTER_PMI_RESOURCE_TABLE AS RESOURCE"
        result = session.select_result(SQL)
        return result


    #美元指数资源查询接口#
    @Router.route(url = r"datacenter/dollarindex", method = Router._GET|Router._POST)
    def dollarindex_action(self,req):
        current_resource = self.dollarindex_source()
        openTime = []
        newStockPrice = []
        for current_dict in current_resource:
            for (key,value) in current_dict.iteritems():
                if ('NEWSTOCKPRICE'==key):
                    newStockPrice.append(value)
                elif('OPENTIME'==key):
                    openTime.append(value)
        currentdata = {'newstockprice':newStockPrice,'opentime':openTime}
        return req.ok(currentdata)


    #美元指数资源查询#
    def dollarindex_source(self):
        session = Session('master')
        SQL = ' SELECT RESOURCE.NEWSTOCKPRICE AS NEWSTOCKPRICE,' \
              ' SUBSTRING(RESOURCE.OPENTIME,1,10) AS OPENTIME ' \
              ' FROM DATACENTER_DOLLARINDEX_RESOURCE_TABLE RESOURCE' \
              ' ORDER BY RESOURCE.OPENTIME DESC LIMIT 0,25'
        result = session.select_result(SQL)
        return result