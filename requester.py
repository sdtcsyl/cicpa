# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 20:28:26 2019
"""
from functools import wraps
import time
import requests
import re
import execjs
from lxml import etree
import subprocess


def exe_cmd(cmd):
    '''cmd can be list'''
    result = subprocess.run(cmd, stdout=subprocess.PIPE)    
    return result.stdout.decode('utf-8')


def ipv4_addr():
    result = exe_cmd('ipconfig')
    ipv4 = re.findall(r'IPv4 Address[^\d]*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', result, re.S)
    return ipv4
    

def func_check_error(func):
        @wraps(func)         
        def deco(*args, **kwargs):
            check = True
            while check:
                req = func(*args, **kwargs)
                dt = re.findall(r'error_flag', req.text, re.S)
                if len(dt) == 0:
                    check = False 
                else:
                    time.sleep(600)
            return req
        return deco

  

class cls_request:
    def __init__(self):
        self.url = 'http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
        self.baseurl = 'http://cmispub.cicpa.org.cn/'
        self.header = ''
        self.cookie = ''
        self.data = ''        
    
    @func_check_error    
    def func_request_post(self, url, header, cookie, data, encode = 'utf-8'):
            try:
                req = requests.post(url, headers = header, cookies = cookie, data = data, timeout = 300)
                req.encoding= encode 
            except requests.ConnectionError:    #if the internet is not steable
                        internet = True
                        while internet:
                            try:
                               time.sleep(600) #retry after timeout
                               req = requests.post(url, headers = header, cookies = cookie, data = data, timeout = 300)
                               req.encoding= encode
                            except requests.ConnectionError:    #if the internet is not steable
                                pass
                            else:
                                internet =False
                        return req
            
    @func_check_error    
    def func_request_get(self, url, encode = 'utf-8'):

            try:
                req = requests.get(url, timeout = 300)
                req.encoding= encode
                return req
            except requests.ConnectionError:    #if the internet is not steable
                        internet = True
                        while internet:
                            try:
                               time.sleep(600) #retry after timeout
                               req = requests.get(url, timeout = 300)
                               req.encoding= encode
                            except requests.ConnectionError:    #if the internet is not steable
                                pass
                            else:
                                internet =False
                        return req
      
        
'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''

    
class request_main(cls_request): 
    
    def __init__(self):
        super(request_main,self).__init__()     
        
        self.cookie = {
        'cookiee':'20111116',
        'JSESSIONID': '849A9A1D4DF6D59846E8E407C35FA5B8'
        }   #please amend

        self.header = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language' : 'en-US, en; q=0.8, zh-Hans-CN; q=0.7, zh-Hans; q=0.5, zh-Hant-HK; q=0.3, zh-Hant; q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',       
        'Content-Length' : '114',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Host': 'cmispub.cicpa.org.cn',
        'Referer': 'http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }   
    
    def func_request_main_post(self, scope, pagenum):
        data = self.func_request_main_data(scope, pagenum)        
        req = self.func_request_post(self.url, self.header, self.cookie, data, 'gb2312')
        return req
        
    
    def func_request_main_data(self, scope, pagenum):
        data = {        
           'ascGuid' : scope,   
           'isStock' : '00',
           'method' : 'indexQuery',   
           'offAllcode' : None,        
           'offName' : None,   
           'pageNum' : str(pagenum),
           'pageSize' : None, 
           'personNum' : None, 
           'queryType' : '1'
                }
        return data
        
    def func_re_main_nums(self, data):
        dt = re.findall(r'<div id="leftctrl">([^<]*)</div>', data, re.S)
        dt = re.findall(r'([\d]+)', dt[0], re.S)
        return tuple(dt)
                 
    def func_re_main(self, data):
        dt = re.findall(r'<td[^>]*>([^<]*)</td>[\n\s]*<td[^>]*><a\shref="([^"]*)">([^<]*)</a></td>[\n\s]*<[^>]*>([^<]*)</td>[\n\s]*<[^>]*>([^<]*)</td>[\n\s]*<[^>]*>([^<]*)</td>', data, re.S)
        return dt



'''///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////
   ///////////////////////////////////////////////////////////////////'''
    
class request_basic(cls_request):
    def __init__(self):
        super(request_basic, self).__init__()
        self.viewDetail = """
                //获取事务所详细信息
                function viewDetail(guid,code){
            	    //guid=guid+","+code;
            	   
            		var url = "";
            		if('1'=='1' || '1'=='4'){
            			guid=guid+","+code;
            			if(code!=null&&code.length>8)
            				url = "/cicpa2_web/002/"+guid+"/1.shtml";
            			else
            				url = "/cicpa2_web/002/"+guid+"/7.shtml";
            		}else if('1'=='2'){
            			url = "/cicpa2_web/003/"+guid+".shtml";   							
            		}else{
            			url = "/cicpa2_web/004/"+guid+".shtml";
            		}
                    return url;
            	}
                """
        self.cxt = execjs.compile(self.viewDetail)
    
    def func_get(self, guid, code):
        url = self.baseurl + self.cxt.call("viewDetail", guid, code)
        #print(url)
        req = self.func_request_get(url, 'gb2312')
        return req
    
    def func_parse_basic_p_basic(self, data):
        data = data.replace('\n','')
        data = data.replace('\t','')   
        data = data.replace(' ','')
        
        ### 去掉备注内容
        #data1 = re.sub('<--[^--]*-->',r'',data,re.S)
        
        #### 去掉 html head
        data1 = re.sub('<scripttype="text/javascript">.*EXCEL"id=\'export\'/></td></tr></table>',r'',data,re.S) #去头
        
        ### 去掉 html tail
        data2 = re.sub('</table></td></tr></tbody></table></td></tr><TR><TDbackground=.*</script>',r'',data1,re.S)  #去尾
        
        ### basic info && 去掉 html basic info 
        data3 = re.findall(r'<tableclass="detail_table"[^>]*id="detailtb"><tr><td[^>]*>[^<]*</td></tr><tr><td[^>]*>基本信息</td></tr><tr><td[^>]*>会计师事务所名称</td><td[^>]*>([^<]*)</td><td[^>]*>证书编号</td><td[^>]*>([^<]*)</td></tr><tr><tdclass="tdl">联系人</td><td[^>]*>([^<]*)</td><tdclass="tdl">联系电话</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">办公地址</td><td[^>]*>([^<]*)</td><tdclass="tdl">传真</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">通讯地址</td><td[^>]*>([^<]*)</td><tdclass="tdl">邮政编码</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">电子邮箱</td><td[^>]*>([^<]*)</td><tdclass="tdl">网址</td><tdclass="data_tb_content">([^<]*)</td></tr>',data2,re.S)  #基本信息
        data2 = re.sub(r'''<tableclass="detail_table"[^>]*id="detailtb"><tr><td[^>]*>[^<]*</td></tr><tr><td[^>]*>基本信息</td></tr><tr><td[^>]*>会计师事务所名称</td><td[^>]*>([^<]*)</td><td[^>]*>证书编号</td><td[^>]*>([^<]*)</td></tr><tr><tdclass="tdl">联系人</td><td[^>]*>([^<]*)</td><tdclass="tdl">联系电话</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">办公地址</td><td[^>]*>([^<]*)</td><tdclass="tdl">传真</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">通讯地址</td><td[^>]*>([^<]*)</td><tdclass="tdl">邮政编码</td><tdclass="data_tb_content">([^<]*)</td></tr><tr><tdclass="tdl">电子邮箱</td><td[^>]*>([^<]*)</td><tdclass="tdl">网址</td><tdclass="data_tb_content">([^<]*)</td></tr>''',r'',data2,re.S)  #去基本信息        
        data3 = list(data3[0])
        data3.extend(['']*(10-len(data3)))
        
        ### register info && 去掉 html register info 
        data4 = re.findall(r'<tr><tdclass="table_header"[^>]*>登记信息</td></tr><tr><td[^>]*>批准设立机关</td><td[^>]*>([^<]*)</td><td[^>]*>批准设立文件号</td><td[^>]*>([^<]*)</td><td[^>]*>批准设立时间</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>法定代表人&nbsp;<br>（或执行合伙人）</td><td[^>]*>([^<]*)</td><td[^>]*>出资额或注册资本&nbsp;<br>（万元）</td><td[^>]*>([^<]*)</td><td[^>]*>组织形式&nbsp;<br>（有限/合伙）</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>主任会计师</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所数量</td><td[^>]*>([^<]*)</td><td[^>]*>合伙人或股东人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*></td><td[^>]*></td></tr><tr><td[^>]*>注册会计师人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?<td[^>]*>从业人员人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><tdclass[^>]*></td><td[^>]*></td></tr><tr><td[^>]*>注册会计师人数&nbsp;<br>（含分所）</td><td[^>]*>([^<]*)</td><td[^>]*>从业人员人数&nbsp;<br>（含分所）</td><td[^>]*>([^<]*)</td>',data2,re.S)  #登记信息
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>登记信息</td></tr><tr><td[^>]*>批准设立机关</td><td[^>]*>([^<]*)</td><td[^>]*>批准设立文件号</td><td[^>]*>([^<]*)</td><td[^>]*>批准设立时间</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>法定代表人&nbsp;<br>（或执行合伙人）</td><td[^>]*>([^<]*)</td><td[^>]*>出资额或注册资本&nbsp;<br>（万元）</td><td[^>]*>([^<]*)</td><td[^>]*>组织形式&nbsp;<br>（有限/合伙）</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>主任会计师</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所数量</td><td[^>]*>([^<]*)</td><td[^>]*>合伙人或股东人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*></td><td[^>]*></td></tr><tr><td[^>]*>注册会计师人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?<td[^>]*>从业人员人数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><tdclass[^>]*></td><td[^>]*></td></tr><tr><td[^>]*>注册会计师人数&nbsp;<br>（含分所）</td><td[^>]*>([^<]*)</td><td[^>]*>从业人员人数&nbsp;<br>（含分所）</td><td[^>]*>([^<]*)</td>',r'',data2,re.S)  #去登记信息 
        data4 = list(data4[0])
        data4 = data4[0:10]+data4[11:13]+data4[14:16]+data4[17:19]
        data4.extend(['']*(16-len(data4)))
        
        ### age info && 去掉 html age info 
        data5 = re.findall(r'<tdclass="tdl"[^>]*></td><tdclass="data_tb_content"[^>]*></td></tr><tr><td[^>]*>注册会计师年龄结构</td></tr><tr><td[^>]*>大于70岁人数</td><td[^>]*>([^<]*)</td><td[^>]*>小于等于70岁且大于60岁人数</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>小于等于60岁且大于40岁人数</td><td[^>]*>([^<]*)</td><td[^>]*>小于等于40岁人数</td><td[^>]*>([^<]*)</td></tr>',data2,re.S)  #登记信息 
        data2 = re.sub(r'<tdclass="tdl"[^>]*></td><tdclass="data_tb_content"[^>]*></td></tr><tr><td[^>]*>注册会计师年龄结构</td></tr><tr><td[^>]*>大于70岁人数</td><td[^>]*>([^<]*)</td><td[^>]*>小于等于70岁且大于60岁人数</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>小于等于60岁且大于40岁人数</td><td[^>]*>([^<]*)</td><td[^>]*>小于等于40岁人数</td><td[^>]*>([^<]*)</td></tr>',r'',data2,re.S)  #去登记信息 
        try:
            data5 = list(data5[0])    
        except IndexError:
            pass
        data5.extend(['']*(4-len(data5)))
        
        ### degree info && 去掉 html degree info 
        data6 = re.findall(r'<tr><tdclass="table_header"[^>]*>注册会计师学历结构</td></tr><tr><td[^>]*>博士研究生人数</td><td[^>]*>([^<]*)</td><td[^>]*>硕士研究生人数</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>本科人数</td><td[^>]*>([^<]*)</td><td[^>]*>大专及以下人数</td><td[^>]*>([^<]*)</td></tr>',data2,re.S)  #登记信息 
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>注册会计师学历结构</td></tr><tr><td[^>]*>博士研究生人数</td><td[^>]*>([^<]*)</td><td[^>]*>硕士研究生人数</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>本科人数</td><td[^>]*>([^<]*)</td><td[^>]*>大专及以下人数</td><td[^>]*>([^<]*)</td></tr>',r'',data2,re.S)  #去登记信息 
        try:
            data6 = list(data6[0])
        except IndexError:
            pass
        data6.extend(['']*(4-len(data6)))        
        
        ### qualification info && 去掉 html qualification info 
        data7 = re.findall(r'<tr><tdclass="table_header"[^>]*>执行业务信息</td></tr><tr><td[^>]*>是否取得证券、期货相关业务许可证</td><td[^>]*>([^<]*)</td><td[^>]*>取得证券、期货相关业务许可证时间</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>资格证书号</td><td[^>]*>([^<]*)</td><td[^>]*></td><td[^>]*></td></tr><[^>]*>',data2,re.S)  #登记信息 
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>执行业务信息</td></tr><tr><td[^>]*>是否取得证券、期货相关业务许可证</td><td[^>]*>([^<]*)</td><td[^>]*>取得证券、期货相关业务许可证时间</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>资格证书号</td><td[^>]*>([^<]*)</td><td[^>]*></td><td[^>]*></td></tr><[^>]*>',r'',data2,re.S)  #去登记信息 
        try:
            data7 = list(data7[0])
        except IndexError:
            pass
        data7.extend(['']*(3-len(data7)))
        
        ### net info && 去掉 html net info 
        data8 = re.findall(r'<tr><tdclass="table_header"[^>]*>执业网络信息</td></tr><tr><td[^>]*>加入国际网络</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>境外分支机构</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr>',data2,re.S)  #登记信息 
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>执业网络信息</td></tr><tr><td[^>]*>加入国际网络</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>境外分支机构</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr>',r'',data2,re.S)  #去登记信息 
        try:
            data8 = list(data8[0])
            data8 = data8[0:2]+data8[3:5]
        except IndexError:
            pass
        data8.extend(['']*(4-len(data8)))
        
        ### comprehensive info && 去掉 html comprehensive info 
        data9 = re.findall(r'<tr><tdclass="table_header"[^>]*>综合信息</td></tr><tr><td[^>]*>是否具有内部培训资格</td><td[^>]*>([^<]*)</td><td[^>]*>继续教育完成率\（上一年度\）</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>处罚/惩戒信息\(披露时限:自2016年至今\)</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>被检查信息</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr><tr><td[^>]*>参与公益活动</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*></td><td[^>]*></td></tr><tbody[^>]*>',data2,re.S)
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>综合信息</td></tr><tr><td[^>]*>是否具有内部培训资格</td><td[^>]*>([^<]*)</td><td[^>]*>继续教育完成率\（上一年度\）</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>处罚/惩戒信息\(披露时限:自2016年至今\)</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>被检查信息</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr><tr><td[^>]*>参与公益活动</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*></td><td[^>]*></td></tr><tbody[^>]*>',r'',data2,re.S)  #去登记信息 
        try:
            data9 = list(data9[0])
            data9 = data9[0:4] + data9[5:7] + data9[8:10]
        except IndexError:
            pass
        data9.extend(['']*(8-len(data9)))
        
        data10 = re.findall(r'<!--<tr><td[^>]*>执行业务信息</td></tr><tr><td[^>]*>客户信息</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><tdclass="tdl"[^>]*></td><td[^>]*></td></tr>-->',data2,re.S)
        data2 = re.sub(r'<!--<tr><td[^>]*>执行业务信息</td></tr><tr><td[^>]*>客户信息</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><tdclass="tdl"[^>]*></td><td[^>]*></td></tr>-->',r'',data2,re.S) 
        try:
            data10 = list(data10[0])
            data10 = data10[0:2]
        except IndexError:
            pass
        data10.extend(['']*(2-len(data10)))
        
        return tuple(data3+data4+data5+data6+data7+data8+data9+data10), data2
        
    def func_parse_basic_p_subsidiaries(self, data2):
        ### 分所信息
        data2 = re.sub(r'<tr><tdclass="table_header"[^>]*>设立分所情况</td></tr><tr><td[^>]*><table[^>]*><tr[^>]*><td[^>]*>序号</td><td[^>]*>分所名称</td><td[^>]*>分所负责人</td><td[^>]*>电话</td><td[^>]*>电子邮箱</td></tr>',r'',data2,re.S)  #去分所表表头
        
        data10 = re.findall(r'<tr><td[^>]*>([^<]*)</td><td[^>]*><ahref=([^>]*)>([^<]*)</a></td><td[^>]*>([^<]*)</td><td>([^<]*)</td><td[^>]*>([^<]*)</td></tr>',data2,re.S)  #登记信息 
        
        data2 = re.sub(r'<tr><td[^>]*>([^<]*)</td><td[^>]*><ahref=([^>]*)>([^<]*)</a></td><td[^>]*>([^<]*)</td><td>([^<]*)</td><td[^>]*>([^<]*)</td></tr>',r'',data2,re.S)  #去登记信息 
        data2 = re.sub(r'<tr><td[^>]*>([^<]*)</td><td[^>]*><ahref=([^>]*)>([^<]*)</a></td><td[^>]*>([^<]*)</td><td>([^<]*)</td><td[^>]*>([^<]*)</td></tr>',r'',data2,re.S)  #去登记信息 
        
        return  data10, data2

    def func_parse_basic_p_qualifications(self, data2):     
        ### 其他职业资格
        data2 = re.sub(r'</table></td></tr></tbody><tbody[^>]*><tr><td[^>]*>取得其他执业资质</td></tr><tr><td[^>]*><tableclass="detail_table"[^>]*><tr[^>]*><td[^>]*>序号</td><td[^>]*>取得的其他执业资质名称</td><td[^>]*>资格取得时间</td><td[^>]*>批准机关</td></tr>',r'',data2,re.S)  #去分所表表头
        
        data11 = re.findall(r'<tr><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td></tr>',data2,re.S)  #登记信息 
        
        data2 = re.sub(r'<tr><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td><td[^>]*>([^>]*)</td></tr>',r'',data2,re.S)  #去登记信息 
        
        return  data11, data2
     
    def func_parse_basic_p_overseascpa(self, data2):
        ### 海外职业资格
        data2 = re.sub(r'</table></td></tr></tbody><tbody[^>]*><tr><td[^>]*>取得境外资格注册会计师情况</td></tr><tr><td[^>]*><tableclass="detail_table"[^>]*><tr[^>]*><td[^>]*>序号</td><td[^>]*>注师名称</td><td[^>]*>境外资格中文名称</td><td[^>]*>英文名称（简称）</td><td[^>]*>取得时间</td><td[^>]*>证书编号</td><td[^>]*>取得地点</td></tr>',r'',data2,re.S)  #去分所表表头
        
        data12 = re.findall(r'<tr><td[^>]*>([^>]*)</td><td><ahref=([^>]*)>([^>]*)</a></td><td>([^>]*)</td><td>([^>]*)</td><td[^>]*>([^>]*)</td><td>([^>]*)</td><td>([^>]*)</td></tr>',data2,re.S)  #登记信息 
        
        data2 = re.sub(r'<tr><td[^>]*>([^>]*)</td><td><ahref=([^>]*)>([^>]*)</a></td><td>([^>]*)</td><td>([^>]*)</td><td[^>]*>([^>]*)</td><td>([^>]*)</td><td>([^>]*)</td></tr>',r'',data2,re.S)  #去登记信息 

        return  data12, data2    
        
    def func_parse_sub(self, data):
        data = data.replace('\n','')
        data = data.replace('\t','')
        data = data.replace(' ','')
        
        #### 去掉 html head
        data1 = re.sub('<scripttype="text/javascript">.*EXCEL"id=\'export\'/></td></tr></table>',r'',data,re.S) #去头
        
        ### 去掉 html tail
        data2 = re.sub('<!--中部表格结束--></td></tr><TR><TDbackground=.*</script>',r'',data1,re.S)  #去尾
        
        
        ### basic info && 去掉 html basic info 
        data3 = re.findall(r'<table[^>]*><tr><td[^>]*>[^<]*</td></tr><tr><td[^>]*>分所名称</td><td[^>]*>([^<]*)</td><td[^>]*>主所证书编号</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所编号</td><td[^>]*>([^<]*)</td><td[^>]*>所在城市</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>邮政编码</td><td[^>]*>([^<]*)</td><td[^>]*>电子邮箱</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>传真</td><td[^>]*>([^<]*)</td><td[^>]*>联系电话</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>成立批准时间</td><td[^>]*>([^<]*)</td><td[^>]*>成立批准文号</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>成立批准机关</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所负责人</td><td[^>]*>([^<]*)</td><td[^>]*>网址</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>注册会计师总数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>从业人员总数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr><![^>]*><tr><td[^>]*>处罚/惩戒信息\(披露时限:自2016年至今\)</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr><[^>]*><tr><td[^>]*>办公地址</td><td[^>]*>([^<]*)</td></tr></table></td></tr></TABLE>',data2,re.S)  #基本信息
        data2 = re.sub(r'<table[^>]*><tr><td[^>]*>[^<]*</td></tr><tr><td[^>]*>分所名称</td><td[^>]*>([^<]*)</td><td[^>]*>主所证书编号</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所编号</td><td[^>]*>([^<]*)</td><td[^>]*>所在城市</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>邮政编码</td><td[^>]*>([^<]*)</td><td[^>]*>电子邮箱</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>传真</td><td[^>]*>([^<]*)</td><td[^>]*>联系电话</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>成立批准时间</td><td[^>]*>([^<]*)</td><td[^>]*>成立批准文号</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>成立批准机关</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>分所负责人</td><td[^>]*>([^<]*)</td><td[^>]*>网址</td><td[^>]*>([^<]*)</td></tr><tr><td[^>]*>注册会计师总数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td><td[^>]*>从业人员总数</td><td[^>]*>(<ahref=[^>]*>)?([^<]*)(</a>)?</td></tr><![^>]*><tr><td[^>]*>处罚/惩戒信息\(披露时限:自2016年至今\)</td><td[^>]*>([^<]*)</td></tr><[^>]*><tr><td[^>]*>办公地址</td><td[^>]*>([^<]*)</td></tr></table></td></tr></TABLE>',r'',data2,re.S)  #去基本信息        
        data3 = list(data3[0])
        data3 = data3[0:13] +data3[14:15]+ data3[17:18] +data3[20:21]+ data3[22:23]+data3[13:14]+ data3[16:17]+data3[19:20]
#        data3.extend(['']*(10-len(data3)))
#        
#        
#        dom = etree.HTML(data)
#        description = dom.xpath("//table[@id = 'detailtb']//td[@class='data_tb_content']//text()")
#        for i in range(len(description)):
#            description[i] = description[i].replace(' ','')
#                
#        description = description[0:13] + description[14:15] + description[17:18]+ description[19:21]
#        webs = re.findall('onclick=([^>]*)>',data, re.S)
#        description = description+webs[1:3]
        return tuple(data3), data2
        
        

        
        #branch = dom.xpath("//table[@id = 'detailtb']/tbody/tr/td/table//tr//text()")
        #branch_link = dom.xpath("//table[@id = 'detailtb']/tbody/tr/td/table//a//text()")