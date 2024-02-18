# 2023 ffuxaq cdc
from flask import render_template, request
from app.flask_adminlte.apps.home.cdc_facade import getLastInfo 

def render(template,segment):
    results = getLastInfo("01/12/2023","31/12/2023",False)
    
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
    return render_template("home/" + template, segment=segment,results = results,countProvv = countProvv, countSent = countSent, countProvvTot = countProvvTot,numeroGiudici = numeroGiudici )