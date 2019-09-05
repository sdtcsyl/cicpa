# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:44:42 2019

"""


import requester as rq
import database as db


def main_table_cpa(date):
    rq_cpa = rq.request_cpa()
    db_cpa = db.table_cpa(date)
    
    selections = db_cpa.func_select_cpa_from_basic() + db_cpa.func_select_cpa_from_subinfo()
    for s in range(8649,len(selections),1):
        selection = selections[s]
        if len(selection[1])!=0:
            guid = selection[1].split("\'")[1]
            code = selection[1].split("\'")[3]
            
            rq_cpa.func_request_header(guid, code)
            req = rq_cpa.func_post(guid, code, 1)
            data = req.text
            try:
                nums, pages, page = rq_cpa.func_re_main_nums(data)
                for i in range(1, int(pages)+1,1):
                    req = rq_cpa.func_post(guid, code, i)
                    req_dts = rq_cpa.func_re_cpa(req.text)
                    for req_dt in req_dts:
                        db_cpa.func_write_table((selection[0], selection[0] + '_' + req_dt[0],) + req_dt)
               # time.sleep(random.randrange(1,10))
            except ValueError:
                 pass
       
if __name__ =='__main__' :
    date = '20190829'
    main_table_cpa(date)
    