# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:26:58 2019
"""

import requests 
import time
import re
import database as db
import files as Files
import pandas as pd

class cicpa:
    def __init__(self):        
        self.url = 'http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
        
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


def func_data(scope, pagenum):
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

def func_request_data(url, header, cookie, data):
    try:
        req = requests.post(url, headers = header, cookies = cookie, data = data, timeout = 300)
    except requests.ConnectionError:    #if the internet is not steable
                internet = True
                while internet:
                    try:
                       time.sleep(600) #retry after timeout
                       req = requests.get(url, headers = header, cookies = cookie, data = data, timeout = 300)
                    except requests.ConnectionError:    #if the internet is not steable
                        pass
                    else:
                        internet =False
    finally:
            return req
def func_re(data):
    dt = re.findall(r'<td[^>]*>([^<]*)</td>[\n\s]*<td[^>]*><a\shref="([^"]*)">([^<]*)</a></td>[\n\s]*<[^>]*>([^<]*)</td>[\n\s]*<[^>]*>([^<]*)</td>[\n\s]*<[^>]*>([^<]*)</td>', data, re.S)
    return dt

def func_viewDetail():
    js = '''function viewDetail(guid,code){
	    //guid=guid+","+code;
	   
		var url = "";
		if('1'=='1' || '1'=='4'){
			guid=guid+","+code;
			if(code!=null&&code.length>8)
				url = "/cicpa2_web/002/"+guid+"/1.shtml";
			else
				url = "/cicpa2_web/002/"+guid+"/7.shtml";
				
			window.open(url);
		}else if('1'=='2'){
			url = "/cicpa2_web/003/"+guid+".shtml";
							
			
			window.open(url);
		}else{
			url = "/cicpa2_web/004/"+guid+".shtml";
							
			
			window.open(url);
		}
	}  '''
    
    url = 'http://cmispub.cicpa.org.cn/'
        
def main():
    cicpa_firm = cicpa()
    qg = '0000010F84968440E06B4F9F27A6E22A'
    for i in range(1,48,1):
        data = func_data(qg, i)
        req = func_request_data(cicpa_firm.url, cicpa_firm.header, cicpa_firm.cookie, data)
        #save_shtml(page, req.text)
        req_dts = func_re(req.text)
        for req_dt in req_dts:
            db.sqlwrite(tuple(req_dt)+(i,0),'bjkjssws')
        #time.sleep(30)
        
    output = db.sqloutput('bjkjssws')
    output_excel = pd.DataFrame(output,columns = ['No', 'Web', 'Name', 'Address', 'Contact', 'Tel', 'Page', 'NY'])
    output_excel.to_excel(Files.db_path + 'bjkjssws.xlsx',index=False)
        
if __name__ =='__main__' :
    main()