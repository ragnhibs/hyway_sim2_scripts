import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os

#Experiment and simulation infor:
table_id = 'monthly'
project_id = 'hyway'


experiment_id_list = ['h2pert','ch4pert']

linestylelist = {'cntr':'-',
                 'h2pert':'--',
                 'ch4pert':':'}



member_id_list =  {'OsloCTM3v1-2':'r2',
                   'EC-Earth3-AerChem':'r1',
                   'EMAC-DLR':'r1',
                   'LMDZ-INCA':'r1',
                   'CESM2-v212':'r1',
                   'GFDL-ESM4-c1':'r1',
                   'UKESM1-0-LL':'r2'}


logplot = False




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
                 'mmrso4']


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
              'NorESM2-LM-C'   : '#000000',  # black
}
#color_list =  {'OsloCTM3v1-2':'darkred',
#               'CESM2-v212':'forestgreen',
#               'EC-Earth3-AerChem':'blue',
#               'LMDZ-INCA':'orange',
#               'EMAC-DLR':'magenta',
#               'UKESM1-0-LL':'purple',
#               'GFDL-ESM4-c1':'lightgreen',
#               'NorESM2-LM-C':'yellow'}


year_period_list = {'EMAC-DLR':[2029,2031],
                    #'NorESM2-LM-C':[0,0],
                    'LMDZ-INCA':[2005,2010],
                    'OsloCTM3v1-2':[2038,2039],
                    'CESM2-v212':[2055,2075],
                    'UKESM1-0-LL':[2000,2005],
                    'GFDL-ESM4-c1':[40,60],
                    'UKESM1-0-LL':[1998,1999],
                    'EC-Earth3-AerChem':[2024,2030]}

fig, axs = plt.subplots(nrows=4,ncols=6,squeeze=True,figsize=(24,15),sharey=False)
axs=axs.flatten()


for var,variable_id in enumerate(variable_list):
    ax = axs[var*2]
    ax2= axs[var*2+1]
    
    for model_id in model_list:
        
        member_id = member_id_list[model_id]
        year_period = year_period_list[model_id]

        
        experiment_id = 'cntr'
        filename = 'results_csv/vertical_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv'
      
        if os.path.exists(filename):
            #print(filename)
            field_vert = pd.read_csv(filename,index_col=0)

            ax.plot(field_vert.values,field_vert.index,color=color_list[model_id],label=model_id)
         
        else:
            print('Not generated: ' + filename)
            


        for experiment_id in experiment_id_list:
            filename = 'results_csv/vertical_'+variable_id+'_'+table_id+'_'+model_id+'_'+member_id+'_'+project_id + '_' +experiment_id + '.csv'
      

            if os.path.exists(filename):
                #print(filename)
                
                field_vert_pert = pd.read_csv(filename,index_col=0)
                

                ax2.plot(field_vert_pert.values- field_vert.values,field_vert.index,color=color_list[model_id],linestyle=linestylelist[experiment_id]) #,label=model_id)
    
            



            
            else:
                print('Not generated: ' + filename)
            

    ax.set_ylim(0.1,1000)
    #plt.xlim([0,0.2])
    #plt.xlim([0,1000000])
    ax.legend(fontsize=8)
    ax.invert_yaxis()
    if logplot:
         ax.set_yscale('log')
    ax.set_title('cntr: '+ variable_id)


    ax2.set_ylim(0.1,1000)
    #plt.xlim([0,0.2])
    #plt.xlim([0,1000000])
    #ax2.legend()
    ax2.invert_yaxis()
    if logplot:
        ax2.set_yscale('log')
        
    ax2.set_title('Delta: '+ variable_id)


    ax2.axvline(0,color='darkgray',linestyle='--')



plt.show()
