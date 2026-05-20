import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


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

member_id_list =  {'OsloCTM3v1-2':'r2',
                   'EC-Earth3-AerChem':'r1',
                   'NorESM2-LM-C':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}

fig, axes = plt.subplots(nrows=3,ncols=7, figsize=(20,14),constrained_layout=True)

plotlist_h2 = ['deltaH2', 'surf_h2_per_h2_flux', 'surf_ch4_per_h2_flux',
               'ch4_flux_per_h2_flux', 'ch4_rf_per_h2_flux', 'ozone_rf_per_h2_flux',
               'h2o_rf_per_h2_flux']

plotlist_ch4 = ['deltaCH4', 'surf_ch4_per_ch4_flux', 'h2_flux_per_ch4_flux',
       'ozone_rf_per_ch4_flux', 'h2o_rf_per_ch4_flux']


for model in model_list:
    print(model)
    df_h2_flux = pd.read_csv('results_fluxes_csv/df_h2_flux_'+ model +'_' + member_id_list[model] + '_hyway.csv',index_col=0)
    df_ch4_flux = pd.read_csv('results_fluxes_csv/df_ch4_flux_'+ model +'_' + member_id_list[model] + '_hyway.csv',index_col=0)

    for ix, field in enumerate(plotlist_h2):
        axes[0,ix].plot(df_h2_flux[field],color=color_list[model])
        axes[0,ix].set_title('df_h2_flux: ' + field)

    for ix, field in enumerate(plotlist_ch4):
        axes[1,ix].plot(df_ch4_flux[field],color=color_list[model])
        axes[1,ix].set_title('df_ch4_flux: ' + field)
    print(df_ch4_flux.columns)


    axes[2,0].plot(df_h2_flux['ch4_flux_per_h2_flux']*df_h2_flux['deltaH2']/df_ch4_flux['deltaCH4'],color=color_list[model])
    axes[2,0].set_title('ch4_flux_per_h2_flux * deltaH2 /deltaCH4')

    #Constant
    #AGWP100_CO2 [mW yr m-2 Tg-1] Source: Table 7.SM.6 in IPCC AR6: 0.0895 pW m-2 yr kg-1 (p=10^-12) 
    agwp100_CO2 = 0.0895
    gwp_ch4 = df_h2_flux['ch4_rf_per_h2_flux']/agwp100_CO2
    axes[2,2].plot(gwp_ch4,color=color_list[model],label=model)
    axes[2,2].set_title('GWP CH4')
    
axes[2,2].legend()    
plt.tight_layout()
plt.show()
