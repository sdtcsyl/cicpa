# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 14:18:17 2019
"""

import requester as rq
import database as db
import files as fl

def main_table_cpainfo(date):
    db_main = db.table_main(date)
    rq_cpainfo = rq.request_cpainfo()
    db_cpainfo = db.table_cpainfo(date)
    
    db_cpainfo_otherqualis = db.table_cpainfo_otherqualis(date)
    db_cpainfo_overseasqualis = db.table_cpainfo_overseasqualis(date)
    db_cpainfo_rewards = db.table_cpainfo_rewards(date)
    db_cpainfo_cpaorgan = db.table_cpainfo_cpaorgan(date)
    db_cpainfo_otherorgan = db.table_cpainfo_otherorgan(date)
    db_cpainfo_congress = db.table_cpainfo_congress(date)
    db_cpainfo_otherparty = db.table_cpainfo_otherparty(date)
    
    selections = db_cpainfo.func_select_cpainfo() 
    for s in range(90000,len(selections),1):
        selection = selections[s]
        guid = selection[1].split("'")[1]
        code = selection[1].split("'")[3]
        req = rq_cpainfo.func_get(guid, code)
        data = req.text

        req_dt, data = rq_cpainfo.func_parse_cpa_basic(data)
        db_cpainfo.func_write_table((selection[0], selection[0] + '_' + req_dt[0]+ '_' + req_dt[12],) + req_dt)
        
        infos, data = rq_cpainfo.func_parse_cpa_otherqualis(data)
        for info in infos:
            db_cpainfo_otherqualis.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'no_subinfo',len(infos))

        infos, data = rq_cpainfo.func_parse_cpa_overseasqualis(data)
        for info in infos:
            db_cpainfo_overseasqualis.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'pages_subinfo',len(infos))

        infos, data = rq_cpainfo.func_parse_cpa_rewards(data)
        for info in infos:
            db_cpainfo_rewards.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'subinfo_NY',len(infos))  
        
        infos, data = rq_cpainfo.func_parse_cpa_cpaorgan(data)
        for info in infos:
            db_cpainfo_cpaorgan.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'cpainfo',len(infos))

        infos, data = rq_cpainfo.func_parse_cpa_otherorgan(data)
        for info in infos:
            db_cpainfo_otherorgan.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'pages_cpainfo',len(infos))

        infos, data = rq_cpainfo.func_parse_cpa_congress(data)
        for info in infos:
            db_cpainfo_congress.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'cpainfo_NY',len(infos))          
        
        infos, data = rq_cpainfo.func_parse_cpa_otherparty(data)
        for info in infos:
            db_cpainfo_otherparty.func_write_table((selection[0], req_dt[12],  selection[0]+'_'+req_dt[12]+'_'+info[0],code,)+info)
        db_main.func_update(selection[0],'no_overseasbranch',len(infos))  
        
        
        if len(data)  > 2200:
            with open(fl.html_path  + req_dt[12] +".txt", "w", encoding='utf-8') as text_file:
                text_file.write(data)
        

def main_table_cpainfo_penalty(date):
    rq_cpainfo_penalty = rq.request_cpainfo_penalty()
    db_cpainfo_penalty = db.table_cpainfo_penalty(date)
    
    selections = db_cpainfo_penalty.func_select_cpainfo() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        guid = selection[3].split("'")[1]
        code = selection[3].split("'")[3]
        req = rq_cpainfo_penalty.func_get(guid, code)
        data = req.text
        
        req_dt = rq_cpainfo_penalty.func_re(data)
        for dt in req_dt:
            db_cpainfo_penalty.func_write_table((selection[0], selection[1], selection[2],  selection[2]+ '_' + dt[0],) + dt)
    
    selections = db_cpainfo_penalty.func_check_penalty_diff_w_cpainfo() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        guid = selection[2].split("'")[1]
        code = selection[2].split("'")[3]
        req = rq_cpainfo_penalty.func_get(guid, code)
        data = req.text
        
        req_dt = rq_cpainfo_penalty.func_re(data)
        for dt in req_dt:
            db_cpainfo_penalty.func_write_table((selection[0], selection[1], selection[2],  selection[2]+ '_' + dt[0],) + dt)
    


def main_table_cpainfo_charity(date):
    rq_cpainfo_charity = rq.request_cpainfo_charity()
    db_cpainfo_charity = db.table_cpainfo_charity(date)
    
    selections = db_cpainfo_charity.func_select_cpainfo() 
    for s in range(0,len(selections),1):
        selection = selections[s]
        guid = selection[3].split("'")[1]
        code = selection[3].split("'")[3]
        req = rq_cpainfo_charity.func_get(guid, code)
        data = req.text
        
        req_dt = rq_cpainfo_charity.func_re(data)
        for dt in req_dt:
            db_cpainfo_charity.func_write_table((selection[0], selection[1], selection[2],  selection[2]+ '_' + dt[0],) + dt)          
       
if __name__ =='__main__' :
    date = '20190829'
    #main_table_cpainfo(date)
