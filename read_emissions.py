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


#experiment_id_list = ['cntr','h2pert','ch4pert']
#experiment_id_list = ['nhh2pert','shh2pert','avih2pert','shiph2pert']
experiment_id_list = ['cntr1850','h2antr1850']



member_id_list =  {'OsloCTM3v1-2':'r2',
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}

model_list = ['OsloCTM3v1-2',
              'NorESM2-LM-C',
              'EC-Earth3-AerChem',
              'EMAC-DLR',
              'LMDZ-INCA',
              'CESM2-v212',
              'GFDL-ESM4-c1',
              'UKESM1-0-LL']
    
for model_id in model_list:
    for experiment_id in experiment_id_list:
    
        path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
        member_id = member_id_list[model_id]

        if (experiment_id == 'cntr1850' or experiment_id == 'h2antr1850'):
            member_id = 'r1'

            
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
