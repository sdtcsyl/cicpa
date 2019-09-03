# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 19:53:36 2019

"""


import requester as rq
import database as db


def main_table_staff(date):
    rq_staff = rq.request_staff()
    db_staff = db.table_staff(date)
    
    selections = db_staff.func_select_staff()
    for s in range(0,len(selections)+1,1):
        selection = selections[s]
        if len(selection[1])!=0:
            guid = selection[1].split("'")[1]
            code = selection[1].split("'")[3]
            
            rq_staff.func_request_header(guid, code)
            req = rq_staff.func_post(guid, code, 1)
            data = req.text
            nums, pages, page = rq_staff.func_re_main_nums(data)
            for i in range(1, int(pages)+1,1):
                req = rq_staff.func_post(guid, code, i)
                req_dts = rq_staff.func_re_cpa(req.text)
                for req_dt in req_dts:
                    db_staff.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
               # time.sleep(random.randrange(1,10))
        

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_staff(date)