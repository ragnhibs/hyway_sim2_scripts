import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

fig, axs = plt.subplots(nrows=3,ncols=3,squeeze=True,figsize=(20,15),sharey=False)
axs=axs.flatten()

#variable_id = 'h2'
#experiment_id = 'h2pert'

variable_id = 'ch4'
#experiment_id = 'ch4pert'
experiment_id = 'h2pert'

model_list = ['OsloCTM3v1-2',
              'EC-Earth3-AerChem',
              'NorESM2-LM-C' ,
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
                   'NorESM2-LM-C':'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}



title_dict = {'surfconc':'Surfconc [ppb]',
              'burden':'Burden [Tg]',
              'atmprod':'Atm.prod. [Tg yr$^{-1}$]',
              'atmloss' :'Atm.loss. [Tg yr$^{-1}$]',
              'emis' :'Emissions [Tg yr$^{-1}$]',
              'soilsink' :'Soil sink [Tg yr$^{-1}$]',
              'lifetime' : 'Total lifetime [yr]',
              'atmlifetime':'Atmospheric lifetime [yr]'}



for model_id in model_list:
    print('Model: ',model_id)
    member_id = member_id_list[model_id]
    budget_annual_cntr = pd.read_csv('annual_budget_csv/'+variable_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'cntr' + '.csv',index_col=0)
    budget_annual_pert = pd.read_csv('annual_budget_csv/'+variable_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
    budget_annual_diff = budget_annual_pert-budget_annual_cntr
    print(budget_annual_diff)
    budget_annual_diff = budget_annual_diff.dropna(how='all')
    budget_annual_diff.index = budget_annual_diff.index - budget_annual_diff.index[0]
    print(budget_annual_diff)
        
    budget_annual_diff['surfconc'] = budget_annual_diff['surfconc']*1e9
    for c,col in enumerate(budget_annual_diff.columns):
        axs[c].plot(budget_annual_diff[col],color=color_list[model_id],label=model_id)
        axs[c].set_title(title_dict[col])

axs[0].legend()
plt.show()
