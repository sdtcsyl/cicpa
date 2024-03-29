# -*- coding: utf-8 -*-
"""
Created on May 15 2019
"""

import sqlite3
import files as Files

class database:
    def __init__(self, db):
        self.db = db
        self.tables = []
        self.conn = sqlite3.connect(Files.db_path + self.db + '.db')
        self.conn.close() 
        
    def get_table(self, name):        
        return table(self.db, name)        

'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''

class table:
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self.fields=[]
        self.types = []
        self.primary_key = []
        self.foreign_key = ''
    
    def string_fields(self):
        return ','.join(self.fields)
    
    def string_fields_types(self):
        return ','.join([field + ' ' + fieldtype + ' primary key'   if field in self.primary_key else field + ' ' + fieldtype for field, fieldtype in zip(self.fields, self.types)])
    
    def string_qmarks(self):
        return ','.join(['?']*len(self.fields))
    
    def add_foreign_key(self, flds, tbs, tbs_flds):
        '''please use it before create_table'''
        self.foreign_key = ','.join([' FOREIGN KEY (' + fld + ') REFERENCES table_' + tb + ' (' + tbs_fld + ')' for fld, tb, tbs_fld in zip(flds, tbs, tbs_flds)])
        return self.foreign_key
   
    def sql_create_table(self):
        sql = 'create table if not exists table_' + self.name + ' (' +  self.string_fields_types() + self.foreign_key +  ')'
        return sql
     
    def sql_insert_table(self):
        sql = 'insert into table_' + self.name + ' (' +  self.string_fields() + ')values (' + self.string_qmarks() +')'
        return sql
    
    def sql_drop_table(self):
        sql = 'DROP table if exists table_' + self.name
        return sql
    
    def exe_sql(self, sql, **kwargs):
        conn = sqlite3.connect(Files.db_path + self.db + '.db')
        cursor = conn.cursor()
        if len(kwargs) == 0:
            cursor.execute(sql)
        else:
            if 'data' in kwargs:
                try:
                    cursor.execute(sql, (kwargs['data']))   #insert data
                except sqlite3.IntegrityError:
                    pass
        cursor.close()
        conn.commit()
        conn.close() 

    def exe_sql_w_return(self, sql, **kwargs):
        conn = sqlite3.connect(Files.db_path + self.db + '.db')
        cursor = conn.cursor()
        if len(kwargs) == 0:
            cursor.execute(sql)
        else:
            if 'data' in kwargs:
                try:
                    cursor.execute(sql, (kwargs['data']))   #insert data
                except sqlite3.IntegrityError:
                    pass
        res =cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close() 
        return res

    def func_write_table(self, data):        
        self.exe_sql(self.sql_create_table())
        self.exe_sql(self.sql_insert_table(), data=data)
        
    def func_count_by_and(self, vares, var_operators, var_values): 
        condition = ' and '.join([var+' '+ var_operator +" '"+  var_value+ "' " for var, var_operator, var_value in zip(vares, var_operators, var_values)  ])
        sql = 'select count(*) from table_' + self.name + ' where ' +  condition
        counts = self.exe_sql_w_return(sql)
        return counts[0][0]
    
    def func_count_by_or(self, vares, var_operators, var_values): 
        condition = ' or '.join([var+' '+ var_operator +" '"+  var_value+ "' " for var, var_operator, var_value in zip(vares, var_operators, var_values)  ])
        sql = 'select count(*) from table_' + self.name + ' where ' +  condition
        counts = self.exe_sql_w_return(sql)
        return counts[0][0]
    
    #def func_check_w_table(self, other_table):
        
        
    
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''

