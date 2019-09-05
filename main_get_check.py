# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:15:16 2019

@author: e0306210
"""

import requester as rq
import database as db

def main_table_check(date):
    db_main = db.table_main(date)
    rq_check = rq.request_check()
    db_check = db.table_check(date)
    
    selections = db_check.func_select_check() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            guid = selection[1].split("\'")[1]
            code = selection[1].split("\'")[3]
            
            rq_check.func_request_header(guid, code)
            req = rq_check.func_get(guid, code)
            data = req.text
            req_dts = rq_check.func_re_check(req.text)
            for req_dt in req_dts:
                db_check.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            try:
                nums, pages, page = rq_check.func_re_main_nums(data)
            except ValueError:
                 pages=1
                 nums =0
                 with open("check.txt", "a+", encoding='utf-8') as text_file:
                     text_file.write(selection[0] + '\n')
            for i in range(2, int(pages)+1,1):
                req = rq_check.func_post(guid, code, i)
                req_dts = rq_check.func_re_check(req.text)
                for req_dt in req_dts:
                    db_check.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            db_main.func_update(selection[0],'no_check',nums)

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_check(date)
    