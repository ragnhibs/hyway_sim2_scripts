import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


#Plot budget values from files in results_csv and calculate annual means.
#This script is for hydrogen, but can easily be adjusted for other components.
#Remeber to add wetdeposition and emissions (also for the total loss in lifetime calc)

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



fig, axs = plt.subplots(nrows=3,ncols=3,squeeze=True,figsize=(20,15),sharey=False)
axs=axs.flatten()

variable_id = 'ch4'


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
experiment_list = ['cntr'] #,'h2pert','ch4pert']
#experiment_list = ['transient2010s']


symlist = {'transient2010s':'x',
           'cntr':'-',
           'h2pert':'d',
           'ch4pert':'*'}




for model_id in model_list:
    #avg_start = avg_period_list[model_id][0]
    #avg_end = avg_period_list[model_id][1]
    member_id = member_id_list[model_id]
    for experiment_id in experiment_list:

        #Surface concentration
        conv = 1e9
        unit = 'ppb'
        unit_surf = unit
        ax = axs[0]


        surfconc = pd.read_csv('results_csv/monthly_surfconc_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
        surfconc.index = pd.to_datetime(surfconc.index)
        
        surfconc_yearmean = calc_annual_mean(surfconc)
        surfconc_yearmean.index = pd.to_datetime(surfconc_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        
        #print(surfconc[model_id]*conv)
        
        #ax.plot(surfconc.index, surfconc[model_id]*conv,color=color_list[model_id])
        if experiment_id == 'cntr':
            ax.plot(surfconc_yearmean.index, surfconc_yearmean*conv,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(surfconc_yearmean.mean()*conv))


        #Burden
        unit = 'Tg'
        unit_burden = unit
        ax = axs[1]


        burden = pd.read_csv('results_csv/monthly_burden_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
        burden.index = pd.to_datetime(burden.index)
            
        burden_yearmean = calc_annual_mean(burden)
    
        #ax.plot(burden.index,burden[model_id],color=color_list[model_id])

        # Convert yearly index to datetime for plotting
        burden_yearmean.index = pd.to_datetime(burden_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        if experiment_id == 'cntr':
            ax.plot(burden_yearmean.index, burden_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(burden_yearmean.mean()))


        #Atmospheric production:
        unit = 'Tg yr$^{-1}$'
        unit_atmprod = unit
        conv = 1.0
        ax = axs[2]
        """
        atmprod = pd.read_csv('results_csv/monthly_atmprod_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
        atmprod.index = pd.to_datetime(atmprod.index)
        ax.plot(atmprod[model_id],color=color_list[model_id])
        atmprod_yearmean = calc_annual_mean(atmprod)
        atmprod_yearmean.index = pd.to_datetime(atmprod_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        ax.plot(atmprod_yearmean.index, atmprod_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(atmprod_yearmean.mean()))
        """




        #Atmospheric loss:
        unit = 'Tg yr$^{-1}$'
        unit_atmloss = unit
        conv = 1.0
        ax = axs[3]

        atmloss = pd.read_csv('results_csv/monthly_atmloss_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
        atmloss.index = pd.to_datetime(atmloss.index)
        
    
        #ax.plot(atmloss[model_id],color=color_list[model_id])
        atmloss_yearmean = calc_annual_mean(atmloss)
        atmloss_yearmean.index = pd.to_datetime(atmloss_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        if experiment_id == 'cntr':
            ax.plot(atmloss_yearmean.index, atmloss_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(atmloss_yearmean.mean()))




        #Soilsink
        unit = 'Tg yr$^{-1}$'
        unit_soilsink = unit
        conv = 1.0
        ax = axs[4]

        """
        soilsink = pd.read_csv('results_csv/monthly_soilsink_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
        soilsink.index = pd.to_datetime(soilsink.index)
        soilsink.index = soilsink.index.map(lambda x: x.replace(day=15))
        
    
        ax.plot(soilsink[model_id],color=color_list[model_id])
        soilsink_yearmean = calc_annual_mean(soilsink)
        soilsink_yearmean.index = pd.to_datetime(soilsink_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        ax.plot(soilsink_yearmean.index, soilsink_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(soilsink_yearmean.mean()))
        """

        
        #Emissions
        unit = 'Tg yr$^{-1}$'
        unit_emis = unit
        conv = 1.0
        ax = axs[6]

        """
        #Concentration driven experiment. Emission estimated as total loss minus total prod.
        if experiment_id == 'transient2010s':
            emis = soilsink[model_id]+atmloss[model_id]-atmprod[model_id]
            emis = emis.to_frame()
            ax.plot(emis[model_id],color=color_list[model_id])
            emis_yearmean = calc_annual_mean(emis)
            emis_yearmean.index = pd.to_datetime(emis_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
            ax.plot(emis_yearmean.index, emis_yearmean,'o',color=color_list[model_id],label='Est.emis '+ model_id + " ({:.1f})".format(emis_yearmean.mean()))


        else:
            emis = pd.read_csv('results_csv/monthly_emis_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id'_'+project_id + '_' +experiment_id + '.csv',index_col=0)
            emis.index = pd.to_datetime(emis.index)
            emis.index = emis.index.map(lambda x: x.replace(day=15))
            ax.plot(emis[model_id],color=color_list[model_id])
            emis_yearmean = calc_annual_mean(emis)
            emis_yearmean.index = pd.to_datetime(emis_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
            ax.plot(emis_yearmean.index, emis_yearmean,'o',color=color_list[model_id],label=model_id + " ({:.1f})".format(emis_yearmean.mean()))

        """
 
        
        #Atmospheric lifetime
        unit = 'years'
        unit_atmlife= unit
        conv = 1.0
        ax = axs[7]
        
        
        print(burden)
        print(atmloss)
        
        atmlifetime =  burden/atmloss
        
        print(atmlifetime)
        
        #ax.plot(atmlifetime[model_id],color=color_list[model_id])
        atmlifetime_yearmean = calc_annual_mean(atmlifetime)
        atmlifetime_yearmean.index = pd.to_datetime(atmlifetime_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        if experiment_id == 'cntr':
            ax.plot(atmlifetime_yearmean.index, atmlifetime_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(atmlifetime_yearmean.mean()))
    
    
        

        #Total lifetime
        unit = 'years'
        unit_totlife = unit
        conv = 1.0
        ax = axs[8]
        """

        totalloss = (soilsink[model_id]+atmloss[model_id]).to_frame()
            
        lifetime =  burden[model_id]/totalloss[model_id]
        lifetime = lifetime.to_frame()
        
        ax.plot(lifetime,color=color_list[model_id])
            
        lifetime_yearmean = calc_annual_mean(lifetime)
        lifetime_yearmean.index = pd.to_datetime(lifetime_yearmean.index.astype(str) + '-07-01')  # Mid-year for visibility
        ax.plot(lifetime_yearmean.index, lifetime_yearmean,symlist[experiment_id],color=color_list[model_id],label=model_id + " ({:.1f})".format(lifetime_yearmean.mean()))



        """

        #Combine all annual values and write to file:
        surfconc_yearmean.name='surfconc'
        burden_yearmean.name='burden'
        #atmprod_yearmean.name='atmprod'
        atmloss_yearmean.name='atmloss'
        #emis_yearmean.name='emis'
        #soilsink_yearmean.name='soilsink'
        #lifetime_yearmean.name='lifetime'
        atmlifetime_yearmean.name='atmlifetime'
        budget_annual = pd.concat([surfconc_yearmean,
                                   burden_yearmean,
                                   #atmprod_yearmean,
                                   atmloss_yearmean,
                                   #emis_yearmean,
                                   #soilsink_yearmean,
                                   #lifetime_yearmean,
                                   atmlifetime_yearmean],axis=1)
        budget_annual.index = budget_annual.index.year
        print(budget_annual)
        budget_annual.to_csv('annual_budget_csv/'+variable_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv')
        
        
        
    
surf_lim = {'h2': [0,1400],
            'ch4':[0,2500]}   

burden_lim = {'h2':[0,500],
              'ch4':[0,6000]}

#atm_prod_lim = {'h2':[0,80],
#                'ch4':[0,800]}

atm_loss_lim = {'h2':[0,70],
                'ch4':[0,1000]}
#soil_sink_lim = {'h2':[0,150]}
atm_lifetime_lim = {'h2':[0,12],
                    'ch4':[0,12]}
#tot_lifetime_lim= {'h2':[0,4]}
#emis_lim = {'h2':[0,70]}

#The ylim must be adjusted for each variables
axs[0].set_ylim(surf_lim[variable_id])
axs[0].legend(loc='lower right')
axs[0].set_title('Surfconc [ '+unit_surf + ']')

axs[1].set_ylim(burden_lim[variable_id])
axs[1].legend(loc='lower right')
axs[1].set_title('Burden [ '+unit_burden + ']')

#axs[2].set_ylim(atm_prod_lim[variable_id])
#axs[2].legend(loc='lower right')
axs[2].set_title('Atm.prod ['+unit_atmprod + ']')

axs[3].set_ylim(atm_loss_lim[variable_id])
axs[3].legend(loc='lower right')
axs[3].set_title('Atm.loss ['+unit_atmloss + ']')

#axs[4].set_ylim(soil_sink_lim[variable_id])
#axs[4].legend(loc='lower right')
axs[4].set_title('Soil sink ['+unit_soilsink + ']')

unit_scav = unit_soilsink
axs[5].set_title('Scavenging ['+unit_scav + ']')

#axs[6].set_ylim(emis_lim[variable_id])
#axs[6].legend(loc='lower right')
axs[6].set_title('Emissions ['+unit_emis + ']')
        
axs[7].set_ylim(atm_lifetime_lim[variable_id])
axs[7].legend()
axs[7].set_title('Atmospheric lifetime ['+unit_atmlife + ']')


#axs[8].set_ylim(tot_lifetime_lim[variable_id])
#axs[8].legend(loc='lower right')
axs[8].set_title('Total lifetime ['+unit_totlife + ']')




plt.suptitle(variable_id.upper())


plt.show()
