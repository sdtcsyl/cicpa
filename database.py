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



#### start
dtb = database('20190829')


            
def sqlwrite(data, table):    
    conn = sqlite3.connect(Files.db_path + 'db.db')
    cursor = conn.cursor()
    cursor.execute(sql_create_table(table))
    try:

        if table == 'CPA':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           xm,
                           rybh,
                           
                           xb,
                           csrq,
                           qkhgzh
                           ) 
                           values (?,?,?,?,?,  ?,?,?)''', 
                           (data))
        if table == 'CPA_info':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           xm,
                           xb,
                           snzw,
                           sfdy,
                           
                           sjyxx,                       
                           xl,
                           xw,
                           sxzy,
                           byxx,
                           
                           zgqdfs,
                           qkhgsh,
                           qkhgnf,
                           zckjszsbh,
                           sfhhr,
                           
                           pzzcwjh,                           
                           pzzcsj,
                           szsws,
                           bndywcxs,
                           cfcjxx, 
                           
                           bndywcxs,                           
                           cjgyhd,                           
                           jwzgzwmc,
                           ywmc,
                           qdsj,
                           
                           zsbh,                           
                           qddd
                           ) 
                           values (?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?,  ?,?)''', 
                           (data))
        if table == 'overseas':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           jrsj,
                           gjkjgsmc,
                           zbzcd,
                           dz,
                           
                           dh,                       
                           cz,
                           fzr,
                           dzyj,
                           wz
                           ) 
                           values (?,?,?,?,?,  ?,?,?,?,?)''', 
                           (data))
        if table == 'overseas branch':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           fzjgmc,
                           slsj,
                           
                           szcs,                       
                           fzr,
                           ygrs
                           ) 
                           values (?,?,?,?,?,  ?,?,?)''', 
                           (data))
        if table == 'charities':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           gyhdgmc,
                           hdzbdw,
                           
                           cjhdsj,                       
                           cyhdfsjzyhd
                           ) 
                           values (?,?,?,?,?,  ?,?)''', 
                           (data))

        if table == 'check':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           jcxh,
                           jsjcnd
                           ) 
                           values (?,?,?,?,?)''', 
                           (data))    
        if table == 'staff':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           xm,
                           xb,
                           
                           jssj,                       
                           sfqht,
                           sfcjsb,
                           sfdy
                           ) 
                           values (?,?,?,?,?,  ?,?,?,?)''', 
                           (data))    
        if table == 'partners':
            cursor.execute('''insert into table_''' + 
                           table + 
                           '''( 
                           gsbm,
                           id,
                           bh,
                           hhr,
                           zfzs,
                           
                           zsbg
                           ) 
                           values (?,?,?,?,?,  ?)''', 
                           (data)) 
    except sqlite3.IntegrityError:
        pass
    cursor.rowcount
    cursor.close()
    conn.commit()
    conn.close()

        
def sqlselect(table, **args):    
    conn = sqlite3.connect(Files.db_path + 'db.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists table_''' + 
                       table + 
                       '''(
                       id varchar(5),
                       secCode varchar(5),
                       secName varchar(5),
                       orgId varchar(5),
                       announcementId varchar(5),
                       announcementTitle varchar(5),
                       timestampStr varchar(5),
                       adjunctUrl varchar(5)  primary key,
                       adjunctSize varchar(5),
                       adjunctType varchar(5),
                       announcementType varchar(5),
                       announcementTypeName varchar(5),
                       associateAnnouncement varchar(5),
                       batchNum varchar(5),
                       columnId varchar(5),
                       sid varchar(5),
                       important varchar(5),
                       orgName varchar(5),
                       pageColumn varchar(5),
                       storageTime varchar(5),
                       page varchar(2),
                       NY varchar(2)
                       )''') 
    
    if 'alldata' in args:
        cursor.execute('SELECT id  FROM table_' + table)  
    else:   
        cursor.execute('SELECT id, adjunctUrl, adjunctType FROM table_' + table + ' WHERE NY = 0') 
    res =cursor.fetchall()
    suc = res
    cursor.close()
    conn.commit()
    conn.close() 
    return suc
    

def sqlupdate(count, dl, table, record):    
    conn = sqlite3.connect(Files.db_path + 'db.db')
    cursor = conn.cursor()     
    cursor.execute('UPDATE table_' + table + ' SET NY = ?  WHERE id = ?',(count, dl,)) 
    cursor.close()
    conn.commit()
    conn.close() 

def sqlcheck(table, **kws):
    conn = sqlite3.connect(Files.db_path + 'db.db')
    cursor = conn.cursor()
    cursor.execute('''create table if not exists table_''' + 
                           table + 
                           '''(
                           id varchar(5),
                           secCode varchar(5),
                           secName varchar(5),
                           orgId varchar(5),
                           announcementId varchar(5),
                           announcementTitle varchar(5),
                           timestampStr varchar(5),
                           adjunctUrl varchar(5)  primary key,
                           adjunctSize varchar(5),
                           adjunctType varchar(5),
                           announcementType varchar(5),
                           announcementTypeName varchar(5),
                           associateAnnouncement varchar(5),
                           batchNum varchar(5),
                           columnId varchar(5),
                           sid varchar(5),
                           important varchar(5),
                           orgName varchar(5),
                           pageColumn varchar(5),
                           storageTime varchar(5),
                           page varchar(2),
                           NY varchar(2)
                           )''') 
    if 'filename' in kws:
        cursor.execute('SELECT id FROM table_' + table + ' WHERE id = ?',(kws['filename'],))
    if 'fileweb' in kws:
        cursor.execute('SELECT adjunctUrl FROM table_' + table + ' WHERE adjunctUrl = ?',(kws['fileweb'],))
    res =cursor.fetchall()
    suc = 0
    if len(res) > 0:
        suc = 1
    else:
        suc = 0 
    cursor.close()
    conn.commit()
    conn.close() 
    return suc

def sqloutput(table):
    conn = sqlite3.connect(Files.db_path + 'db.db')
    cursor = conn.cursor()
    cursor.execute('select swsbm, web, swsmc, txdz, lxr, lxdh, page, NY from table_'+table)
    res =cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return res
    