class table_main(table):
    def __init__(self, db):
        super(table_main,self).__init__(db,'main')
        self.fields = ['swsbm',   ##
                     'web',   ##
                     'swsmc',   ##
                     'txdz',   ##
                     'lxr',   ##
                     'lxdh',   ##
                     'sf',   ##
                     'Page',   ##
                     'isSubsidary',   ##
                     'basic_NY',   ##
                     'register_NY',   ##
                     'other_NY',   ##
                     'no_qualifications',   ##
                     'no_overseasCPA',   ##
                     'overseasCPA_NY',   ##
                     'no_staff',   ##
                     'pages_staff',   ##
                     'staff_NY',   ##
                     'no_cpa',   ##
                     'pages_cpa',   ##
                     'cpa_NY',   ##
                     'no_partners',   ##
                     'pages_partners',   ##
                     'partners_NY',   ##
                     'no_subsidiaries',   ##
                     'subsidiaries_NY',   ##
                     'no_overseas',   ##
                     'pages_overseas',   ##
                     'overseas_NY',   ##
                     'no_subinfo',   ##
                     'pages_subinfo',   ##
                     'subinfo_NY',   ##
                     'cpainfo',   ##
                     'pages_cpainfo',   ##
                     'cpainfo_NY',   ##
                     'no_overseasbranch',   ##
                     'pages_overseasbrach',   ##
                     'overseasbranch_NY',   ##
                     'no_charity',   ##
                     'pages_charity',   ##
                     'charity_NY',   ##
                     'no_check',   ##
                     'pages_check',   ##
                     'check_NY']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['swsbm']
        self.exe_sql(self.sql_create_table())

    def func_count_by_sf(self, sf): #按照省份来数个数
        counts = self.func_count_by_and('sf','=',sf)
        #sql = 'select count(*) from table_' + self.name + ' where sf = ' +  "'" + (sf) + "'"
        #counts = self.exe_sql_w_return(sql)
        return counts[0][0]
    
    def func_select_swsbm_web(self):
        sql = 'select swsbm, web from table_' + self.name
        counts = self.exe_sql_w_return(sql)
        return counts
    
    def func_update(self, swsbm, fld, fld_val):
        sql = 'UPDATE table_' + self.name + ' SET ' + fld +' = ' + "'" + str(fld_val) + "'"  + ' WHERE swsbm = ' +  "'" + str(swsbm) + "'" 
        self.exe_sql(sql)

    def func_check_w_basic(self):
        sql = 'select swsbm, web from table_main where swsbm not in (select gsbm from table_basic)'
        return self.exe_sql_w_return(sql)
        

'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
   
class table_basic(table):
    def __init__(self, db):
        super(table_basic,self).__init__(db,'basic')
        self.fields = [
                        ## basic info
                        'swsswsmc',  ##会计师事务所名称
                        'gsbm',   ##证书编号
                        'lxr',  ##联系人
                        'lxdh', ##联系电话
                        'bgdz', ##办公地址  
                        
                        'cz',   ##传真
                        'txdz',   ##通讯地址                   
                        'yzbm', ##邮政编码
                        'dzyx', ##电子邮箱
                        'wz',   ##网址
                        
                        ## register info
                        'pzsljg',   ## 批准设立机关
                        'pzslwjh',  ## 批准设立文件号   
                        'pzslsj',   ##批准设立时间
                        'fddbr',    ##法定代表人（或执行合伙人）
                        'czehzczb', ##出资额或注册资本 (万元）                        
                        
                        'zzxs',     ##组织形式 （有限/合伙）
                        'zrkjs',    ##主任会计师
                        'fssl',     ##分所数量 
                        'web_partner',                        
                        'hhrrs',    ##合伙人或股东人数
                        
                        'web_cpa',
                        'kjsrs',    ##注册会计师人数  
                        'web_staff',
                        'cyryrs',   ##从业人员人数
                        'kjsrshfs', ##注册会计师人数（含分所）
                        
                        'cyryrshfs',   ##从业人员人数（含分所）                    
                        ## age info
                        'dy70srs',  ##大于70岁人数
                        'xydy70sqdy60srs',  ##小于等于70岁且大于60岁人数
                        'xydy60sqdy40srs',   ## 小于等于60岁且大于40岁人数                   
                        'xydy40srs',    ##小于等于40岁人数
                        
                        ## degree
                        'bsyjsrs',    ## 博士研究生人数                   
                        'ssyjsrs',      ## 硕士研究生人数
                        'bkrs',         ## 本科人数
                        'dzjyxrs',      ## 大专及以下人数
                        ## qulifications
                        'sfxdzqqhxgywxkz',    ## 是否取得证券、期货相关业务许可证
                        
                        'qdzqqhxgywxkzwsj',     ##取得证券、期货相关业务许可证时间
                        'zgzsh',        ##资格证书号                        
                        ## network
                        'web_jrgjwl',
                        'jrgjwl',   ## 加入国际网络
                        'web_jwfzjg',
                        'jwfzjg',   ## 境外分支机构                        
                        ## comprehensive
                        'sfjynbpxzg',   ## 是否具有内部培训资格
                        
                        'jxjywcl',  ##继续教育完成率（上一年度）
                        'web_cfczxx',
                        'cfczxx',   ##处罚/惩戒信息(披露时限:自2016年至今) 
                        'web_bjcxx',
                        'bjcxx',     ##被检查信息                        
                        'web_cygyhd',
                        
                        'cygyhd',   ## 参与公益活动               
                        
                        ##执行业务信息
                        'web_zxywxx',
                        'zxywxx'  ##执行业务信息
                        ]   ##
        self.types = ['varchar(3)']*len(self.fields)
        self.primary_key = ['gsbm']
        #self.add_foreign_key('gsbm','main','swsbm')
        #self.exe_sql(self.sql_create_table())


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''



