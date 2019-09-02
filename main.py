# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 22:26:58 2019
"""

import cicpa
import requester as rq
import database as db
import files as Files
import pandas as pd
from lxml import etree
import time
import random

def main_table_main(date):  
    cicpa_firm = cicpa.cicpa()
    rq_main = rq.request_main()
    db_main = db.table_main(date)
    
    for count in range(1,4,1): #循环4次用于检查是否有遗漏
        for key in cicpa_firm.locations:
            if key != '全部':
                req = rq_main.func_request_main_post(cicpa_firm.locations[key], 1)
                nums, pages, page = rq_main.func_re_main_nums(req.text)
                counts = db_main.func_count_by_sf(key)
                if counts != int(nums):
                    for i in range(1, int(pages)+1,1):
                        req = rq_main.func_request_main_post(cicpa_firm.locations[key], i)
                        req_dts = rq_main.func_re_main(req.text)
                        for req_dt in req_dts:
                            db_main.func_write_table((tuple(req_dt)+(key, i) +(0,)*36))
                        time.sleep(random.randrange(1,10))


def main_table_basic(date):
    rq_basic = rq.request_basic()
    db_main = db.table_main(date)
    db_basic = db.table_basic(date)    
    db_qualifications = db.table_qualifications(date)
    db_overseascpa = db.table_overseascpa(date)
    db_subsidiaries = db.table_subsidiaries(date)
    db_subinfo = db.table_subinfo(date)
    
    selections = db_main.func_select_swsbm_web()
    #selections.reverse()
    for selection in selections:
        guid = selection[1].split("'")[1]
        code = selection[1].split("'")[3]
        req = rq_basic.func_get(guid, code)
        data = req.text
        if '分所编号' in data:
            sub_info, data = rq_basic.func_parse_sub(data)
            db_subinfo.func_write_table((selection[0],)+sub_info)
        else:
            info, data = rq_basic.func_parse_basic_p_basic(data)
            db_basic.func_write_table(info)
            
            infos, data = rq_basic.func_parse_basic_p_subsidiaries(data)
            for ifo in infos:
                db_subsidiaries.func_write_table((selection[0],selection[0]+'_'+ifo[0],)+ifo)
            db_main.func_update(selection[0],'no_subsidiaries',len(infos))
            
            infos, data = rq_basic.func_parse_basic_p_qualifications(data)
            for ifo in infos:
                db_qualifications.func_write_table((selection[0],selection[0]+'_'+ifo[0],)+ifo)
            db_main.func_update(selection[0],'no_qualifications',len(infos))
    
            infos, data = rq_basic.func_parse_basic_p_overseascpa(data)
            for ifo in infos:
                db_overseascpa.func_write_table((selection[0],selection[0]+'_'+ifo[0],)+ifo)
            db_main.func_update(selection[0],'no_overseasCPA',len(infos))
        if len(data)  > 30:
            with open(selection[0]+".txt", "w", encoding='utf-8') as text_file:
                text_file.write(data)
            
#    output = db.sqloutput('bjkjssws')
#    output_excel = pd.DataFrame(output,columns = ['No', 'Web', 'Name', 'Address', 'Contact', 'Tel', 'Page', 'NY'])
#    output_excel.to_excel(Files.db_path + 'bjkjssws.xlsx',index=False)
        
if __name__ =='__main__' :
    date = '20190829'
    main_table_basic(date)
    