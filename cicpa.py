# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 11:18:00 2019
"""


import time
import requests
import re


class cicpa:
    def __init__(self):        
        ##from website
        
        self.locations = {
        '全部':'00',
        '北京注协':'0000010F84968440E06B4F9F27A6E22A',
        '天津注协':'0000010F8496847E921E7F6839F85C62',
        '河北注协':'0000010F8496849E8E6BBCA9192A3EE8',
        '山西注协':'0000010F8496849E3184E81F08BA9F91',
        '内蒙注协':'0000010F849684AD1BF4D260B666FB01',
        '辽宁注协':'0000010F849684BDDDBD3B87E41FCB5B',
        '吉林注协':'0000010F849684CDF10E8E024ADDA4ED',
        '黑龙江注协':'0000010F849684CDEABEFD04BA7F02F1',
        '上海注协':'0000010F849684DCEB0DA1CE842044D0',
        '江苏注协':'0000010F849684EC5D56C3DF1C737DC9',
        '浙江注协':'0000010F849684ECDCA54437FA1C85F9',
        '安徽注协':'0000010F8496850B7171A5A6C127C7E0',
        '福建注协':'0000010F8496851B06D99CE3A3F1C9A7',
        '江西注协':'0000010F8496852A162E0BFA034067CE',
        '山东注协':'0000010F8496853AA3B101B05B58B16C',
        '河南注协':'0000010F8496854A6DBDB31B5F4396C9',
        '湖北注协':'0000010F8496854A60CCB457629ED137',
        '湖南注协':'0000010F849685594D162AE0F99EDFF7',
        '广东注协':'0000010F84968569DDB2CD9ADD2CAA43',
        '广西注协':'0000010F84968578C1770CF71536D3C0',
        '海南注协':'0000010F849685882E06678254A10DDF',
        '深圳注协':'0000010F8496859888BBD1029F822843',
        '重庆注协':'0000010F849685A75D7956DC32768653',
        '四川注协':'0000010F849685A79478F6A3A445F571',
        '贵州注协':'0000010F849685B7E59BF926493B78F7',
        '云南注协':'0000010F849685C78CF5BB6ED7C7D9D2',
        '西藏注协':'0000010F849685D63874E1EC4B5EFFD0',
        '陕西注协':'0000010F849685E649EBE2BD0DAA4450',
        '甘肃注协':'0000010F849685F53BEA66FF5283D10C',
        '青海注协':'0000010F849685F55C170C78C1453015',
        '宁夏注协':'0000010F84968605C5017216586DA0F2',
        '新疆注协':'0000010F84968615879EA828919DFBF1'
        }
                
                
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

        self.getPartner = """
        	//获取股东列表
        	function getPartner(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swsgd/"+title+"/"+offGuid+".html";
        	}"""
            
        self.getPersons = """
        	//注师列表
        	function getPersons(offGuid,title){
        		title = " ";
        		return "/cicpa2_web/public/query/swszs/"+title+"/"+offGuid+".html";
        	}"""
            
        self.getNwPers = """
        	//从业人员
        	function getNwPers(offGuid,title){
        		title = " ";
        		return "/cicpa2_web/public/query/swscyry/"+title+"/"+offGuid+".html";
        	}"""
    
        self.getChkedInfo = """
        	//被检查信息
        	function getChkedInfo(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swsbjc/"+title+"/"+offGuid+".html";
        	}"""
    
        self.getZykhInfo = """
        	//主要客户
        	function getZykhInfo(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swszykh/"+title+"/"+offGuid+".html";
        	}"""
    
        self.getGjwlInfo = """
            //国际网络
        	function getGjwlInfo(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swszywl/"+title+"/"+offGuid+".html";
        	}"""
            
        self.getJwjgInfo = """    
        	//境外机构
        	function getJwjgInfo(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swsjwjg/"+title+"/"+offGuid+".html";
        	}"""

        self.getCjcfInfo = """     
        	//惩戒处罚
        	function getCjcfInfo(offGuid,title,code){
        		title = encodeURI(title);
        		//offGuid=offGuid+"_"+code;
        		
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swscjcf/"+title+"/"+offGuid+"/"+code+".html";
        	}"""

        self.getGyhdInfo = """     
        	//公益活动
        	function getGyhdInfo(offGuid,title){
        		title = encodeURI(title);
        		var re = /%/g;
        		title = title.replace(re,"-");
        		return "/cicpa2_web/public/query/swsgyhd/"+title+"/"+offGuid+".html";
        	}"""
    
        self.getSubOffice = """
            //分所
        	function getSubOffice(offGuid,offType){
        		return "/cicpa2_web/public/query/subsws/1/"+offGuid+".html";
        	}"""
        
        self.getSubOffice = """
        	//注师详细信息
        	function getPerDetails(perGuid,perName){
        		perName = encodeURI(perName);
        		var re = /%/g;
        		perName = perName.replace(re,"-");
        		url = "/cicpa2_web/public/query/sws/p/"+perGuid+".html";
        		return url;
        	}"""
            
        self.exportExcel = """
        //主要要进行的操作是计算行高和列宽，只需要计算最外层table的列宽即可 
        //如果有嵌套的情况(嵌套表格的行高以内部表格为标准，列宽则以第一个表格为标准) 
        function exportExcel(tableid) {//整个表格拷贝到EXCEL中   
        	//检索浏览器  
        	if(navigator.userAgent.indexOf("MSIE")<0){  
        	    alert('请用ie浏览器进行表格导出');  
        	    return;  
        	}
        	var curTbl = document.getElementById(tableid);   
        	var oExcelApp = null;   
        	//创建Excel应用程序对象oExcelApp
        	try {  
        	    oExcelApp = GetObject("", "Excel.Application");  
        	}  
        	catch (E) {  
        	    try {  
        	        oExcelApp = new ActiveXObject("Excel.Application");  
        	    }  
        	    catch (E2) {  
        	        alert("请确认已经执行了如下操作:\n1.您的电脑已经安装Microsoft Excel软件！。\n2.浏览器中Internet选项=>安全=>自定义级别中已经设置\"允许运行ActiveX控件\"。");  
        	        return;  
        	    }  
        	}
        	
        	//新增excel工作簿   
        	var oExcelBook = oExcelApp.Workbooks.Add();   
        	 //获取workbook对象   
        	var oSheet = oExcelBook.ActiveSheet;   
        	      
        	//在此进行样式控制 
        	var letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];
        	var trows = curTbl.rows;
        	    
        	//判断第一个表格行内是否有嵌套表格，如果有则以第一个嵌套表格为标准(目前只处理最外层表格只有一个单元格的情况)
        	if(trows.length > 0 && trows[0].cells.length >0){
        		if(trows[0].cells[0].firstChild.nodeName=='TABLE' && trows[0].cells.length!=1){
        			alert('导出表格不符合规范，暂时无法处理！');
        			return;
        		}
        		if(trows[0].cells[0].firstChild.nodeName=='TABLE'){
        			var innerTab = trows[0].cells[0].firstChild;
        			var inRows = innerTab.rows;
        			var maxCellsIndex = 0;
        			var maxColLength = 0;
        			//设置第一个内部表格行高
        			for(var i=0;i<inRows.length;i++){
        				var cells = inRows[i].cells;
        				if(cells.length > maxColLength){
        					maxColLength = cells.length;
        					maxCellsIndex = i;
        				} 
        				oSheet.Rows((i+1)+":"+(i+1)).RowHeight=roundFloat(inRows[i].clientHeight*3/4,2);
        			}			
        			//设置列宽
        			var maxCells = inRows[maxCellsIndex].cells;
        			for(var j=0;j<maxCells.length;j++){
        				oSheet.Columns(letters[j]+":"+letters[j]).ColumnWidth = roundFloat((maxCells[j].clientWidth/80)*10,2);
        			}
        			//设置其它表格行高
        		}
        		else{
        			var maxCellsIndex = 0;
        			var maxColLength = 0;
        			//设置行高
        			for(var i=0;i<trows.length;i++){
        				var cells = trows[i].cells;
        				if(cells.length > maxColLength){
        					maxColLength = cells.length;
        					maxCellsIndex = i;
        				} 
        				oSheet.Rows((i+1)+":"+(i+1)).RowHeight=roundFloat(trows[i].clientHeight*3/4,2);
        			}
        			//设置列宽
        			var maxCells = trows[maxCellsIndex].cells;
        			for(var j=0;j<maxCells.length;j++){
        				oSheet.Columns(letters[j]+":"+letters[j]).ColumnWidth = roundFloat((maxCells[j].clientWidth/80)*10,2);
        			}			
        		}
        	}
        	oSheet.Rows(1).HorizontalAlignment=3;     
        	
        	var sel = document.body.createTextRange(); //激活当前sheet   
        	sel.moveToElementText(curTbl); //把表格中的内容移到TextRange中  
        	//sel.select();  //全选TextRange中内容   
        	sel.execCommand("Copy"); //复制TextRange中内容   
        	oSheet.Paste(); //粘贴到活动的EXCEL中   
        	oExcelApp.Visible = true; //设置excel可见属性  
        	  
        	oSheet.Application.Quit(); //结束当前进程  
        	
        	window.opener=null;  
        	window.close(); //关闭当前窗口
        }   
        /*************************************导出结束********************************************/"""
	    
        ##configure based upon users
        self.url = 'http://cmispub.cicpa.org.cn/cicpa2_web/OfficeIndexAction.do'
        self.baseurl = 'http://cmispub.cicpa.org.cn/'
        
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

        ## main table
        