class table_subsidiaries(table):
    def __init__(self, db):
        super(table_subsidiaries,self).__init__(db,'subsidiaries')
        self.fields = ['gsbm', ### from  table_main
                        'id',
                        
                        'bh',   ##'序号'
                        'web_sub',
                        'fsmc',  ###分所名称
                        'fsfzr',   ###分所负责人
                        'dh',   ###电话          
                        'dzyx' ###电子邮箱
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''   
   
class table_qualifications(table):
    def __init__(self, db):
        super(table_qualifications,self).__init__(db,'qualifications')
        self.fields = ['gsbm',  ### from  table_main
                        'id',
                        'bh',   ##'序号'
                        'qddqtzyzgmc',  ###取得的其他执业资质名称 
                        'zgqdsj',   ###资格取得时间
                        
                        'pzjg' ###批准机关
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
   
class table_overseascpa(table):
    def __init__(self, db):
        super(table_overseascpa,self).__init__(db,'overseascpa')
        self.fields = ['gsbm',  ### from  table_main
                        'id',
                        'bh',   ##'序号'
                        'web_zsmc', 
                        'zsmc',     ##注师名称
                        'jwzg',     ##境外资格中文名称
                        
                        'ywmc',     ##英文名称（简称）
                        'qdsj',     ##取得时间
                        'zsbh',     ##证书编号
                        'qdsd']   ##取得地点
        self.types = ['varchar(3)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
   
class table_subinfo(table):
    def __init__(self, db):
        super(table_subinfo,self).__init__(db,'subinfo')
        self.fields = ['id',
                        'fsmc', ##分所名称
                        'zszsbh',##主所证书编号
                        'fsbh', ##分所编号
                        'szcs', ##所在城市
                        
                        'yzbm', ##邮政编码
                        'dzyx', ##电子邮箱
                        'cz',   ##传真   
                        'lxdh', ##联系电话
                        'clpzsj',##成立批准时间
                        
                        'clpzwh',##成立批准文号  
                        'clpzjg', ##成立批准机关
                        'fsfzr', ##分所负责人                        
                        'wz',##网址
                        'zckjszs',##注册会计师总数
                        'cyryzs',##从业人员总数
                        
                        'cfcjxx',##处罚/惩戒信息(披露时限:自2016年至今)
                        'bgdz', ##办公地址
                        'web_cpa',
                        'web_staff',
                        'web_cfcjxx']   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_check_subsidiaries_diff(self):
        ## check subisidiaries number with table_subsidiaries.
        sql = 'select count(*) from table_subsidiaries;'
        res = self.exe_sql_w_return(sql)
        sql = 'select count(*) from table_subinfo;'
        res2 = self.exe_sql_w_return(sql)
        return res2[0]-res[0]
        


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
   
class table_cpa(table):
    def __init__(self, db):
        super(table_cpa,self).__init__(db,'cpa')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'web_xm', ##
                        'xm', ##姓名
                        'rybh', ##人员编号
                        
                        'xb', ##性别
                        'csrq', ##出生日期
                        'qkhgzh' ##全科合格证号（或者考核批准文号） 
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_cpa_from_basic(self):
        sql = 'select gsbm, web_cpa from table_basic'
        return self.exe_sql_w_return(sql)

    def func_select_cpa_from_subinfo(self):
        sql = 'select id, web_cpa from table_subinfo'
        return self.exe_sql_w_return(sql)

    def func_check_cpa_diff(self):
        sql = 'select a.gsbm, a.hhrrs, b.hhrrs from (select gsbm, substr(kjsrs, 0, instr(kjsrs,"（")) as hhrrs from table_basic) a left join (select distinct gsbm, count(*) hhrrs from table_cpa group by gsbm) b on a.gsbm = b.gsbm where cast(a.hhrrs as integer) != cast(b.hhrrs as integer);'
        res = self.exe_sql_w_return(sql)
        sql = 'select gsbm, substr(kjsrs, 0, instr(kjsrs,"（")), 0 from table_basic where gsbm not in (select distinct gsbm from table_staff) and cast(cyryrs as integer) >0;'
        res += self.exe_sql_w_return(sql)
        sql = 'select a.gsbm, a.hhrrs, b.hhrrs from (select id gsbm, substr(zckjszs, 0, instr(zckjszs,"（")) as hhrrs from table_subinfo) a left join (select distinct gsbm, count(*) hhrrs from table_cpa group by gsbm) b on a.gsbm = b.gsbm where cast(a.hhrrs as integer) != cast(b.hhrrs as integer);'
        res = self.exe_sql_w_return(sql)
        sql = 'select id, substr(zckjszs, 0, instr(zckjszs,"（")), 0 from table_subinfo where id not in (select distinct gsbm from table_cpa) and cast(zckjszs as integer) >0;'
        res += self.exe_sql_w_return(sql)
        return res


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_partner(table):
    def __init__(self, db):
        super(table_partner,self).__init__(db,'partner')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'xm', ##合伙人（股东）姓名
                        'sfzs', ##是否注师
                        
                        'zsbh' ##注师编号
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_partner(self):
        sql = 'select gsbm, web_partner from table_basic'
        return self.exe_sql_w_return(sql)
    
    def func_check_partner_diff_w_basic(self):
        sql = 'select a.gsbm, a.hhrrs, b.hhrrs from (select gsbm, substr(hhrrs, 0, instr(hhrrs,"（")) as hhrrs from table_basic) a left join (select distinct gsbm, count(*) hhrrs from table_partner group by gsbm) b on a.gsbm = b.gsbm where cast(a.hhrrs as integer) <> cast(b.hhrrs as integer);'
        res = self.exe_sql_w_return(sql)
        sql = 'select gsbm, substr(hhrrs, 0, instr(hhrrs,"（")), 0 from table_basic where gsbm not in (select distinct gsbm from table_partner) and cast(substr(hhrrs, 0, instr(hhrrs,"（")) as integer) >0;'
        res += self.exe_sql_w_return(sql)
        return res
        
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_staff(table):
    def __init__(self, db):
        super(table_staff,self).__init__(db,'staff')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'xm', ##姓名
                        'xb',   ##性别
                        'jssj',##进所时间
                        'sfqht',##是否签合同
                        'sfcjsb',##是否参加社保
                        'sfdy'##是否党员
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_staff(self):
        sql = 'select gsbm, web_staff from table_basic'
        res =  self.exe_sql_w_return(sql)
        sql = 'select id, web_staff from table_subinfo'
        res +=  self.exe_sql_w_return(sql)
        return res

    def func_check_staff_diff(self):
        sql = 'select a.gsbm, a.hhrrs, b.hhrrs from (select gsbm, substr(cyryrs, 0, instr(cyryrs,"（")) as hhrrs from table_basic) a left join (select distinct gsbm, count(*) hhrrs from table_staff group by gsbm) b on a.gsbm = b.gsbm where cast(a.hhrrs as integer) != cast(b.hhrrs as integer);'
        res = self.exe_sql_w_return(sql)
        sql = 'select gsbm, substr(cyryrs, 0, instr(cyryrs,"（")), 0 from table_basic where gsbm not in (select distinct gsbm from table_staff) and cast(cyryrs as integer) >0;'
        res += self.exe_sql_w_return(sql)
        sql = 'select a.gsbm, a.hhrrs, b.hhrrs from (select id gsbm, substr(cyryzs, 0, instr(cyryrs,"（")) as hhrrs from table_subinfo) a left join (select distinct gsbm, count(*) hhrrs from table_staff group by gsbm) b on a.gsbm = b.gsbm where cast(a.hhrrs as integer) != cast(b.hhrrs as integer);'
        res = self.exe_sql_w_return(sql)
        sql = 'select id, substr(cyryzs, 0, instr(cyryzs,"（")), 0 from table_subinfo where id not in (select distinct gsbm from table_staff) and cast(cyryzs as integer) >0;'
        res += self.exe_sql_w_return(sql)
        return res

'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_charity(table):
    def __init__(self, db):
        super(table_charity,self).__init__(db,'charity')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'gyhdmc', ##公益活动名称
                        'hdzbdw',   ##活动主办单位
                        'cjhdsj',##参加活动时间
                        'cjhdfsjzynr'##参与活动方式及主要内容
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_charity(self):
        sql = 'select gsbm, web_cygyhd from table_basic'
        res =  self.exe_sql_w_return(sql)
        return res


'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_check(table):
    def __init__(self, db):
        super(table_check,self).__init__(db,'check')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'jcxh', ##检查协会
                        'jsjcnd' ##接受检查年度
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_check(self):
        sql = 'select gsbm, web_bjcxx from table_basic'
        res =  self.exe_sql_w_return(sql)
        return res    



'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_overseas(table):
    def __init__(self, db):
        super(table_overseas,self).__init__(db,'overseas')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'jrsj', ##加入时间
                        'gjkjgsmc', ##国际会计公司名称
                        'zbzcd', ##总部注册地
                        'dz', ##地址
                        'dh', ##电话
                        'cz', ##传真
                        'fzr', ##负责人
                        'dzyx', ##电子邮件
                        'wz'  ##网址
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_overseas(self):
        sql = 'select gsbm, web_jrgjwl from table_basic'
        res =  self.exe_sql_w_return(sql)
        return res
    
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_overseasbranch(table):
    def __init__(self, db):
        super(table_overseasbranch,self).__init__(db,'overseasbranch')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'fzjgmc', ##分支机构名称
                        'slsj', ##设立时间
                        'szcs', ##所在城市
                        'fzr', ##负责人
                        'ygrs' ##员工人数
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_overseasbranch(self):
        sql = 'select gsbm, web_jwfzjg from table_basic'
        res =  self.exe_sql_w_return(sql)
        return res    

    
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_punishoff(table):
    def __init__(self, db):
        super(table_punishoff,self).__init__(db,'punishoffs')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'swsmc', ##事务所名称
                        'swsbh', ##事务所编号
                        'cfcjsj', ##处罚/惩戒时间
                        'sscfcjbm', ##实施处罚/惩戒的部门
                        'yy', ##原因
                        'cfcjjl', ##处罚/惩戒种类
                        'cfcjcs', ##处罚/惩戒措施
                        'cfcjwjh' ##处罚/惩戒文件号
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_punishoff(self):
        sql = 'select gsbm, web_cfczxx from table_basic where web_cfczxx <> ""'
        res =  self.exe_sql_w_return(sql)
        return res    
   
    def func_select_punishoff_f_subinfo(self):
        sql = 'select id, web_cfcjxx from table_subinfo where web_cfcjxx <> ""'
        res =  self.exe_sql_w_return(sql)
        return res  
    
    ### We check the punishoff table with subinfo and basic tables where punished link is not null
    ### there are lots of office have no punish information
    def func_check_punishoff(self):
        sql = 'select id, web_cfcjxx  from table_subinfo where id not in (select distinct gsbm from table_punishoffs) and web_cfcjxx <>"" union select gsbm, web_cfczxx  from table_basic where gsbm not in (select distinct gsbm from table_punishoffs) and web_cfczxx <>"";'
        res =  self.exe_sql_w_return(sql)
        return res  

    def func_check_w_basic(self):
        sql = 'select gsbm, web_cfczxx from table_basic where gsbm not in (select gsbm from table_regdisplays) and gsbm not in (select gsbm from table_punishoffs) and web_cfczxx <>"";'
        res =  self.exe_sql_w_return(sql)
        return res  
    
    
    
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_regdisplay(table):
    def __init__(self, db):
        super(table_regdisplay,self).__init__(db,'regdisplays')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'bh',##编号
                        'zsxm', ##注师姓名
                        'zsbh', ##注师编号
                        'cfcjsj', ##处罚/惩戒时间
                        'sscfcjbm', ##实施处罚/惩戒的部门
                        'yy', ##原因
                        'cfcjjl', ##处罚/惩戒种类
                        'cfcjcs', ##处罚/惩戒措施
                        'cfcjwjh', ##处罚/惩戒文件号
                        'scfsszsws'##受处罚/惩戒时所在事务所
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_regdisplay(self):
        sql = 'select gsbm, web_cfczxx from table_basic where web_cfczxx <> ""'
        res =  self.exe_sql_w_return(sql)
        return res   
   
    def func_select_regdisplay_f_subinfo(self):
        sql = 'select id, web_cfcjxx from table_subinfo where web_cfcjxx <> ""'
        res =  self.exe_sql_w_return(sql)
        return res  
    
    
    ### We check the regdisplay table with subinfo and basic tables where punished link is not null
    ### there are lots of personal have no punish information
    def func_check_regdisplay(self):
        sql = 'select id, web_cfcjxx from table_subinfo where id not in (select distinct gsbm from table_regdisplays) and web_cfcjxx <>"" union select gsbm, web_cfczxx from table_basic where gsbm not in (select distinct gsbm from table_regdisplays) and web_cfczxx <>"";'
        res =  self.exe_sql_w_return(sql)
        return res      
        
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
   
  
class table_cpainfo(table):
    def __init__(self, db):
        super(table_cpainfo,self).__init__(db,'cpainfo')
        self.fields = ['gsbm',##公司编号
                        'id', 
                        'xm',##姓名
                        'xb', ##性别
                        'csny', ##出生年月
                        'snzw', ##所内职务   
                        'sfdy', ##是否党员
                        'xl', ##学历
                        'xw', ##学位
                        'sxzy', ##所学专业
                        'byxx', ##毕业学校
                        'zgqdfs', ##资格取得方式（考试/考核）
                        'qkhgzsh',##全科合格证书号
                        'qkhgnf',##全科合格年份  
                        'zckjszsbh',##注册会计师证书编号
                        'sfgd', ##是否合伙人（股东）
                        'pzzcwjh',##批准注册文件号
                        'pzzcsj',##批准注册时间
                        'szsws',##所在事务所
                        'bndywcxs',##本年度应完成学时
                        'ywcxs',##本年度已完成学时
                        'web_cfcjxx',
                        'cfcjxx',##处罚/惩戒信息
                        'web_charity',
                        'cjgyhd'##参加公益活动
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_cpainfo(self):
        sql = 'select gsbm, web_xm from table_cpa'
        res =  self.exe_sql_w_return(sql)
        return res   

    def func_update_overseascpa_from_cpainfo(self, data):
        sql = 'select gsbm, zsmc, jwjg, ywmc, qdsj, zsbh, qdsd table_overseascpa where gsbm ='+ data[0]+ ' and zsmc =' + data[1] +' and jwzg=' + data[2]+ ' and ywmc='+ data[3] +' and qdsj=' + data[4] +' and zsbh='+data[5] +' and qdsd ='+ data[6]
        res =  self.exe_sql_w_return(sql)
        return res   
    
class table_cpainfo_otherqualis(table):
    def __init__(self, db):
        super(table_cpainfo_otherqualis,self).__init__(db,'cpainfo_otherqualis')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'qtzg',     ##取得国内其他执业资格名称
                    
                        'qdsj',     ##取得时间
                        'zsbh',     ##证书编号
                        'qdsd'      ##取得地点
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())
  
class table_cpainfo_overseasqualis(table):
    def __init__(self, db):
        super(table_cpainfo_overseasqualis,self).__init__(db,'cpainfo_overseasqualis')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'jwzg',     ##境外资格中文名称
                        
                        'ywmc',     ##英文名称（简称）
                        'qdsj',     ##取得时间
                        'zsbh',     ##证书编号
                        'qdsd'      ##取得地点
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

      
class table_cpainfo_rewards(table):
    def __init__(self, db):
        super(table_cpainfo_rewards,self).__init__(db,'cpainfo_rewards')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'jlzl',     ##奖励种类
                        
                        'jlsj',     ##奖励时间
                        'jlbm',     ##奖励部门
                        'jlyy'     ##奖励原因
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())
    
      
class table_cpainfo_cpaorgan(table):
    def __init__(self, db):
        super(table_cpainfo_cpaorgan,self).__init__(db,'cpainfo_cpaorgan')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'rzxh',     ##任职协会
                        
                        'rzqj',     ##任职期间
                        'lsjc',     ##理事会届次
                        'drzw'      ##具体职务（理事或常务理事
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())
    
      
class table_cpainfo_otherorgan(table):
    def __init__(self, db):
        super(table_cpainfo_otherorgan,self).__init__(db,'cpainfo_otherorgan')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'rzxh',     ##任职协会
                        
                        'rzqj',     ##任职期间
                        'zywyhmc',     ##专业委员会名称
                        'drzw'      ##担任职务
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())
    
      
class table_cpainfo_congress(table):
    def __init__(self, db):
        super(table_cpainfo_congress,self).__init__(db,'cpainfo_congress')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'szrdzx',     ##所在人大/政协
                        
                        'rzqj',     ##任职期间
                        'rdzxjc',     ##人大/政协届次
                        'drzw'      ##担任职务
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    
class table_cpainfo_otherparty(table):
    def __init__(self, db):
        super(table_cpainfo_otherparty,self).__init__(db,'cpainfo_otherparty')
        self.fields = ['gsbm', ##公司编号
                       'cpano',##注册会计师证书编号
                       'id',
                        'zsmc',     ##注师名称
                        'bh',
                        'rzmzdpgsl',     ##任职民主党派/工商联
                        
                        'rzqj',     ##任职期间
                        'jrsj',     ##加入时间
                        'drzw'     ##担任职务
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())




