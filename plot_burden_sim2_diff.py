import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os


def calc_annual_mean(dataset):
    # Calculate number of days in each month
    days_in_month = dataset.index.days_in_month
    print(days_in_month)
    print(dataset.index)
   
    dataset['weighted_values'] = dataset[model_id + '_'+member_id] * days_in_month
        
    #Weighted mean (365 days in each year)
    yearmean = dataset['weighted_values'].groupby(dataset.index.year).sum()/365.0
    yearmean.name = model_id
        
    return yearmean

molecw_list = {'h2':2.016,
               #'ch3oh':32.032,
               'ch4':16.042,
               'hcho':30.026,
               'h2o':28.01,
               'co':28.01,
               'o3':48.0,
               #'ch3cho': 44.052,
               #'ch3cooh': 60.052,
               #'ch3coch3': 58.080,
               #'nh3': 17.031,
               #'c6h6': 78.111,
               #'dms': 62.134,
               #'c2h6': 30.070,
               #'c2h4': 28.054,
               #'c2h2': 26.038,
               #'hcooh': 46.025,
               #'chocho': 60.052,
               'oh': 17.007,
               #'isop': 68.100,
               #'mhp': 78.111,
               #'mtp': 60.052,
               #'hno3': 63.012,
               'no2': 46.0055,
               'no': 30.0061,
               #'pan': 60.052,
               #'c3h8': 44.095,
               #'c3h6': 42.079,
               'so2': 64.066}







#model_list = ['OsloCTM3v1-2']
#model_list = ['UKESM1-0-LL'] #,
model_list = ['GFDL-ESM4-c1'] #'EC-Earth3-AerChem'] #'CESM2-v212']


color_list = {'OsloCTM3v1-2'   : '#D55E00',  # vermillion
              'CESM2-v212'     : '#0072B2',  # blue
              'EC-Earth3-AerChem':'#009E73', # bluish green
              'LMDZ-INCA'      : '#A6761D',   # warm brown 
              'EMAC-DLR'       : '#CC79A7',  # reddish purple
              'UKESM1-0-LL'    : '#56B4E9',  # sky blue
              'GFDL-ESM4-c1'   : '#E69F00',  # orange
              'NorESM2-LM-C'   : '#000000'}  # black

table_id = 'monthly'
project_id = 'hyway'


member_id_list =  {'OsloCTM3v1-2':'r2',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r1',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}



              


#List of experiments to plot:
experiment_list = ['h2pert','ch4pert']
#experiment_id = 'transient2010s'


linestylelist = {'transient2010s':'-',
                 'cntr':'-',
                 'h2pert':'-',
                 'ch4pert':'--'}
              

fig, axs = plt.subplots(nrows=4,ncols=3,squeeze=True,figsize=(20,15),sharey=False)
axs=axs.flatten()

for v,variable_id in enumerate(molecw_list):
    ax = axs[v]
    for model_id in model_list:
        member_id = member_id_list[model_id]
        #Burden
        unit = 'Tg'
        unit_burden = unit
        
        for experiment_id in experiment_list:
            filename = 'results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_' + member_id + '_'+project_id + '_' +experiment_id + '.csv'
            if os.path.exists(filename):
                burden = pd.read_csv(filename,index_col=0)
                print(burden)

                if model_id == 'GFDL-ESM4-c1':
                    print('Her')
                    print(burden.index)
                    
                    idx = burden.index.astype(str)
                    
                    # 1) Split year and the rest
                    years = idx.str.slice(0, 4).astype(int) + 2000     # add 2000 years
                    rest  = idx.str.slice(4)                           # "-MM-DD HH:MM:SS"
                    
                    # 2) Reassemble with zero-padded year
                    idx_shifted_str = years.map("{:04d}".format) + rest

                    # 3) Parse with explicit format (now safely in 2000+ range)
                    burden.index = pd.to_datetime(idx_shifted_str, format="%Y-%m-%d %H:%M:%S")

                else:
                    burden.index = pd.to_datetime(burden.index)

                    
                burden.index = burden.index.map(lambda dt: dt.replace(day=15, hour=12, minute=0, second=0))

                burden_pert = burden

                filename = 'results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id +'_' +project_id + '_' +'cntr' + '.csv'
                burden = pd.read_csv(filename,index_col=0)
                if model_id == 'GFDL-ESM4-c1':
                    print('Her')
                    print(burden.index)
                    
                    idx = burden.index.astype(str)
                    
                    # 1) Split year and the rest
                    years = idx.str.slice(0, 4).astype(int) + 2000     # add 2000 years
                    rest  = idx.str.slice(4)                           # "-MM-DD HH:MM:SS"
                    
                    # 2) Reassemble with zero-padded year
                    idx_shifted_str = years.map("{:04d}".format) + rest

                    # 3) Parse with explicit format (now safely in 2000+ range)
                    burden.index = pd.to_datetime(idx_shifted_str, format="%Y-%m-%d %H:%M:%S")
                else:
                    burden.index = pd.to_datetime(burden.index)

                burden.index = burden.index.map(lambda dt: dt.replace(day=15, hour=12, minute=0, second=0))
                burden_cntr = burden

                burden = burden_pert - burden_cntr
                
                burden_yearmean = calc_annual_mean(burden)
                
                #ax.plot(burden.index,burden[model_id],color=color_list[model_id])
                
                # Convert yearly index to datetime for plotting
                burden_yearmean.index = pd.to_datetime(burden_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
                ax.plot(burden_yearmean.index, burden_yearmean,linestyle =linestylelist[experiment_id],color=color_list[model_id],label=model_id + " ({:.3f})".format(burden_yearmean.mean()))
            else:
                print('Not generated: '+filename)


            
    ax.set_title(variable_id)
    ax.legend()
plt.show()
