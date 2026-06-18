import numpy as np
import pandas as pd
import xarray as xr
import datetime


from read_budget_func import *

#Calculate global budget values from hyway simulations.

#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'

#experiment_id_list = ['cntr','h2pert','ch4pert']

#experiment_id_list = ['cntr1850','h2antr1850',
experiment_id_list =  ['nhh2pert','shh2pert','avih2pert','shiph2pert']


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


molecw_list = {#'ch3oh':32.032,
               #'c2h6':30.068,
               'h2':2.016 ,
               'ch4':16.042,
               'hcho':30.026,
               'h2o':18.015,
               'co':28.01}#,
               #'o3':48.0,
               #'mhp':48.042}
    
#molecw_list = {'ch4':16.042}




for variable_id in molecw_list:
    molecw = molecw_list[variable_id]

    for model_id in model_list:
        member_id = member_id_list[model_id]

        

        for experiment_id in experiment_id_list:
            
            if (experiment_id == 'cntr1850' or experiment_id == 'h2antr1850'):
                member_id = 'r1'
            
            path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
            if model_id =='CESM2-v212':
                area_path = '/nird/home/ragnhibs/hyway/tmp/'
            elif model_id =='EMAC-DLR':
                area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
            elif model_id == 'EC-Earth3-AerChem':
                area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
            else:
                area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'
            
    
                
            read_global_surfconc(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            #burden is read for a different file
            #read_global_burden(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            read_global_atmprod(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            read_global_atmloss(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            


            read_global_photoloss(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            read_global_soilsink(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            
            read_global_wetdep(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
            #emission is read from a different file
            #read_global_emis(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path)
        
    
