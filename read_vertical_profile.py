import numpy as np
import pandas as pd
import xarray as xr
import datetime
import glob


#Read vertival profile
def read_vertical_profile(variable_id,table_id,experiment_id,project_id,member_id,model_id,path,area_path,year_period):

    time_range='*'
    filename = variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    filename_pfull = 'pfull_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    print(path + filename)

    full_path = path + filename
    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return
    
    model_data = xr.open_mfdataset(full_path)
    model_data_pfull = xr.open_mfdataset(path + filename_pfull)

#    if model_id ==  'EC-Earth3-AerChem':
#        print(model_data['hyam'].values)
#        print(model_data['hybm'].values)
#        print(model_data['p0'].values)
#        #)=(hybm(lev)*sp(*,*)+hyam(lev))/100.
#        model_data['lev'] =(model_data['hyam'].values + 100000.0*model_data['hybm'].values)/100.0
#        print(model_data['lev'])
#        exit()
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
    
            
    model_field = model_data[variable_id].sel(time=slice(str(year_period[0]).zfill(4),str(year_period[1]).zfill(4)))
    model_field = model_field.mean(dim='time')

    model_field_pfull = model_data_pfull['pfull'].sel(time=slice(str(year_period[0]).zfill(4),str(year_period[1]).zfill(4)))
    model_field_pfull = model_field_pfull.mean(dim='time')
    
        
    #Calculate area weighted global mean.
    weighted_field = model_field.weighted(area['areacella'])
    globalmean = weighted_field.mean(dim=['lat', 'lon'])
    print(globalmean)
    
    weighted_field_pfull = model_field_pfull.weighted(area['areacella'])
    globalmean_pfull = weighted_field_pfull.mean(dim=['lat', 'lon'])
    print(globalmean_pfull)

    
    
    df = globalmean.to_dataframe(name=model_id +'_' +member_id)
    df.index = globalmean_pfull*0.01 #Convert from Pa to hPa
    print(df)
   
    df.to_csv('results_csv/vertical_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
    


    
#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'


experiment_id_list = ['cntr','h2pert','ch4pert']


variable_list = ['ch3oh',
                 'c2h6',
                 'h2',
                 'ch4',
                 'hcho',
                 'h2o',
                 'co',
                 'o3',
                 'oh',
                 'no2',
                 'no',
                 'so2',
                 'mmrso4',
                 'mhp']


model_list = ['EMAC-DLR'] #,
#              'NorESM2-LM-C',
#              'LMDZ-INCA',
#              'OsloCTM3v1-2',
#              'CESM2-v212',
#              'UKESM1-0-LL',
#              'GFDL-ESM4-c1',
#              'EC-Earth3-AerChem']


year_period_list = {'EMAC-DLR':[2039,2040],
                    'NorESM2-LM-C':[2037,2038],
                    'LMDZ-INCA':[2017,2018],
                    'OsloCTM3v1-2':[2038,2039],
                    'CESM2-v212':[2055,2075],
                    'UKESM1-0-LL':[2010,2014],
                    'GFDL-ESM4-c1':[50,60],
                    'EC-Earth3-AerChem':[2024,2029]}

member_id_list =  {'OsloCTM3v1-2':'r2',
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}




for variable_id in variable_list:
    
    for model_id in model_list:
        
        year_period = year_period_list[model_id]
        member_id = member_id_list[model_id]
            
        
        if model_id =='CESM2-v212':
            area_path = '/nird/home/ragnhibs/hyway/tmp/'
        elif model_id =='EMAC-DLR':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        elif model_id == 'EC-Earth3-AerChem':
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/fixed/'
        else:
            area_path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/transient2010s/'

        for experiment_id in experiment_id_list:    
            path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'
            read_vertical_profile(variable_id,table_id,experiment_id,project_id,member_id,model_id,path,area_path,year_period)