#class table_cpainfo_cpa(table):
#    def __init__(self, db):
#        super(table_cpainfo_cpa,self).__init__(db,'cpainfo_cpa')
#        self.fields = ['gsbm', ##公司编号
#                       'id',
#                        'zsmc',     ##注师名称
#                        'bh',
#                        'rzxh',     ##任职协会
#                        
#                        'rzqj',     ##任职期间
#                        'lshjc',     ##理事会届次
#                        'jtzw'     ##具体职务（理事或常务理事）
#                        ]   ##
#        self.types = ['varchar(2)']*len(self.fields)
#        self.primary_key = ['id']
#        #self.add_foreign_key('gsbm','main','swsbm')
#        self.exe_sql(self.sql_create_table())
#
#    def func_select_cpainfo(self):
#        sql = 'select gsbm, web_xm from table_cpa'
#        res =  self.exe_sql_w_return(sql)
#        return res   
#
#class table_cpainfo_duty(table):
#    def __init__(self, db):
#        super(table_cpainfo_duty,self).__init__(db,'cpainfo_duty')
#        self.fields = ['gsbm', ##公司编号
#                       'cpano',##注册会计师证书编号
#                       'id',
#                        'zsmc',     ##注师名称
#                        'bh',
#                        'rzxh',     ##任职协会
#                        
#                        'rzqj',     ##任职期间
#                        'zywyhmc',     ##专业委员会名称
#                        'drzw'     ##担任职务
#                        ]   ##
#        self.types = ['varchar(2)']*len(self.fields)
#        self.primary_key = ['id']
#        #self.add_foreign_key('gsbm','main','swsbm')
#        self.exe_sql(self.sql_create_table())
#
#    def func_select_cpainfo(self):
#        sql = 'select gsbm, web_xm from table_cpa'
#        res =  self.exe_sql_w_return(sql)
#        return res   





