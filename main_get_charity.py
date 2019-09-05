# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:27:06 2019

"""

import requester as rq
import database as db

def main_table_charity(date):
    db_main = db.table_main(date)
    rq_charity = rq.request_charity()
    db_charity = db.table_charity(date)
    
    selections = db_charity.func_select_charity() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            guid = selection[1].split("\'")[1]
            code = selection[1].split("\'")[3]
            
            rq_charity.func_request_header(guid, code)
            req = rq_charity.func_get(guid, code)
            data = req.text
            req_dts = rq_charity.func_re_charity(req.text)
            for req_dt in req_dts:
                db_charity.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            try:
                nums, pages, page = rq_charity.func_re_main_nums(data)
            except ValueError:
                 pages=1
                 nums =0
                 with open("Charity.txt", "a+", encoding='utf-8') as text_file:
                     text_file.write(selection[0] + '\n')
            for i in range(2, int(pages)+1,1):
                req = rq_charity.func_post(guid, code, i)
                req_dts = rq_charity.func_re_charity(req.text)
                for req_dt in req_dts:
                    db_charity.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            db_main.func_update(selection[0],'no_charity',nums)

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_charity(date)
    