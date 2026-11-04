import numpy as np
import pandas as pd
import xarray as xr
import datetime
import os
import glob


def read_global_vertdist(variable_id,table_id,experiment_id,project_id,member_id,model_id,path,area_path):

    time_range='*'
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)

    full_path = path + filename

    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return
    
    model_data = xr.open_mfdataset(full_path)

    if model_id == 'CESM2-v212':
        file_area = 'areacella_'+model_id+'_'+project_id +'_transient2010s_'+member_id +'.nc'
        area = xr.open_dataset(area_path + file_area)
        area = area.isel(time=0).drop_vars('time')
        area['lat'] = model_data['lat']
    else:
        file_area = 'areacella_fixed_'+model_id+'_'+project_id + '.nc'
        area_full_path = area_path + file_area
        if not glob.glob(area_full_path):
            return
        
        area = xr.open_dataset(area_full_path)
        

   

    #Calculate area weighted global mean.
    weighted_field = model_data[variable_id].weighted(area['areacella'])
    globalmean = weighted_field.mean(dim=['lat', 'lon'])

    globalmean.to_netcdf('results_netcdf_vertical/monthly_vertical_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
    

    df = globalmean.to_dataframe(name=model_id +'_' +member_id)

    #if model_id == 'GFDL-ESM4-c1':
    #   df.index = add_2000yr(df.index)

    print(df)

    #Maybe write as netcdf?
    #df.to_csv('results_csv/monthly_surfconc_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')



#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'

complist = ['h2','ch4','o3','h2o','oh']

experiment_id_list = ['freech4h2pert','freech4cntr']
#experiment_id_list = ['ch4pert','cntr','h2pert','cntrch4'] #'ch4pert']
#experiment_id_list = ['h2pert','ch4pert']
#experiment_id_list = ['cntr1850','h2antr1850'] #,'nhh2pert','shh2pert','avih2pert','shiph2pert']


member_id_list =  {'OsloCTM3v1-2':'r2',
                   'OsloCTM3v1-2freech4':'r1',
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}

member_id_list_sim3 =  {'OsloCTM3v1-2freech4':'r1',
                        'NorESM2-LM-C':'r1',
                        'LMDZ-INCA':'r1',
                        'UKESM1-0-LL':'r3'}

member_id_list = member_id_list_sim3

model_list = [#'OsloCTM3v1-2',
              'NorESM2-LM-C',
              #'EC-Earth3-AerChem',
              #'EMAC-DLR',
              'UKESM1-0-LL',
              'LMDZ-INCA'] #,
#model_list =[ 'CESM2-v212',
#              'UKESM1-0-LL'] #,
#              #'GFDL-ESM4-c1']



              
#model_list =['OsloCTM3v1-2freech4']
#Try the rest of the models

for experiment_id in experiment_id_list:
    for model_id in model_list:

        print(model_id)
        
        member_id = member_id_list[model_id]
        path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'

        if (experiment_id == 'cntr1850' or experiment_id == 'h2antr1850'):
            member_id = 'r1'

            
        if model_id =='EC-Earth3-AerChem':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id == 'EMAC-DLR':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id == 'CESM2-v212':
            area_path = '/nird/home/ragnhibs/hyway/tmp/'

        elif model_id =='OsloCTM3v1-2freech4':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        else:
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'

        print('pfull')
        read_global_vertdist(variable_id='pfull',
                             table_id=table_id,
                             experiment_id=experiment_id,
                             project_id=project_id,
                             member_id=member_id,
                             model_id=model_id,
                             path=path,
                             area_path=area_path)
        
        for variable_id in complist:
            print(variable_id)
            
            read_global_vertdist(variable_id=variable_id,
                                 table_id=table_id,
                                 experiment_id=experiment_id,
                                 project_id=project_id,
                                 member_id=member_id,
                                 model_id=model_id,
                                 path=path,
                                 area_path=area_path)
            
        
