# 2023 ffuxaq cdc
from flask import render_template, request
from app_cdc.flask_adminlte.apps.home.cdc_facade import getLastInfo
from app_cdc.config import Config
import app_cdc.help_functions as hf
import os

def render(template,segment):
    #prendiamo l'ultimo periodo in funzione dell'ultimo caricamento dati effttuato.
    results = getLastInfo("01/12/2023","31/12/2023",False)
    config  = Config()
    config_app = hf.readYamlFile(os.path.join(config.APP_PATH,'config_app.yaml'))
    test2 = hf.readYamlFile()
    
    last_date_import_ame = config_app['last_global_import']
    last_date_import_ita = hf.getDateItasStrFromAmeNoSepa(last_date_import_ame)
    data_mese_precedente = hf.getFineMesePrecedente(last_date_import_ita,1)
    #calcoliamo i provvedimenti totali nell'ultimo mese
    countProvv = 0
    countSent  = 0
    countProvvTot = 0
    listDistinctGiudici = []
    for res in results:
        if "sentenze" in  (str(res[65])).lower():
            countSent = countSent + int(res[64])
        else:
            countProvv = countProvv + int(res[64])
        
        if str(res[0]) not in listDistinctGiudici:
            listDistinctGiudici.append(str(res[0]))
    
    numeroGiudici = len(listDistinctGiudici)              
    countProvvTot = countProvv + countSent
    
    #calcoliamo le sentenze totali enll'ultimo mese)
    return render_template("home/" + template, segment=segment,results = results,countProvv = countProvv, countSent = countSent, countProvvTot = countProvvTot,numeroGiudici = numeroGiudici,period_start=data_mese_precedente,period_end=last_date_import_ita, conf=config_app )