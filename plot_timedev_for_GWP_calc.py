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
fig, axes = plt.subplots(nrows=4,ncols=6, figsize=(20,14),constrained_layout=True)
plotlist = ['surfconc','burden','lifetime','flux','pertlifetime','feedback_fact']
plotlist_ch4 = ['surfconc','burden','lifetime','flux']
plotlist_ch4_ch4pert = ['surfconc','burden','lifetime','flux','pertlifetime','feedback_fact']
plotlist_h2_ch4pert = ['surfconc','burden','lifetime','flux']


for model in model_list:
    print(model)
    
    delta_budget_h2pert = pd.read_csv('results_fluxes_csv/delta_budget_h2pert_'+ model +'_' + member_id_list[model] + '_hyway.csv')
    if model == 'CESM2-v212':
        delta_budget_h2pert.index = delta_budget_h2pert.index - 5
    else:
        delta_budget_h2pert.index = delta_budget_h2pert.index + 1

    delta_budget_h2pert.loc[0] = 0
    delta_budget_h2pert = delta_budget_h2pert.sort_index()

    
    delta_ch4budget_h2pert=pd.read_csv('results_fluxes_csv/delta_ch4budget_h2pert_'+ model +'_' + member_id_list[model] + '_hyway.csv')

    if model == 'CESM2-v212':
        delta_ch4budget_h2pert.index = delta_ch4budget_h2pert.index - 5
    else:
        delta_ch4budget_h2pert.index = delta_ch4budget_h2pert.index + 1
    
    delta_ch4budget_h2pert.loc[0] = 0
    delta_ch4budget_h2pert = delta_ch4budget_h2pert.sort_index()


    
    delta_budget_ch4pert = pd.read_csv('results_fluxes_csv/delta_budget_ch4pert_'+ model +'_' + member_id_list[model] + '_hyway.csv')

    if model == 'CESM2-v212':
        delta_budget_ch4pert.index = delta_budget_ch4pert.index - 5
    else:
        delta_budget_ch4pert.index = delta_budget_ch4pert.index + 1
    print(delta_budget_ch4pert)
    

    delta_budget_ch4pert.loc[0] = 0
    delta_budget_ch4pert = delta_budget_ch4pert.sort_index()
    
    delta_ch4budget_ch4pert = pd.read_csv( 'results_fluxes_csv/delta_ch4budget_ch4pert_'+ model +'_' + member_id_list[model] + '_hyway.csv')

    if model == 'CESM2-v212':
        delta_ch4budget_ch4pert.index = delta_ch4budget_ch4pert.index - 5
    else:
        delta_ch4budget_ch4pert.index = delta_ch4budget_ch4pert.index + 1
    print(delta_ch4budget_ch4pert)

    delta_ch4budget_ch4pert.loc[0] = 0
    delta_ch4budget_ch4pert = delta_ch4budget_ch4pert.sort_index()

    for ix, field in enumerate(plotlist):
        axes[0,ix].plot(delta_budget_h2pert[field],color=color_list[model])
        axes[0,ix].set_title('H2 h2pert: ' + field)

    for ix, field in enumerate(plotlist_ch4):
        axes[1,ix].plot(delta_ch4budget_h2pert[field],color=color_list[model])
        axes[1,ix].set_title('CH4 h2pert: ' + field)

    for ix, field in enumerate(plotlist_ch4_ch4pert):
        axes[2,ix].plot(delta_ch4budget_ch4pert[field],color=color_list[model])
        axes[2,ix].set_title('CH4 ch4pert: ' + field)

    for ix, field in enumerate(plotlist_h2_ch4pert):
        axes[3,ix].plot(delta_budget_ch4pert[field],color=color_list[model])
        axes[3,ix].set_title('H2 ch4pert: ' + field)



    #FLUX output
    #FLUX output.
    #Initialize hydrogen flux table:
    columns_names={'deltaH2':'Flux H2 [Tg/yr]',
                   'surf_h2_per_h2_flux': 'Surf. conc. H2 per flux [ppb yr/Tg]',
                   'surf_ch4_per_h2_flux':'Surf. conc. CH4 per flux [ppb yr/Tg]',
                   'ch4_flux_per_h2_flux':'Flux CH4/Flux H2 [Tg CH4/Tg H2]',
                   'ch4_rf_per_h2_flux':'CH4 RF per flux [mW m-2 yr/ Tg]',
                   #'trop_du_ozone_per_h2_flux':'Trop. ozone per flux [10$^{-3}$ DU yr/Tg]',
                   #'strat_du_ozone_per_h2_flux':'Strat. ozone per flux [10$^{-3}$ DU yr/Tg]',
                   'ozone_rf_per_h2_flux':'ozone RF per flux [mW m-2 yr/ Tg]',
                   'h2o_rf_per_h2_flux':'Strat. H2O RF per flux [mW m-2 yr/ Tg]'}#,
    #'aerosol_rf_per_h2_flux':'Aerosol RF per flux [mW m-2 yr/ Tg]'}
    
    df_h2_flux = pd.DataFrame(data=[],columns=columns_names)
    
    df_h2_flux['deltaH2']=delta_budget_h2pert['flux']
    df_h2_flux['surf_h2_per_h2_flux']=delta_budget_h2pert['surfconc']/delta_budget_h2pert['flux']
    print(df_h2_flux)



    #Initialize methane flux table:
    columns_names={'deltaCH4':'Flux CH4 [Tg/yr]',
                   'surf_ch4_per_ch4_flux':'Surf. conc. CH4 per flux [ppb yr/Tg]',
                   'h2_flux_per_ch4_flux':'Flux H2/Flux CH4 [Tg H2/Tg CH4]',
                   #'trop_du_ozone_per_ch4_flux':'Trop. ozone per flux [10$^{-3}$ DU yr/Tg]',
                   #'strat_du_ozone_per_ch4_flux':'Strat. ozone per flux [10$^{-3}$ DU yr/Tg]',
                   'ozone_rf_per_ch4_flux':'ozone RF per flux [mW m-2 yr/ Tg]',
                   'h2o_rf_per_ch4_flux':'Strat H2O RF per flux [mW m-2 yr/ Tg]'} #,
    #'aerosol_rf_per_ch4_flux':'Aerosol RF per flux [mW m-2 yr/ Tg]'}
    
    df_ch4_flux = pd.DataFrame(data=[],columns=columns_names)
    
    df_ch4_flux['deltaCH4']=delta_ch4budget_ch4pert['flux']
    df_ch4_flux['surf_ch4_per_ch4_flux'] = delta_ch4budget_ch4pert['surfconc']/delta_ch4budget_ch4pert['flux']
    print(df_ch4_flux)



    df_h2_flux['ch4_flux_per_h2_flux']=delta_ch4budget_h2pert['flux']/delta_budget_h2pert['flux']*-1.0
    print(df_h2_flux['ch4_flux_per_h2_flux'])

    #Specific RF for CH4 [mW m-2 ppb-1] Etminan et al., 2016
    spec_rf_ch4 = 0.44800

    #The adjustment is –14% ± 15% IPCC AR6
    spec_rf_ch4 = spec_rf_ch4*(1.0-0.14)
    
    df_h2_flux['ch4_rf_per_h2_flux'] = df_ch4_flux['surf_ch4_per_ch4_flux']*df_h2_flux['ch4_flux_per_h2_flux']*spec_rf_ch4
    print(df_h2_flux['ch4_rf_per_h2_flux'])


    df_h2_flux.to_csv('results_fluxes_csv/df_h2_flux_'+ model +'_' + member_id_list[model] + '_hyway.csv')
    df_ch4_flux.to_csv('results_fluxes_csv/df_ch4_flux_'+ model +'_' + member_id_list[model] + '_hyway.csv')
    

plt.show()

