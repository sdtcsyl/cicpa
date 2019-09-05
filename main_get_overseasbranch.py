# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:24:07 2019

@author: e0306210
"""


import requester as rq
import database as db

def main_table_overseasbranch(date):
    db_main = db.table_main(date)
    rq_overseasbranch = rq.request_overseasbranch()
    db_overseasbranch = db.table_overseasbranch(date)
    
    selections = db_overseasbranch.func_select_overseasbranch() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            guid = selection[1].split("\'")[1]
            code = selection[1].split("\'")[3]
            
            rq_overseasbranch.func_request_header(guid, code)
            req = rq_overseasbranch.func_get(guid, code)
            data = req.text
            req_dts = rq_overseasbranch.func_re_overseasbranch(req.text)
            for req_dt in req_dts:
                db_overseasbranch.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            try:
                nums, pages, page = rq_overseasbranch.func_re_main_nums(data)
            except ValueError:
                 pages=1
                 nums =0
                 with open("overseasbranch.txt", "a+", encoding='utf-8') as text_file:
                     text_file.write(selection[0] + '\n')
            for i in range(2, int(pages)+1,1):
                req = rq_overseasbranch.func_post(guid, code, i)
                req_dts = rq_overseasbranch.func_re_overseasbranch(req.text)
                for req_dt in req_dts:
                    db_overseasbranch.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            db_main.func_update(selection[0],'no_overseasbranch',nums)

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_overseasbranch(date)