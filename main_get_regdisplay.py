# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:51:01 2019

@author: e0306210
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 21:36:23 2019

@author: e0306210
"""


import requester as rq
import database as db

def main_table_regdisplay(date):
    db_main = db.table_main(date)
    rq_regdisplay = rq.request_regdisplay()
    db_regdisplay = db.table_regdisplay(date)
    
    selections = db_regdisplay.func_select_regdisplay() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            rq_regdisplay.func_request_header(selection[0])
            req = rq_regdisplay.func_get(selection[0])
            data = req.text
            req_dts = rq_regdisplay.func_re_regdisplay(req.text)
            for req_dt in req_dts:
                db_regdisplay.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            try:
                nums, pages, page = rq_regdisplay.func_re_main_nums(data)
            except ValueError:
                 pages=1
                 nums =0
                 with open("regdisplay.txt", "a+", encoding='utf-8') as text_file:
                     text_file.write(selection[0] + '\n')
            for i in range(2, int(pages)+1,1):
                req = rq_regdisplay.func_post(selection[0], i)
                req_dts = rq_regdisplay.func_re_regdisplay(req.text)
                for req_dt in req_dts:
                    db_regdisplay.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
            db_main.func_update(selection[0],'overseasbranch_NY',nums)

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_regdisplay(date)