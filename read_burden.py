import numpy as np
import pandas as pd
import xarray as xr
import datetime
import os
import glob

from read_budget_func import read_global_burden


#Read burden from a range of components. Check if file exist.

#Need to have the molecular weight.
molecw_list = {'h2':2.016,
               'ch3oh':32.032,
               'ch4':16.042,
               'hcho':30.026,
               'h2o':28.01,
               'co':28.01,
               'o3':48.0,
               'ch3cho': 44.052,
               'ch3cooh': 60.052,
               'ch3coch3': 58.080,
               'nh3': 17.031,
               'c6h6': 78.111,
               'dms': 62.134,
               'c2h6': 30.070,
               'c2h4': 28.054,
               'c2h2': 26.038,
               'hcooh': 46.025,
               'chocho': 60.052,
               'oh': 17.007,
               'isop': 68.100,
               'ch4': 16.042,
               'mhp': 78.111,
               'mtp': 60.052,
               'hno3': 63.012,
               'no2': 46.0055,
               'no': 30.0061,
               'pan': 60.052,
               'c3h8': 44.095,
               'c3h6': 42.079,
               'so2': 64.066}

#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'




experiment_id_list = ['cntr','h2pert','ch4pert']

member_id_list =  {'OsloCTM3v1-2':'r2',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r1',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}


model_list = ['GFDL-ESM4-c1'] #'CESM2-v212'] #'OsloCTM3v1-2' ] #UKESM1-0-LL','GFDL-ESM4-c1']

for experiment_id in experiment_id_list:
    for model_id in model_list:
        member_id = member_id_list[model_id]
        path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
        
        if model_id =='EC-Earth3-AerChem':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id == 'EMAC-DLR':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'
        else:
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'

        for variable_id in molecw_list:
            molecw = molecw_list[variable_id]
            read_global_burden(variable_id=variable_id,
                               table_id=table_id,
                               experiment_id=experiment_id,
                               project_id=project_id,
                               member_id=member_id,
                               model_id=model_id,
                               path=path,
                               area_path=area_path,
                               molecw=molecw)
