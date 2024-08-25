# 2024 FFUXAQ CDC
from flask import render_template, request
import app_cdc.flask_adminlte.apps.home.cdc_facade as facade
from app_cdc.config import Config
import app_cdc.help_functions as hf
import os
from sqlite3 import Row as sqliteRow
import pprint

    
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
        if "sentenze" in  (str(res[63])).lower():
            countSent = countSent + int(res[63])
        else:
            countProvv = countProvv + int(res[63])
        
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
    
    """
    Di seguito calcoliamo i totali per periodo e il totale dei 4 periodi
    anche se non ci servirà a nulla

    """   
        
    contaTotPeriodi = {"totale":0,"periodi":[]}
    mdlTotPeriodo = {"periodo:":"","tot":0}   # mpdello dict per inserire il conto dei totali per periodo
    
    periodo = ""
    cnt = 0
    for res in results:
        if isinstance(res,sqliteRow): 
            if res['periodo'] != periodo :
                mdlTotPeriodNew = dict(mdlTotPeriodo)
                mdlTotPeriodNew["periodo"] = res["periodo"]                
                contaTotPeriodi["periodi"].append(mdlTotPeriodNew)
                cnt = 0
                
            periodo = res['periodo']
            cnt = res['cnt'] + cnt
            mdlTotPeriodNew["tot"] = cnt
            contaTotPeriodi["totale"] = res['cnt'] + contaTotPeriodi["totale"]
     
     
    """
    Di seguito calcoliamo i totali macromateria e per materia,
    associamo tutte le materie con la stessa macromateria ad un dict macromaterie 
    e le macromaterie con lo stesso periodo al periodo e quindi visti i totali del periodo
    ci andiamo a calcolare i pesi

    """   
       
    dictMateria = {"materia":"","totmat":0,"pesomat":0.0}
    dictMacro  = {"macromateria":"","totmacro":0,"pesomacro":0.0,"numeroMacroMaterie":0,"materie":[]}
    dictPeriodo = {"periodo":"","totper":0,"macromaterie":[]}
    dictAll = {"periodi":[]}
    
    memoMacro = "" # memoria la macromateria
    memoPeriodo = ""  # memorizza il periodo
    periodo = ""
    macro = ""
    materia = ""
    totperiodo = 0
    totmacro = 0 
    CountMacroMat = 0
    MemoTotCalcolatiPeriodo = 0 
    
    contcycle = 0
    for res in results:
        if isinstance(res,sqliteRow): 
            periodo = res['periodo']
            macro = res['dm']
            materia = res['materia']
                        
            if periodo != memoPeriodo:
                totCalcolatiPeriodo = getTotPerPeriod(contaTotPeriodi,periodo)
                #cloniamo ma dobbiamo azzerare la lista di macromaterie
                #altrimenti il riferimento ci rimane sempre lo stesso               
                dictPeriodoNew = dictPeriodo.copy()
                dictPeriodoNew["macromaterie"] = list()
                dictAll["periodi"].append(dictPeriodoNew)
                totperiodo = 0
                dictPeriodoNew["periodo"] = res["periodo"]
            else :
                pass            
            
            dictMateriaNew = dictMateria.copy()
            dictMateriaNew["materia"] = materia
            dictMateriaNew["totmat"] = int(res['cnt'])
            dictMateriaNew['pesomat']= percTwoDec(float(int(res['cnt'])/int(totCalcolatiPeriodo)))
            
            totperiodo= totperiodo + int(res['cnt'])

            
            if macro != memoMacro:
                ## prima dell'assegnazione dle cambio verifichiamo se dictMacroNew esiste
                if ('dictMacroNew' in locals()):
                    dictMacroNew["pesomacro"] = percTwoDec(float( int(totmacro)/int(MemoTotCalcolatiPeriodo)))
                    dictMacroNew["numeroMacroMaterie"] = CountMacroMat
                
                CountMacroMat = 0
                #dopo l'assegnazione del cambio
                #cloniamo ma dobbiamo azzerare la lista di materie
                #altrimenti il riferimento ci rimane sempre lo stesso
                dictMacroNew = dictMacro.copy()
                dictMacroNew["materie"] = list()
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
            memoPeriodo = periodo  # memorizza il
            CountMacroMat = CountMacroMat +1
            MemoTotCalcolatiPeriodo = totCalcolatiPeriodo
            contcycle = contcycle +1
    
    #per come è gestito dobbliamo aggiunger all'ultimo l'ultimo peso macromateria      
    dictMacroNew["pesomacro"] = percTwoDec(float( int(totmacro)/int(totCalcolatiPeriodo/CountMacroMat)))
    dictMacroNew["numeroMacroMaterie"] = CountMacroMat
         
    #print (dictAll)  
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dictAll)
    
    semestrale =dictAll["periodi"][0]
    annuale =dictAll["periodi"][1]
    biennale =dictAll["periodi"][2]
    quadriennale =dictAll["periodi"][3]

    return render_template("home/" + template, segment=segment,semestrale =semestrale, annuale=annuale,biennale=biennale,quadriennale=quadriennale,conf=config_app )

def getTotPerPeriod(listOfDict,period):
        # iterate over the list
    for value in listOfDict["periodi"]:        
        if value["periodo"] == period:
            return value["tot"]
    return 0

def percTwoDec(num):
    """
        Percentuale con 2 cifre decimali
    """
    return round(num * 100,2)