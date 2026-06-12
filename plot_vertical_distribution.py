import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
import matplotlib.cm as cm
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


#Plot zonal mean fields from HYway simulation 2

def plot_zonal(field_3d, pfull_3d, cminmax):
    zonal_mean = field_3d.mean(dim=['lon'],keep_attrs=True)
    zonal_mean_pfull = pfull_3d.mean(dim=['lon'],keep_attrs=True)

    # Extract values as numpy arrays
    lat = zonal_mean.lat.values
    pressure = zonal_mean_pfull.values  # 2D array (lev, lat)
    print(pressure.max(),pressure.min())
    
    data = zonal_mean.values  # 2D array (lev, lat)
    
    # Use matplotlib's pcolormesh directly
    im = ax.pcolormesh(lat, pressure, data, cmap=cmap, vmin=cminmax[0], vmax=cminmax[1])
    # Add colorbar
    plt.colorbar(im, ax=ax)
    
    ax.set_yscale('log')
    ax.set_ylim([1000, 1])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_ylabel('Pressure (hPa)')
    ax.set_xlabel('Latitude')
    ax.set_title('')


def read_vmr():
    filename = path + variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    print(filename)
    if model_id == 'GFDL-ESM4-c1':
        #Read variable
        model_data = xr.open_mfdataset(filename)
        #print(model_data.time)
        #print(f"{year_period[0]:04d}")
        #print(f"{year_period[1]:04d}")
        model_data =model_data.sel(time=slice(f"{year_period[0]:04d}", f"{year_period[1]:04d}"))
        #print(model_data)
       
    else:
        model_data = xr.open_mfdataset(filename).sel(time=slice(str(year_period[0]),str(year_period[1])))
    print(model_data.time)

    model_field = model_data[variable_id].mean(dim='time')*unit_fact[unit_variable[variable_id]]   

    
    #Pressure:
    filename = path + 'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+time_range+'.nc'
    #Read variable:
    if model_id == 'GFDL-ESM4-c1':
        model_data = xr.open_mfdataset(filename)
        #print(model_data.time)
        #print(f"{year_period[0]:04d}")
        #print(f"{year_period[1]:04d}")
        model_data =model_data.sel(time=slice(f"{year_period[0]:04d}", f"{year_period[1]:04d}"))
        #print(model_data)
       
    else:
        model_data = xr.open_mfdataset(filename).sel(time=slice(str(year_period[0]),str(year_period[1])))

    print(model_data.time)

    pressure_field = model_data['pfull'].mean(dim='time')*0.01 #Convert from Pa to hPa

    model_field.to_netcdf('results_netcdf/'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' 
                          +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc')
    pressure_field.to_netcdf('results_netcdf/'+'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'
                             +str(year_period[0])+'_'+str(year_period[1])+'.nc')

    return model_field, pressure_field


#Read precaluculated netcdf files:
def read_vmr_from_netcdf():
    print('Read precalculated netcdf files')
    filename = 'results_netcdf/'+variable_id+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data = xr.open_dataset(filename)
    filename = 'results_netcdf/'+'pfull'+'_'+table_id+'_'+model_id+'_'+project_id + '_' +experiment_id+'_'+member_id+'_'+str(year_period[0])+'_'+str(year_period[1])+'.nc'
    model_data_pfull = xr.open_dataset(filename)
    return model_data[variable_id], model_data_pfull['pfull']



##########################################################
#Choose perturbation experiment to plot relative to cntr.
#experiment_id_pert = 'ch3ohpert'
experiment_id_pert = 'h2pert'
#experiment_id_pert = 'ch4pert'   


time_range = '*'
table_id = 'monthly'
project_id = 'hyway'

###################################################
#Choose model_id and member_id

#model_id = 'OsloCTM3v1-2'
#member_id = 'r2'

#model_id = 'CESM2-v212'
#member_id = 'r1'

#model_id = 'EC-Earth3-AerChem'
#member_id = 'r1'

model_id = 'EMAC-DLR'
member_id = 'r3'


#model_id = 'GFDL-ESM4-c1'
#member_id = 'r1'


#model_id = 'UKESM1-0-LL'
#member_id ='r2'

#model_id = 'NorESM2-LM-C'
#member_id = 'r1'

#model_id = 'LMDZ-INCA'
#member_id = 'r1'

year_period_list = {'EMAC-DLR':[2039,2040],
                    'NorESM2-LM-C':[2027,2028],
                    'LMDZ-INCA':[2018,2019],
                    'OsloCTM3v1-2':[2038,2039],
                    ##'OsloCTM3v1-2':[2022,2023],
                    'CESM2-v212':[2055,2075],
                    ##'CESM2-v212':[2045,2055],
                    #'UKESM1-0-LL':[2000,2004],
                    'UKESM1-0-LL':[2005,2010],
                    'GFDL-ESM4-c1':[50,60],
                    'EC-Earth3-AerChem':[2024,2030]}


#############################################################################################################################
#If this is false, read the original files on nird. If this is true, a netcdf is previosly made and this will be read instead.
#Read previosly:
read_prev = False


#Variable to be plotted
var_list = ['h2','ch4','hcho','o3','oh','h2o']


#Make figure: 
noOfCols = 3
noOfRows = len(var_list)

fig, axes = plt.subplots(nrows=noOfRows,ncols=noOfCols, figsize=(10,14),constrained_layout=True)


#Relative
cminmax_rel = {'h2':[-100,100],
               'ch4':[-5,5],
               'hcho':[-5,5],
               'o3':[-5,5],
               'oh':[-25,25],
               'h2o':[-25,25]}

#Absolute
cminmax_abs = {'h2':[-600,600],
               'ch4':[-10,10],
               'hcho':[-10,10],
               'o3':[-20,20],
               'oh':[-0.25,0.25],
               'h2o':[-250,250]}

cminmax_cntr = {'h2':[250,750],
                'ch4':[0,2000],
               'hcho':[0,250],
               'o3':[0,100],
               'oh':[0,0.3],
               'h2o':[0,4500]}

unit_variable = {'h2':'ppb',
                 'ch4':'ppb',
                 'hcho':'ppt',
                 'o3':'ppb',
                 'oh':'ppt',
                 'h2o':'ppb'}

unit_fact = {'ppb':1e9,
             'ppt':1e12,
             'vmr':1}




for v,variable_id in enumerate(var_list): #[:-1]): #NBNBNB Drop h2o

    year_period = year_period_list[model_id]
    experiment_id = 'cntr'
    path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'

    #Read cntr
    if read_prev:
        model_data_cntr, pfull_cntr = read_vmr_from_netcdf()
    else:
        model_data_cntr, pfull_cntr = read_vmr()


    print(model_data_cntr.mean(dim=['lon']))
    print(pfull_cntr.mean(dim=['lon']))

    #Plot control:
    ax = axes[v,0]
    cmap = plt.get_cmap('OrRd')
    plot_zonal(model_data_cntr, pfull_cntr, cminmax_cntr[variable_id])
    ax.set_title('CNTR ' + variable_id + ' [' + unit_variable[variable_id] + ']')

    #Plot absolute difference:
    experiment_id = experiment_id_pert

    path = '/projects/NS11106K/HYway/modelling_repository/'+model_id+'/'+experiment_id+'/'

    #Read perturbation experiment
    if read_prev:
        model_data_pert, pfull_pert = read_vmr_from_netcdf()
    else:
        model_data_pert, pfull_pert = read_vmr()
        

    ax = axes[v,1]
    cmap = plt.get_cmap('seismic')
    plot_zonal(model_data_pert-model_data_cntr, pfull_cntr, cminmax_abs[variable_id])
    ax.set_title(experiment_id + ' - CNTR')
    ax.set_title('Absolute diff. ' +variable_id+ ' [' + unit_variable[variable_id] + ']')


    #Plot relative difference:
    ax = axes[v,2]
    plot_zonal((model_data_pert-model_data_cntr)/model_data_cntr*100.0, pfull_cntr, cminmax_rel[variable_id])
    ax.set_title('Relative diff. ' +variable_id+ ' [%]')
    


plt.suptitle(model_id + ' ' + experiment_id_pert   +' rel to  '+ 'cntr') 
plt.show()

exit()
