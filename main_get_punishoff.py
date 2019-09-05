# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:36:23 2019

@author: e0306210
"""


import requester as rq
import database as db

def main_table_punishoff(date):
    db_main = db.table_main(date)
    rq_punishoff = rq.request_punishoff()
    db_punishoff = db.table_punishoff(date)
    
    selections = db_punishoff.func_select_punishoff() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            
            rq_punishoff.func_request_header(selection[0])
            req = rq_punishoff.func_get(selection[0])
            data = req.text
            req_dts = rq_punishoff.func_re_punishoff(req.text)
            for req_dt in req_dts:
                db_punishoff.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            try:
                nums, pages, page = rq_punishoff.func_re_main_nums(data)
            except ValueError:
                 pages=1
                 nums =0
                 with open("punishoff.txt", "a+", encoding='utf-8') as text_file:
                     text_file.write(selection[0] + '\n')
            for i in range(2, int(pages)+1,1):
                req = rq_punishoff.func_post(selection[0], i)
                req_dts = rq_punishoff.func_re_punishoff(req.text)
                for req_dt in req_dts:
                    db_punishoff.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            db_main.func_update(selection[0],'pages_overseasbrach',nums)

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_punishoff(date)