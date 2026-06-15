import numpy as np
import pandas as pd
import xarray as xr
import datetime
import matplotlib.pyplot as plt
import glob

#This script contains functions for reading global budget values from HYway simulations.
#The time series of monthly budget values are written to a csv in the catalogue results_csv/
#Important to follow the modelling protocol for file name and variables

#To do: if the dimension variables are slightly different for different files, the script will not work. This can be authomatically fixed in the script.


def add_2000yr(index):
    idx = index.astype(str)
    
    # 1) Split year and the rest
    years = idx.str.slice(0, 4).astype(int) + 2000     # add 2000 years
    rest  = idx.str.slice(4)                           # "-MM-DD HH:MM:SS"
    
    # 2) Reassemble with zero-padded year
    idx_shifted_str = years.map("{:04d}".format) + rest
    
    # 3) Parse with explicit format (now safely in 2000+ range)
    index = pd.to_datetime(idx_shifted_str, format="%Y-%m-%d %H:%M:%S")
    return index

def read_global_burden(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
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
    
    file_airmass = 'airmass_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    if not glob.glob(path + file_airmass): #os.path.exists(full_path):
        print('Did not find')
        print(path + file_airmass)
        return


    airmass_data = xr.open_mfdataset(path + file_airmass)

    if model_id == 'EC-Earth3-AerChem':
        print((area['areacella']*airmass_data['airmass'].isel(time=0)).sum().values)
    
    
    print(area['areacella'].sum().values)
    

    mass_per_gridbox = model_data[variable_id]*molecw/28.97*airmass_data['airmass']*area['areacella']
    monthly_burden = mass_per_gridbox.sum(dim=['lat', 'lon', 'lev'])*1e-9

        
    df = monthly_burden.to_dataframe(name=model_id +'_' +member_id)

    #Add years to the index to make this work
    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)
    
    df.to_csv('results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

def  read_global_burden_aerosols(variable_id,table_id,experiment_id,project_id,member_id,model_id,path,area_path):
    
    time_range='*'
    filename = 'mmr'+ variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)
    full_path = path + filename

    if not glob.glob(full_path): 
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
            print('Did not find')
            print(area_full_path)
            return

        area = xr.open_dataset(area_full_path)
    
    file_airmass = 'airmass_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    if not glob.glob(path + file_airmass): #os.path.exists(full_path):
        print('Did not find')
        print(path + file_airmass)
        return

    airmass_data = xr.open_mfdataset(path + file_airmass)
    
    if model_id == 'EC-Earth3-AerChem':
        print((area['areacella']*airmass_data['airmass'].isel(time=0)).sum().values)
    
    
    print(area['areacella'].sum().values)
    

    mass_per_gridbox = model_data['mmr'+variable_id]*airmass_data['airmass']*area['areacella']
    monthly_burden = mass_per_gridbox.sum(dim=['lat', 'lon', 'lev'])*1e-9

        
    df = monthly_burden.to_dataframe(name=model_id +'_' +member_id)


    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)

    
    df.to_csv('results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

def read_global_surfconc(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):

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
    

    if model_id == 'EMAC-DLR':
        surfconc = model_data[variable_id].isel(lev=-1)
    else:
        surfconc = model_data[variable_id].isel(lev=0)

    #Calculate area weighted global mean.
    weighted_field = surfconc.weighted(area['areacella'])
    globalmean = weighted_field.mean(dim=['lat', 'lon'])

    df = globalmean.to_dataframe(name=model_id +'_' +member_id)

    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)


    df.to_csv('results_csv/monthly_surfconc_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
   

def read_global_atmprod(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'prod'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)
    full_path = path + filename

    if not glob.glob(full_path): 
        print('Did not find')
        print(full_path)
        return
    
    model_data = xr.open_mfdataset(full_path, chunks={'time': 1})
        
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    else:
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return
    print(volume_full_path)
    

    volume = xr.open_mfdataset(volume_full_path, chunks={'time': 1})
    

    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']
    

    atmprod = model_data['prod'+variable_id]*volume['volume']

    days_in_month = model_data['time'].dt.days_in_month
    atmprod = atmprod.sum(dim=['lat','lev','lon'])*days_in_month*24.0*60.0*60.0  #kg sec-1 -> kg per month
    atmprod = atmprod*1e-9 #kg -> Tg
    print(atmprod)

    df = atmprod.to_dataframe(name=model_id +'_' +member_id)

    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)

    df.to_csv('results_csv/monthly_atmprod_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

    
def read_global_photoprod(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'prodphoto'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)

    full_path = path + filename

    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return
    

    model_data = xr.open_mfdataset(full_path, chunks={'time': 1})
        
        
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    else:
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return

    
    volume = xr.open_mfdataset(volume_full_path, chunks={'time': 1})
    
        
    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']
    
    atmprod = model_data['prodphoto'+variable_id]*volume['volume']
    days_in_month = model_data['time'].dt.days_in_month
    atmprod = atmprod.sum(dim=['lat','lev','lon'])*days_in_month*24.0*60.0*60.0  #kg sec-1 -> kg per month
    atmprod = atmprod*1e-9 #kg -> Tg
    print(atmprod)

    df = atmprod.to_dataframe(name=model_id +'_' +member_id)


    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)

    
    df.to_csv('results_csv/monthly_photoprod_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

    
def read_global_atmloss(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'loss'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(path + filename)
    full_path = path + filename

    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return
    
   
    model_data = xr.open_mfdataset(full_path, chunks={'time': 1})
        
    
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    else:    
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return

   
    volume = xr.open_mfdataset(volume_full_path, chunks={'time': 1})

    

              
    
    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']

    
    atmloss = model_data['loss'+variable_id]*volume['volume']
    days_in_month = model_data['time'].dt.days_in_month
    
    if model_id ==  'GFDL-ESM4-c1' and variable_id == 'ch4':
        atmloss = atmloss.sum(dim=['lat','lev','lon'])*days_in_month*24.0*60.0*60.0*16.04*1e-3 # mol per sec -> mol per month -> kg
    else:
        atmloss = atmloss.sum(dim=['lat','lev','lon'])*days_in_month*24.0*60.0*60.0  #kg sec-1 -> kg per month
    
    atmloss = atmloss*1e-9 #kg -> Tg

    df = atmloss.to_dataframe(name=model_id +'_' +member_id)

    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)
    
    df.to_csv('results_csv/monthly_atmloss_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

def read_global_photoloss(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'lossphoto'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    
    full_path = path + filename

    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return

    model_data = xr.open_mfdataset(full_path, chunks={'time': 1})
        
    if model_id == 'NorESM2-LM-C':         
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'12.nc'
    else:
        file_volume = 'volume'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'

    volume_full_path = path + file_volume

    if not glob.glob(volume_full_path):
        print('Did not find')
        print(volume_full_path)
        return

    
    volume = xr.open_mfdataset(volume_full_path, chunks={'time': 1})

    if model_id == 'CESM2-v212':
        volume['lat'] = model_data['lat']
        volume['lev'] = model_data['lev']

    atmloss = model_data['lossphoto'+variable_id]*volume['volume']
    days_in_month = model_data['time'].dt.days_in_month
    atmloss = atmloss.sum(dim=['lat','lev','lon'])*days_in_month*24.0*60.0*60.0  #kg sec-1 -> kg per month
    atmloss = atmloss*1e-9 #kg -> Tg

    df = atmloss.to_dataframe(name=model_id +'_' +member_id)
    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)
    df.to_csv('results_csv/monthly_photoloss_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
    

def read_global_soilsink(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'dry'+ variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    full_path = path + filename

    if not glob.glob(full_path): 
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
            print('Did not find')
            print(area_full_path)
            return

        area = xr.open_dataset(area_full_path)
        
    days_in_month = model_data['time'].dt.days_in_month
    data = model_data['dry'+variable_id]*area['areacella']*days_in_month*24.0*60.0*60.0
    data = data.sum(dim=['lat','lon'])*1e-9 #kg -> Tg

    df = data.to_dataframe(name=model_id +'_' +member_id)
    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)
    df.to_csv('results_csv/monthly_soilsink_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
   
def read_global_wetdep(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'wet'+ variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
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
            print('Did not find')
            print(area_full_path)
            return
        
        area = xr.open_dataset(area_full_path)
    days_in_month = model_data['time'].dt.days_in_month
    data = model_data['wet'+variable_id]*area['areacella']*days_in_month*24.0*60.0*60.0
    data = data.sum(dim=['lat','lon'])*1e-9 #kg -> Tg

    df = data.to_dataframe(name=model_id +'_' +member_id)
    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)
    df.to_csv('results_csv/monthly_wetdep_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

def read_global_emis(variable_id,table_id,experiment_id,project_id,member_id,molecw,model_id,path,area_path):
    
    time_range='*'
    filename = 'emi'+ variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    full_path = path + filename

    if not glob.glob(full_path): #os.path.exists(full_path):
        print('Did not find')
        print(full_path)
        return

    print(full_path)
    model_data = xr.open_mfdataset(full_path)

    if model_id == 'CESM2-v212':
        file_area = 'areacella_'+model_id+'_'+project_id +'_transient2010s_'+member_id +'.nc'
        area_full_path = area_path + file_area
        if not glob.glob(area_full_path):
            return
        area = xr.open_dataset(area_full_path)
        area = area.isel(time=0).drop_vars('time')
        area['lat'] = model_data['lat']
    else:
        file_area = 'areacella_fixed_'+model_id+'_'+project_id + '.nc'
        area_full_path = area_path + file_area
        if not glob.glob(area_full_path):
            print('Did not find:')
            print(area_full_path)
            return
        area = xr.open_dataset(area_full_path)

    
    days_in_month = model_data['time'].dt.days_in_month
    data = model_data['emi'+variable_id]*area['areacella']*days_in_month*24.0*60.0*60.0
    data = data.sum(dim=['lat','lon'])*1e-9 #kg -> Tg   #emissions per month

    df = data.to_dataframe(name=model_id +'_' +member_id)
    print(df)
    if model_id == 'GFDL-ESM4-c1':
        df.index = add_2000yr(df.index)

    print(df)
    df.to_csv('results_csv/monthly_emis_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')

