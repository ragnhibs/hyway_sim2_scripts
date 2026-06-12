import numpy as np
import pandas as pd
import xarray as xr
import datetime
import os
import glob

from read_budget_func import read_global_burden_aerosols

#Read burden from a range of components. Check if file exist.
variable_id_list = ['oa','so4','no3fine']

#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'

member_id = 'r1'

experiment_id_list = ['cntr','h2pert','ch4pert']





model_list = ['LMDZ-INCA',
              'EC-Earth3-AerChem',
              'EMAC-DLR',
              'NorESM2-LM-C',
              'LMDZ-INCA',
              'OsloCTM3v1-2',
              'CESM2-v212']

model_list =['EMAC-DLR','NorESM2-LM-C'] #'GFDL-ESM4-c1']



member_id_list =  {'OsloCTM3v1-2':'r2',
                   'EC-Earth3-AerChem':'r1',
                   'NorESM2-LM-C':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}


for experiment_id in experiment_id_list:
    for model_id in model_list:
        
        path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
        
        if model_id =='EC-Earth3-AerChem':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id == 'EMAC-DLR':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'
        else:
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'
            
        member_id = member_id_list[model_id]

        for variable_id in variable_id_list:
            
            read_global_burden_aerosols(variable_id=variable_id,
                                        table_id=table_id,
                                        experiment_id=experiment_id,
                                        project_id=project_id,
                                        member_id=member_id,
                                        model_id=model_id,
                                        path=path,
                                        area_path=area_path)
          
