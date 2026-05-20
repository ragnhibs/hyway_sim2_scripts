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


#Move the annual budget files calculated on nird to this folder.
budget_path = './annual_budget_csv/'

#Runs to include.
scen_list = ['cntr','h2pert','ch4pert']


#budget_cntr = pd.DataFrame([],columns=model_list)
#budget_h2pert = pd.DataFrame([],columns=model_list)
#budget_ch4pert = pd.DataFrame([],columns=model_list)

fig, axes = plt.subplots(nrows=3,ncols=6, figsize=(20,14),constrained_layout=True)
#axes = axes.flatten()

plotlist = ['surfconc','burden','lifetime','flux','pertlifetime','feedback_fact']
plotlist_ch4 = ['surfconc','burden','lifetime','flux']
plotlist_ch4_ch4pert = ['surfconc','burden','lifetime','flux','pertlifetime','feedback_fact']

for model in model_list:
    for scen in scen_list:
        
        budget = pd.read_csv(budget_path + 'h2_'+ model +'_' + member_id_list[model] + '_hyway_' + scen + '.csv',index_col=0)
        ch4budget = pd.read_csv(budget_path + 'ch4_'+ model +'_' + member_id_list[model] + '_hyway_' + scen + '.csv',index_col=0)
        #avg_period = avg_period_list[model]
        
        
        #Calculate the average budget over the period when the model reaches a new steady state after the perturbation.
        #budget = budget.loc[avg_period[0]:avg_period[1]].mean()
        
        #Surface concentraton, from mol/mol to ppb
        budget['surfconc']=budget['surfconc']*1e9
        ch4budget['surfconc']=ch4budget['surfconc']*1e9

                #Lifetime calculated based on annual values not equal monthly...
        budget['lifetime_annual']=budget['burden']/(budget['atmloss']+budget['soilsink'])
        budget['flux'] = budget['burden']/budget['lifetime']

        ch4budget['lifetime_annual']=ch4budget['burden']/(ch4budget['atmloss'])

        tau_strat = 120.0*2.0 #Multiplied by two for not double counting OH loss in stratosphere. What about models that do not include stratospheric chemistry?

        #CH4 tau_soil [yr] 
        tau_soil = 160.0

        
        ch4budget['lifetime'] = 1.0/(1.0/ch4budget['atmlifetime'] + 1.0/tau_strat + 1.0/tau_soil)
        ch4budget['flux'] = ch4budget['burden']/ch4budget['lifetime']
        
        if scen == 'cntr':
            budget_cntr = budget
            ch4budget_cntr = ch4budget
        elif scen == 'h2pert':
            budget_h2pert=budget
            ch4budget_h2pert=ch4budget
        elif scen == 'ch4pert':
            budget_ch4pert=budget
            ch4budget_ch4pert=ch4budget

        print(ch4budget)


    delta_budget_h2pert = budget_h2pert - budget_cntr
    delta_ch4budget_h2pert = ch4budget_h2pert - ch4budget_cntr
    
    delta_budget_ch4pert = budget_ch4pert - budget_cntr
    delta_ch4budget_ch4pert = ch4budget_ch4pert - ch4budget_cntr

    
    delta_budget_h2pert['pertlifetime'] = delta_budget_h2pert['burden']/delta_budget_h2pert['flux']   
    print(delta_budget_h2pert)
    delta_budget_h2pert['feedback_fact'] = delta_budget_h2pert['pertlifetime']/budget_cntr['lifetime']

    delta_ch4budget_ch4pert['pertlifetime'] = delta_ch4budget_ch4pert['burden']/delta_ch4budget_ch4pert['flux']   
    print(delta_budget_h2pert)
    delta_ch4budget_ch4pert['feedback_fact'] = delta_ch4budget_ch4pert['pertlifetime']/ch4budget_cntr['lifetime']


    #delta_budget_h2pert
    outputfile = 'results_fluxes_csv/delta_budget_h2pert_'+ model +'_' + member_id_list[model] + '_hyway.csv'
    delta_budget_h2pert.to_csv(outputfile)
    
    #delta_ch4budget_h2pert
    outputfile = 'results_fluxes_csv/delta_ch4budget_h2pert_'+ model +'_' + member_id_list[model] + '_hyway.csv'
    delta_ch4budget_h2pert.to_csv(outputfile)

    #delta_budget_ch4pert
    outputfile = 'results_fluxes_csv/delta_budget_ch4pert_'+ model +'_' + member_id_list[model] + '_hyway.csv'
    delta_budget_ch4pert.to_csv(outputfile)
    
    #delta_ch4budget_ch4pert
    outputfile = 'results_fluxes_csv/delta_ch4budget_ch4pert_'+ model +'_' + member_id_list[model] + '_hyway.csv'
    delta_ch4budget_ch4pert.to_csv(outputfile)

    for ix, field in enumerate(plotlist):
        axes[0,ix].plot(delta_budget_h2pert[field],color=color_list[model])
        axes[0,ix].set_title('H2: ' + field)

    for ix, field in enumerate(plotlist_ch4):
        axes[1,ix].plot(delta_ch4budget_h2pert[field],color=color_list[model])
        axes[1,ix].set_title('CH4 h2pert: ' + field)

    for ix, field in enumerate(plotlist_ch4_ch4pert):
        axes[2,ix].plot(delta_ch4budget_ch4pert[field],color=color_list[model])
        axes[2,ix].set_title('CH4 ch4pert: ' + field)


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
   
        
plt.show()
exit()
exit()


        
