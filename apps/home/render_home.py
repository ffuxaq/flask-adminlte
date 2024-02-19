# 2023 ffuxaq cdc
from flask import render_template, request
import  app_cdc.flask_adminlte.apps.home.cdc_facade as facade
from app_cdc.config import Config
import app_cdc.help_functions as hf
import os
from sqlite3 import Row as sqliteRow

    
def render_index1(template,segment):
    #prendiamo l'ultimo periodo in funzione dell'ultimo caricamento dati effttuato.
    results = facade.getLastInfo("01/12/2023","31/12/2023",False)
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
    
    result_peso_materie = dict()
    
    
    #calcoliamo le sentenze totali enll'ultimo mese)
    return render_template("home/" + template, segment=segment,results = results,countProvv = countProvv, countSent = countSent, countProvvTot = countProvvTot,numeroGiudici = numeroGiudici,period_start=data_mese_precedente,period_end=last_date_import_ita, conf=config_app )

def render_index4(template,segment):
    #prendiamo l'ultimo periodo in funzione dell'ultimo caricamento dati effttuato.
    results = facade.getIscrittiPesoMateriePeriodi("31/12/2023",False)
    config  = Config()
    config_app = hf.readYamlFile(os.path.join(config.APP_PATH,'config_app.yaml'))
    
    #calcoliamo i provvedimenti totali nell'ultimo mese
    countProvv = 0
    countSent  = 0
    countProvvTot = 0

    dictMateria = {"materia":"","totmat":0}
    dictMacro  = {"macromateria":"","totmacro":0,"materie":[]}
    dictPeriodo = {"periodo":"","totper":0,"macromaterie":[]}
    dictAll = {"periodi":[]}
    
    memoMacro = "" # memoria la macromateria
    memoPeriodo = ""  # memorizza il periodo
    periodo = ""
    macro = ""
    materia = ""
    totperiodo = 0
    totmacro = 0    
   
    for res in results:
        if isinstance(res,sqliteRow): 
            periodo = res['periodo']
            macro = res['dm']
            materia = res['materia']
            
            dictMateriaNew = dict(dictMateria)
            dictMateriaNew["materia"] = materia
            dictMateriaNew["totmat"] = int(res['cnt'])
            
            if periodo != memoPeriodo:                
                dictPeriodoNew = dict(dictPeriodo)
                dictAll["periodi"].append(dictPeriodoNew)
                totperiodo = 0
                dictPeriodoNew["periodo"] = res["periodo"]
            else :
                pass
            
            totperiodo= totperiodo + int(res['cnt'])
        
            if macro != memoMacro:
                dictMacroNew = dict(dictMacro)
                dictPeriodoNew["macromaterie"].append(dictMacroNew)  
                dictMacroNew["macromateria"] = res["dm"]
                totmacro = 0
            else :
                pass
            
            totmacro = totmacro + int(res['cnt'])
            
            dictMacroNew["totmacro"] = totmacro
            dictMacroNew["materie"].append(dictMateriaNew)            
            
            
            dictPeriodoNew["totper"] = totperiodo
                    
            
            memoMacro = macro # memoria la macromateria
            memoPeriodo = periodo  # memorizza il periodo
            
        #print(res['materia'] )
        # if "sentenze" in  (str(res[65])).lower():
        #     print(res)
        #     countSent = countSent + int(res[64])
        # else:
        #     countProvv = countProvv + int(res[64])
         
    print (dictAll)    
    countProvvTot = countProvv + countSent
    
    result_peso_materie = dict()
    
    
    #calcoliamo le sentenze totali enll'ultimo mese)
    return render_template("home/" + template, segment=segment,results = results,countProvv = countProvv, countSent = countSent, countProvvTot = countProvvTot, conf=config_app )
