import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os





def calc_annual_mean(dataset):
    # Calculate number of days in each month
    days_in_month = dataset.index.days_in_month
    #print(days_in_month)
    days_in_month = days_in_month.where(days_in_month != 29, 28)
    #exit()
    print(dataset.index)
   
    dataset['weighted_values'] = dataset[model_id + '_' + member_id] * days_in_month
        
    #Weighted mean (365 days in each year)
    yearmean = dataset['weighted_values'].groupby(dataset.index.year).sum()/365.0
    yearmean.name = model_id
        
    return yearmean

variable_list = ['h2',
                 'ch4',
                 'hcho',
                 'h2o',
                 'co',
                 'o3',
                 'oh',
                 'no2',
                 'no',
                 'so2',
                 'so4']


model_list = ['OsloCTM3v1-2',
              'NorESM2-LM-C' ,
              'EC-Earth3-AerChem']#,
#              'EMAC-DLR',
#              'LMDZ-INCA',
#              'CESM2-v212',
#              'UKESM1-0-LL',
#              'GFDL-ESM4-c1']

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



#List of experiments to plot:
#experiment_list = ['h2pert','ch4pert']

experiment_list = ['cntr','cntr1850','h2antr1850']

member_id_list_cntr =  {'OsloCTM3v1-2':'r2',
                        'NorESM2-LM-C':'r1',
                        'EC-Earth3-AerChem':'r1',
                        'EMAC-DLR':'r3',
                        'LMDZ-INCA':'r1',
                        'CESM2-v212':'r1',
                        'GFDL-ESM4-c1':'r1',
                        'UKESM1-0-LL':'r2'}

member_id_list_preind =  {'OsloCTM3v1-2':'r1',
                          'NorESM2-LM-C':'r1',
                          'EC-Earth3-AerChem':'r1',
                          'EMAC-DLR':'r3',
                          'LMDZ-INCA':'r1',
                          'CESM2-v212':'r1',
                          'GFDL-ESM4-c1':'r1',
                          'UKESM1-0-LL':'r2'}

linestyle_list = {'cntr':'-',
                  'h2antr1850':'-.',
                  'cntr1850':':'}
                


fig, axs = plt.subplots(nrows=4,ncols=3,squeeze=True,figsize=(20,15),sharey=False)
axs=axs.flatten()

for v,variable_id in enumerate(variable_list):
    ax = axs[v]
    for model_id in model_list:
        for experiment_id in experiment_list:
            if experiment_id == 'cntr':
                member_id_list = member_id_list_cntr
            else:
                member_id_list = member_id_list_preind
                
            member_id = member_id_list[model_id]
            #Burden
            unit = 'Tg'
            unit_burden = unit
        
            #for experiment_id in experiment_list:
            filename = 'results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv'
            if os.path.exists(filename):
                print(filename)
                burden = pd.read_csv(filename,index_col=0)
                
                burden.index = pd.to_datetime(burden.index)
                
                burden.index = burden.index.map(lambda dt: dt.replace(day=15, hour=12, minute=0, second=0)).floor("min")
            

            
                burden_yearmean = calc_annual_mean(burden)
            
                #ax.plot(burden.index,burden[model_id],color=color_list[model_id])
            
                # Convert yearly index to datetime for plotting
                burden_yearmean.index = pd.to_datetime(burden_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
                ax.plot(burden_yearmean.index, burden_yearmean,
                        linestyle = linestyle_list[experiment_id],
                        color=color_list[model_id],
                        label=model_id + " ({:.3f})".format(burden_yearmean.mean()))
            else:
                print('Not generated: '+filename)


            
    ax.set_title(variable_id)
    ax.legend()
plt.tight_layout()
plt.show()
