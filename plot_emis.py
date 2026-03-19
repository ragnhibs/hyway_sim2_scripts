import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os

plt.rcParams.update({'font.size': 8})

def calc_annual_mean(dataset):
    # Calculate number of days in each month
    days_in_month = dataset.index.days_in_month
    days_in_month = days_in_month.where(days_in_month != 29, 28)
    #print(days_in_month)
    #print(dataset.index)
    print(dataset)
    
    dataset['weighted_values'] = dataset[model_id+'_'+member_id] * days_in_month
        
    #Weighted mean (365 days in each year)
    yearmean = dataset['weighted_values'].groupby(dataset.index.year).sum()/365.0
    yearmean.name = model_id
        
    return yearmean

emilist =['emich3cho',
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



model_list = ['OsloCTM3v1-2',
              'EC-Earth3-AerChem',
              'EMAC-DLR',
              'LMDZ-INCA',
              'CESM2-v212',
              'UKESM1-0-LL',
              'GFDL-ESM4-c1']



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
#experiment_list = ['cntr','h2pert','ch4pert']
#experiment_id = 'transient2010s'
experiment_id = 'cntr'

symlist = {'transient2010s':'x',
           'cntr':'-',
           'h2pert':'d',
           'ch4pert':'*'}


fig, axs = plt.subplots(nrows=5,ncols=5,squeeze=True,figsize=(30,15),sharey=False)
axs=axs.flatten()


for v,comp in enumerate(emilist):
    emis_all_year = pd.DataFrame([])
    variable_id = comp[3:]
    ax = axs[v]
    for model_id in model_list:
        print(model_id)
        member_id = member_id_list[model_id]
        
        unit = 'Tg yr$^{-1}$'
        
        

        filename = 'results_csv/monthly_emis_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id + '_' +project_id + '_' +experiment_id + '.csv'
        print(filename)
        if os.path.exists(filename):
            emis = pd.read_csv(filename,index_col=0)
            #if model_id ==  'EC-Earth3-AerChem':
            #    emis.index = index_save
            #else:
            if model_id == 'GFDL-ESM4-c1':
                    print('Her')
                    print(emis.index)
                    
                    idx = emis.index.astype(str)
                    
                    # 1) Split year and the rest
                    years = idx.str.slice(0, 4).astype(int) + 2000     # add 2000 years
                    rest  = idx.str.slice(4)                           # "-MM-DD HH:MM:SS"
                    
                    # 2) Reassemble with zero-padded year
                    idx_shifted_str = years.map("{:04d}".format) + rest

                    # 3) Parse with explicit format (now safely in 2000+ range)
                    emis.index = pd.to_datetime(idx_shifted_str, format="%Y-%m-%d %H:%M:%S")

            
            emis.index = pd.to_datetime(emis.index)
            index_save = emis.index

            emis.index = emis.index.map(lambda dt: dt.replace(day=15, hour=12, minute=0, second=0))
            emis_yearmean = calc_annual_mean(emis)
            
            #ax.plot(emis.index,emis[model_id],color=color_list[model_id])
            
            # Convert yearly index to datetime for plotting
            emis_yearmean.index = pd.to_datetime(emis_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
            ax.plot(emis_yearmean.index, emis_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(emis_yearmean.mean()))
            ax.set_title(variable_id)
            ax.set_ylabel(unit)
            ax.legend()
plt.show()
