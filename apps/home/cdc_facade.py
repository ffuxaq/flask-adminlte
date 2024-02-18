import app.report.report_last_month as rlm

def getLastInfo(period_start,period_end,retursql):
    return rlm.get_info_last(period_start,period_end,retursql)
    
