import numpy as np
import pandas as pd
import xarray as xr
import datetime
import os
import glob

from read_budget_func import read_global_emis

  

emilist =[ 'emich3cho',
           'emich3cooh',
           'emich3coch3',
           'eminh3',
           'emic6h6',
           'emico',
           'emidms',
           'emic2h6',
           'emic2h4',
           'emic2h2',
           'emihcho',
           'emihcooh',
           'emiisop',
           'emich4',
           'emich3oh',
           'emih2',
           'emimtp',
           'emino',
           'emino2',
           'eminox',
           'eminmvoc',
           'emic3h8',
           'emic3h6',
           'emiso4',
           'emiso2']
  


#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'


experiment_id_list = ['cntr','h2pert','ch4pert']

member_id_list =  {'OsloCTM3v1-2':'r2',
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}

#member_id = 'r1'
#model_list = [ 'GFDL-ESM4-c1'] #'UKESM1-0-LL'] #,'EC-Earth3-AerChem','EMAC-DLR']
#model_list = [ 'LMDZ-INCA'] #'EMAC-DLR'] #'EC-Earth3-AerChem'] #'OsloCTM3v1-2']
#['EC-Earth3-AerChem','EMAC-DLR', 'CESM2-v212','NorESM2-LM-C','LMDZ-INCA','OsloCTM3v1-2']#,  'CESM2-v212']
#model_list = [ 'LMDZ-INCA'] #,'CESM2-v212']
#model_list = ['NorESM2-LM-C'] #'GFDL-ESM4-c1']
model_list =['EMAC-DLR'] #,'NorESM2-LM-C']
#model_list = ['EC-Earth3-AerChem']#,'EMAC-DLR'] #,'UKESM1-0-LL']

#model_list = [ 'OsloCTM3v1-2',  'CESM2-v212']#'UKESM1-0-LL','GFDL-ESM4-c1']

for model_id in model_list:
    for experiment_id in experiment_id_list:
    
        path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
        member_id = member_id_list[model_id]
    
        if model_id =='CESM2-v212':
            area_path = '/nird/home/ragnhibs/hyway/tmp/'
        elif model_id == 'EC-Earth3-AerChem':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id =='EMAC-DLR':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        
        else:
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'
     
    
        for comp in emilist:
            variable_id = comp[3:]
            print(variable_id)


            read_global_emis(variable_id=variable_id,
                             table_id=table_id,
                             experiment_id=experiment_id,
                             project_id=project_id,
                             member_id=member_id,
                             model_id=model_id,
                             path=path,
                             area_path=area_path,
                             molecw=-99)
