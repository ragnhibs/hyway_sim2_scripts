import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import xarray as xr
#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'

plt.rcParams.update({'font.size': 12})


experiment_id_list = ['h2pert','ch4pert']

linestylelist = {'cntr':'-',
                 'h2pert':'--',
                 'ch4pert':':'}



member_id_list =  {'OsloCTM3v1-2':'r2',
                   'NorESM2-LM-C'   :'r1',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r3',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}

model_names_out = {'OsloCTM3v1-2':'OsloCTM3v1-2',
                   'NorESM2-LM-C':'NorESM2.3-LM-C',
                   'EC-Earth3-AerChem':'EC-Earth3-AerChem',
                   'EMAC-DLR':'EMAC',
                   'LMDZ-INCA':'LMDZ-INCA',
                   'CESM2-v212':'CESM2-v212',
                   'UKESM1-0-LL':'UKESM1-0-LL',
                   'GFDL-ESM4-c1':'GFDL-ESM4.1'}

logplot = True




variable_list = ['h2',
                 'ch4',
                 'h2o',
                 'o3']


model_list = ['NorESM2-LM-C',
              'OsloCTM3v1-2',
              'EC-Earth3-AerChem',
              'EMAC-DLR',
              'LMDZ-INCA',
              'CESM2-v212',
              'UKESM1-0-LL',
              'GFDL-ESM4-c1']

model_list = sorted(model_list)


              
to_hPa = 0.01
             


color_list = {'OsloCTM3v1-2'   : '#D55E00',  # vermillion
              'CESM2-v212'     : '#0072B2',  # blue
              'EC-Earth3-AerChem':'#009E73', # bluish green
              'LMDZ-INCA'      : '#A6761D',   # warm brown 
              'EMAC-DLR'       : '#CC79A7',  # reddish purple
              'UKESM1-0-LL'    : '#56B4E9',  # sky blue
              'GFDL-ESM4-c1'   : '#E69F00',  # orange
              'NorESM2-LM-C'   : '#000000',  # black
}


avg_period_list = {'EMAC-DLR':[2036,2041],
                   'NorESM2-LM-C':[2033,2038],
                   'LMDZ-INCA':[2027,2029],
                   'OsloCTM3v1-2':[2038,2039],
                   'CESM2-v212':[2045,2075],
                   'UKESM1-0-LL':[2010,2014],
                   'GFDL-ESM4-c1':[26,60],
                   'EC-Earth3-AerChem':[2024,2029]}

#Can read this from a file:
scale_fact = {'OsloCTM3v1-2':         0.559466,
              'NorESM2-LM-C'   :      0.632010,
              'EC-Earth3-AerChem':    0.641707,
              'EMAC-DLR'          :   0.520235,
              'LMDZ-INCA'         :   0.596359,
              'CESM2-v212'        :  0.714198,
              'UKESM1-0-LL'       :   0.692561,
              'GFDL-ESM4-c1'      :   0.479299}




fig, axs = plt.subplots(nrows=4,ncols=4,squeeze=True,figsize=(24,15))
#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'

for model_id in model_list:
    member_id = member_id_list[model_id]
    print(model_id)
    print('monthly_vertical_pfull_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'cntr' + '.csv')
    pfull = xr.open_dataset('monthly_vertical_pfull_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'cntr' + '.csv')
    year1 = avg_period_list[model_id][0]
    year2 = avg_period_list[model_id][1]

    print(pfull.time.values)
 
    mean_pfull = (
        pfull['pfull']
        .where(
            (pfull.time.dt.year >= year1) &
            (pfull.time.dt.year <= year2),
            drop=True
        )
        .mean('time')
        * to_hPa
    )
    
    
    
    for c,comp in enumerate(variable_list):
        print(comp)
        data = xr.open_dataset('monthly_vertical_'+comp+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'cntr' + '.csv')
        data_h2pert = xr.open_dataset('monthly_vertical_'+comp+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'h2pert' + '.csv')
        data_ch4pert = xr.open_dataset('monthly_vertical_'+comp+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +'ch4pert' + '.csv')

        if model_id == 'LMDZ-INCA':
            data_h2pert['time'] = data.time
            data_ch4pert['time'] = data.time
               
        
        pert_h2_perc = (data_h2pert - data)/data*100.0
        pert_ch4_perc = (data_ch4pert - data)/data*100.0

        pert_h2_total_perc = ((data_h2pert - data)+scale_fact[model_id]*(data_ch4pert - data))/data*100.0

        

        
        mean_comp = (
            data[comp].
            where(
                (data.time.dt.year >= year1) &
                (data.time.dt.year <= year2),
                drop=True
            )
            .mean('time')
        )

        mean_h2pert =(pert_h2_perc[comp].
            where(
                (pert_h2_perc.time.dt.year >= year1) &
                (pert_h2_perc.time.dt.year <= year2),
                drop=True
            )
            .mean('time')
        )




        #pert_h2_perc[comp].sel(time=slice(f'{year1}-01-01', f'{year2}-12-31')).mean('time')


        mean_ch4pert =(
            pert_ch4_perc[comp].
            where(
                (pert_ch4_perc.time.dt.year >= year1) &
                (pert_ch4_perc.time.dt.year <= year2),
                drop=True
            )
            .mean('time')
        )

        #pert_ch4_perc[comp].sel(time=slice(f'{year1}-01-01', f'{year2}-12-31')).mean('time')
        mean_h2totalpert = (pert_h2_total_perc[comp].
            where(
                (pert_h2_total_perc.time.dt.year >= year1) &
                (pert_h2_total_perc.time.dt.year <= year2),
                drop=True
            )
            .mean('time')
        )


            #pert_h2_total_perc[comp].sel(time=slice(f'{year1}-01-01', f'{year2}-12-31')).mean('time')

    
        for yr in np.arange(year1,year2+1):
            annual_mean = (
                data[comp].
                where(
                    (data.time.dt.year >= yr) &
                    (data.time.dt.year < yr+1),
                    drop=True
                )
                .mean('time')
            )
            
            axs[c,0].plot(annual_mean,mean_pfull,color=color_list[model_id],alpha=0.3,linewidth=0.5,zorder=-10)      
            
            annual_mean_pert =(
                pert_h2_perc[comp].
                where(
                    (pert_h2_perc.time.dt.year >= yr) &
                    (pert_h2_perc.time.dt.year < yr+1),
                    drop=True
                )
                .mean('time')
            )


            axs[c,1].plot(annual_mean_pert,mean_pfull,color=color_list[model_id],alpha=0.3,linewidth=0.5,zorder=-10)



            annual_mean_pert_ch4 = (
                pert_ch4_perc[comp].where(
                    (pert_ch4_perc.time.dt.year >= yr) &
                    (pert_ch4_perc.time.dt.year < yr+1),
                    drop=True
                )
                .mean('time')
            )

            axs[c,2].plot(annual_mean_pert_ch4,mean_pfull,color=color_list[model_id],alpha=0.3,linewidth=0.5,zorder=-10)

            annual_mean_h2_total = (
                pert_h2_total_perc[comp].where(
                    (pert_h2_total_perc.time.dt.year >= yr) &
                    (pert_h2_total_perc.time.dt.year < yr+1),
                    drop=True
                )
                .mean('time')
            )

        
            axs[c,3].plot(annual_mean_h2_total,mean_pfull,color=color_list[model_id],alpha=0.3,linewidth=0.5,zorder=-10) 

        
        axs[c,0].plot(mean_comp,mean_pfull,color=color_list[model_id],label=model_names_out[model_id])
        axs[c,1].plot(mean_h2pert,mean_pfull,color=color_list[model_id],label=model_names_out[model_id])
        axs[c,2].plot(mean_ch4pert,mean_pfull,color=color_list[model_id],label=model_names_out[model_id])
        axs[c,3].plot(mean_h2totalpert,mean_pfull,color=color_list[model_id],label=model_names_out[model_id])
        
#axs[0,0].set_title('CNTR')
#axs[0,1].set_title('(H2PERT-CNTR)/CNTR [%]')
#axs[0,2].set_title('(CH4PERT-CNTR)/CNTR [%]')
#axs[0,3].set_title('(H2PERT+methane induced-CNTR)/CNTR [%]')

for c,comp in enumerate(variable_list):
    axs[c,0].set_xlabel(comp +' [mol/mol]')
    axs[c,0].invert_yaxis()

    if logplot == True:
        axs[c,0].set_yscale('log')
        axs[c,1].set_yscale('log')
        axs[c,2].set_yscale('log')
        axs[c,3].set_yscale('log')
        
    axs[c,1].set_xlabel('[%]')
    axs[c,1].invert_yaxis()
    #axs[c,1].legend()

    
    axs[c,2].set_xlabel('[%]')
    axs[c,2].invert_yaxis()
    #axs[c,2].legend()
 

    axs[c,3].set_xlabel('[%]')
    axs[c,3].invert_yaxis()
    #axs[c,3].legend()

    axs[c,0].set_ylim([1000,0.1])
    axs[c,1].set_ylim([1000,0.1])
    axs[c,2].set_ylim([1000,0.1])
    axs[c,3].set_ylim([1000,0.1])
    
    
    axs[c,0].set_title(' '+comp.upper(),y = 0.90,loc='left')
    axs[c,1].set_title(' '+comp.upper(),y = 0.90,loc='left')
    axs[c,2].set_title(' '+comp.upper(),y = 0.90,loc='left')
    axs[c,3].set_title(' '+comp.upper(),y = 0.90,loc='left')
    axs[c,0].set_ylabel('Pressure [hPa]')
    axs[c,1].set_ylabel('Pressure [hPa]')
    axs[c,2].set_ylabel('Pressure [hPa]')
    axs[c,3].set_ylabel('Pressure [hPa]')

axs[0,0].set_title('CNTR')
axs[0,1].set_title('(H2PERT-CNTR)/CNTR [%]')
axs[0,2].set_title('(CH4PERT-CNTR)/CNTR [%]')
axs[0,3].set_title('(H2PERT+methane induced-CNTR)/CNTR [%]')


axs[0,0].legend()



axs[2,0].set_xlim([0,0.00004])
plt.tight_layout()
plt.show()
exit()

                                   
        

