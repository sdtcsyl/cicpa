# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 14:18:17 2019
"""

import requester as rq
import database as db

def main_table_cpainfo(date):
    db_main = db.table_main(date)
    rq_cpainfo = rq.request_cpainfo()
    db_cpainfo = db.table_cpainfo(date)
    db_cpainfo_overseas = db.table_cpainfo_overseas(date)
    
    selections = db_cpainfo.func_select_cpainfo() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        guid = selection[1].split("'")[1]
        code = selection[1].split("'")[3]
        req = rq_cpainfo.func_get(guid, code)
        data = req.text

        req_dt, data = rq_cpainfo.func_parse_cpa_basic(data)
        db_cpainfo.func_write_table((selection[0], selection[0] + '_' + req_dt[0]+ '_' + req_dt[12],) + req_dt)
        
        infos = rq_cpainfo.func_parse_cpa_other(data)
        for info in infos:
            db_cpainfo_overseas.func_write_table((selection[0],selection[0]+'_'+code+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'no_subinfo',len(infos))
        

       
if __name__ =='__main__' :
    date = '20190829'
    main_table_cpainfo(date)