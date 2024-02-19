import app_cdc.report.report_last_month as rlm
import app_cdc.report.report_last_year as rly

def getLastInfo(period_start,period_end,retursql,**kwargs):
    return rlm.get_info_last(period_start,period_end,retursql)


def getIscrittiPesoMateriePeriodi(period_start,retursql,**kwargs):
    return rly.get_iscritti_peso_materie_periodi(period_start,retursql)