### penalty table is derived from the cpainfo table because cpainfo table will provide the web link.
class table_cpainfo_penalty(table):
    def __init__(self, db):
        super(table_cpainfo_penalty,self).__init__(db,'cpainfo_penalties')
        self.fields = ['gsbm', ##公司编号                       
                        'zsxm', ##注师姓名
                        'zsbh', ##注师编号
                        'id',
                        'bh', ##编号
                        'cfcjsj', ##处罚/惩戒时间
                        'sscfcjbm', ##实施处罚/惩戒的部门
                        'web_cfcjgg', ##
                        'cfcjjl', ##处罚/惩戒种类
                        'cfcjcs', ##处罚/惩戒措施
                        'cfcjwjh' ##处罚/惩戒文件号
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_cpainfo(self):
        sql = 'select gsbm, xm, zckjszsbh, web_cfcjxx from table_cpainfo where web_cfcjxx != ""'
        res =  self.exe_sql_w_return(sql)
        return res  

    ### penalties table has two checks
    ### first, we have to check with the cpainfo which has web link to penalty
    def func_check_penalty_diff_w_cpainfo(self):
        sql ='select zckjszsbh, xm, web_cfcjxx from table_cpainfo where web_cfcjxx <>"" and zckjszsbh not in (select zsbh from table_cpainfo_penalties);'
        res =  self.exe_sql_w_return(sql)
        return res 
    
    ### second, we have to check with the regdisplay table, which is the personal penalty disclosure. but some people may retire or out of the market.
    def func_check_penalty_diff_w_regdisplay(self):
        sql = 'select distinct zsbh from table_regdisplays where zsbh not in (select zsbh from table_cpainfo_penalties);'
        res =  self.exe_sql_w_return(sql)
        return res          
    

### charity table is derived from the cpainfo table because cpainfo table will provide the web link.    
class table_cpainfo_charity(table):
    def __init__(self, db):
        super(table_cpainfo_charity,self).__init__(db,'cpainfo_charity')
        self.fields = ['gsbm', ##公司编号
                       'zsxm', ##注师姓名
                        'zsbh', ##注师编号
                        'id',
                        'bh',   ##序号
                        'gyhdmc',     ##公益活动名称
                        
                        'hdzbdw',     ##活动主办单位
                        'cjhdsj',     ##参加活动时间
                        'cyhdfsjzynr' ##参与活动方式及主要内容
                        ]   ##
        self.types = ['varchar(2)']*len(self.fields)
        self.primary_key = ['id']
        #self.add_foreign_key('gsbm','main','swsbm')
        self.exe_sql(self.sql_create_table())

    def func_select_cpainfo(self):
        sql = 'select gsbm, xm, zckjszsbh, web_charity from table_cpainfo where web_charity != ""'
        res =  self.exe_sql_w_return(sql)
        return res

    ### penalties table has one check
    ### first, we have to check with the cpainfo which has web link to charity
    def func_check_charity_diff_w_cpainfo(self):
        sql ='select zckjszsbh, xm, web_charity from table_cpainfo where web_charity <>"" and zckjszsbh not in (select zsbh from table_cpainfo_charity);'
        res =  self.exe_sql_w_return(sql)
        return res
