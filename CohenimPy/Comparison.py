# %%

# This program was made for comparing between scenario in the Staff Forcast
# can be reduced to the my other libarariys

#%%
import numpy as np
import subprocess
inkscapePath_go = r"C:/Program Files/Inkscape/bin/inkscape.exe"
import os
try: 
    os.makedirs('Figs_compare')
except OSError: 
    pass
import datetime
now = datetime.datetime.now() 
file_date = '_'+str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)
#import scipy
#from scipy.optimize import fsolve
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cbook as cbook
import matplotlib.dates as dates
import matplotlib.ticker as ticker
#import matplotlib.ticker as ticker
# set plot parameters
# %matplotlib inline
# plt.style.use('seaborn') # pretty matplotlib plots
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png', 'jpeg')
plt.rcParams['savefig.dpi'] = 75
#plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = 16, 9  # for ppt - wide screen 
plt.rcParams['figure.constrained_layout.use'] = True
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = "serif"
plt.rcParams['font.serif'] = "cm"
# plt.rcParams['text.latex.preamble'] = "\usepackage{subdepth}, \usepackage{type1cm}" 
#%%
colors = list(mcolors.BASE_COLORS)
#colors = list(mcolors.CSS4_COLORS)
style = [':', '--','-.', ':']
marker = ['', 'x', '+', '^']
#np.save('Results/scalars.npy', [ciss,inc_target,niss,uiss,urss,do_opt_policy], allow_pickle=True)

#File_to_comp = ['Tables_4_Baseline_11.5.20','Tables_6_Pasemistic_12.5.20']   # 'Tables_5_Pasemistic_11.5.20']
#File_to_comp = ['Tables_8_Baseline_18.5.20','Tables_4_Baseline_11.5.20','Tables_4_Baseline_5.4.20']   
File_to_comp = ['Tables_4_nothing','Tables_1_R_by_EtaR','Tables_3_DYnR_by_RP_FX_n_R'] 
File_History = ['C3_History']  
#labels = ['Baseline', 'Pessimistic']
labels = ['SS', 'IR policy','FX intervention policy (Constant R)']

#%% trends

#     df_trend = pd.read_excel('30.Cond_n_Simul/XLSX_and_more/'+File_History+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
# #    df_pi = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_inflations',header=3,index_col=0)    
    
#     ob_chng = ['OB_DY','OB_DPOP']
#     ob_levels = ['Output' ,'population']
#     for cng,level in zip(ob_chng,ob_levels):
#         df[level] = df[cng] * 0 + 100    
#         temp_level = 100
#         for idx, row in df.iterrows():        
#             row[level] = temp_level * (1+row[cng])
#             temp_level = row[level]
#             #print(idx, cng , row[cng], level, row[level]) 
#     ob_chng = ['OB_DU']
#     ob_pers = ['Unemployment']
#     for cng,pres in zip(ob_chng,ob_pers):
#         df[pres] = df[cng] * 0 + 100    
#         temp_level = 100
#         for idx, row in df.iterrows():        
#             row[pres] = temp_level +row[cng]
#             temp_level = row[pres]
#             #print(idx, cng , row[cng], level, row[level])
    
#     df_pi['PIE_H_4Q'] = df_pi['PIE_H'].rolling(window=4).sum()    # average 4 quarters!!
#     df_pi['PIE_IM_4Q'] = df_pi['PIE_IM'].rolling(window=4).sum()  # average 4 quarters!!
#     df_pi['PIE_C_4Q'] = df['OB_DP_CP'].rolling(window=4).sum()  # average 4 quarters!!
    
#%% Fig 1
start = 14  # 7 
history = 15
horz = 23 # 20
time = np.arange(start,horz, dtype=float)

fig,((ax1, ax2, ax3), (ax4,ax5, ax6)) = plt.subplots(2,3,constrained_layout=True)
#fig.suptitle('Figure 1: ', fontsize=30,fontweight='bold')

for index,Sim in enumerate(File_to_comp):
    df = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
    df_pi = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_inflations',header=3,index_col=0)    
    
    props = dict()
    props['alpha'] = 1 - 0.25 * index
    props['linestyle'] = style[index]
    props['linewidth'] = 2 - 0.5 * index
    props['color'] = colors[index]
    props['marker']= marker[index]
    props['label'] = labels[index]
    
    ob_chng = ['OB_DY','OB_DPOP']
    ob_levels = ['Output' ,'population']
    for cng,level in zip(ob_chng,ob_levels):
        df[level] = df[cng] * 0 + 100    
        temp_level = 100
        for idx, row in df.iterrows():        
            row[level] = temp_level * (1+row[cng])
            temp_level = row[level]
            #print(idx, cng , row[cng], level, row[level]) 
    ob_chng = ['OB_DU']
    ob_pers = ['Unemployment']
    for cng,pres in zip(ob_chng,ob_pers):
        df[pres] = df[cng] * 0 + 100    
        temp_level = 100
        for idx, row in df.iterrows():        
            row[pres] = temp_level +row[cng]
            temp_level = row[pres]
            #print(idx, cng , row[cng], level, row[level])
    
    df_pi['PIE_H_4Q'] = df_pi['PIE_H'].rolling(window=4).sum()    # average 4 quarters!!
    df_pi['PIE_IM_4Q'] = df_pi['PIE_IM'].rolling(window=4).sum()  # average 4 quarters!!
    df_pi['PIE_C_4Q'] = df['OB_DP_CP'].rolling(window=4).sum()  # average 4 quarters!!
    
    
#     nominal wage growth
# OB_DW

# Output deflator inflation
# OB_DP_YM

# The Change in hours worked (per capita)
# OB_DN

    
    tt =df.index.to_numpy()[start:horz] - np.timedelta64(80,'D')  #  to plot point not at the last day of quarter
    df['QUARTER'] = pd.PeriodIndex(df.index, freq='Q')
   
    #ax1.plot(tt,df['Output'].iloc[0:horz]+df['population'].iloc[0:horz],**props)
    ax1.plot(tt,df['Output'].iloc[start:horz],**props)
    #df.plot(x='QUARTER',y='Output',ax=ax1,**props)
    ax1.set(xlabel='', ylabel='level',title='GDP (per capita, index)')
    ax1.set_ylim(bottom=102,top=106)
    ax1.legend()
    # ax2.plot(tt,100*df['OB_DY'].iloc[0:horz],**props)
    # ax2.set(xlabel='',ylabel='\%',title='Growth (per capita)')
    
    ax2.plot(tt,100*(0.0379 + df['Unemployment'].iloc[start:horz]-100),**props)
    ax2.set(xlabel='', ylabel='\%',title='Unemployment rate (index)')
    ax2.set_ylim(bottom=3.5,top=3.9)
    
    ax3.plot(tt,100*df['OB_DS'].iloc[start:horz],**props)
    ax3.set(xlabel='', ylabel='\%',title='Nominal Depreciation (change)')    
    #ax3.axis('off')
    
    
    ax4.plot(tt,100*df['OB_R'].iloc[start:horz], **props)       
    ax4.set(xlabel='',ylabel='\%',title='BoI Interest Rate')    

    ax5.plot(tt,100*df['OB_DP_CP_YOY'].iloc[start:horz],**props)
    #ax5.plot(tt,100*df_pi['PIE_C_4Q'].iloc[start:horz],'.',marker = 'x' ,color= colors[index])
    # ax5.plot(tt,2+100*df_pi['PIE_H_4Q'].iloc[start:horz],'-.',color= colors[index],lw=0.5,label=r'$\pi^{Local}$')
    # ax5.plot(tt,2+100*df_pi['PIE_IM_4Q'].iloc[start:horz],':',color= colors[index],lw=0.3,label=r'$\pi^{Imported}$')
    ax5.set(xlabel='', ylabel='\%',title='Inflation (4 Quarters)')
    #ax5.legend(loc='lower left')

    ax6.plot(tt,100*df['OB_RI'].iloc[start:horz], **props)       
    ax6.set(xlabel='',ylabel='\%',title='Real interest rate (anualized)')  
    
    for ax in [ax1, ax2, ax3, ax4,ax5, ax6]:        
        ax.axvspan(tt[0],tt[history - start], facecolor='lightgray', alpha=0.5)
        ax.axhline(c='grey', lw=1)        
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
#    fig.autofmt_xdate(rotation=45)    
    
    # rotate and align the tick labels so they look better
    #fig.autofmt_xdate()       
    # fig.canvas.get_supported_filetypes()
   
multi_save(name = 'Figs_compare/comp_YURPS'+file_date)    

#%% Inflation
fig,ax1 = plt.subplots(1,1,constrained_layout=True)
#fig.suptitle('Figure 1: ', fontsize=30,fontweight='bold')

for index,Sim in enumerate(File_to_comp):
    df = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
    df_pi = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_inflations',header=3,index_col=0)    
    
    props = dict()
    props['alpha'] = 1 - 0.25 * index
    props['linestyle'] = style[index]
    props['linewidth'] = 3 - 0.5 * index
    props['color'] = colors[index]
    props['label'] = labels[index]
    
    period = 4
    df_pi['PIE_H_4Q'] = df_pi['PIE_H'].rolling(window=period).sum()    # average 4 quarters!!
    df_pi['PIE_IM_4Q'] = df_pi['PIE_IM'].rolling(window=period).sum()  # average 4 quarters!!
    df_pi['PIE_C_4Q'] = df['OB_DP_CP'].rolling(window=period).sum()  # average 4 quarters!!
   
#     nominal wage growth  OB_DW
#  Output deflator inflation OB_DP_YM
# The Change in hours worked (per capita)  OB_DN
    
    tt =df.index.to_numpy()[start:horz] - np.timedelta64(80,'D')  #  to plot point not at the last day of quarter
    df['QUARTER'] = pd.PeriodIndex(df.index, freq='Q')

    #ax1.plot(tt,100*df['OB_DP_CP_YOY'].iloc[0:horz],**props)
    ax1.plot(tt,100*df_pi['PIE_C_4Q'].iloc[start:horz],'-',marker = 'x' ,color= colors[index])
    ax1.plot(tt,2+100*df_pi['PIE_H_4Q'].iloc[start:horz],'-.',color= colors[index],lw=1,label=r'$\pi^{Local}$')
    ax1.plot(tt,2+100*df_pi['PIE_IM_4Q'].iloc[start:horz],':',color= colors[index],lw=1,label=r'$\pi^{Imported}$')
    ax1.set(xlabel='', ylabel='\%',title='Inflation (4 Quarters)')
    ax1.legend(loc='lower left')

    for ax in [ax1]:        
        ax.axvspan(tt[0],tt[history-start], facecolor='lightgray', alpha=0.5)
        ax.axhline(c='grey', lw=1)
    
    # rotate and align the tick labels so they look better
    #fig.autofmt_xdate()         
multi_save(name = 'Figs_compare/comp_Pi'+file_date)    
#%% Levels  National Acuunts

fig,((ax1, ax2, ax3), (ax4,ax5, ax6)) = plt.subplots(2,3,constrained_layout=True)
#fig.suptitle('Figure 1: ', fontsize=30,fontweight='bold')

for index,Sim in enumerate(File_to_comp):
    df = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
    
    props = dict()
    props['alpha'] = 1 - 0.25 * index
    props['linestyle'] = style[index]
    props['linewidth'] = 2 - 0.5 * index
    props['color'] = colors[index]
    props['marker']= marker[index]
    props['label'] = labels[index]
    
    tt =df.index.to_numpy()[start:horz]
  
    
    ob_chng = ['OB_DY','OB_DC','OB_DI_NI','OB_DG','OB_DX','OB_DIM']
    ob_levels = ['Output' ,'Consumption','Investment','Government','Export','Import']
    for cng,level in zip(ob_chng,ob_levels):
        df[level] = df[cng] * 0 + 100    
        temp_level = 100
        for idx, row in df.iterrows():        
            row[level] = temp_level * (1+row[cng])
            temp_level = row[level]
            #print(idx, cng , row[cng], level, row[level])
            
            
    ax1.plot(tt,df['Output'].iloc[start:horz], **props)       
    ax1.set(xlabel='',ylabel='\%',title='Output')    
    #ax1.legend(loc='upper right')  
    ax1.legend()
    ax2.plot(tt,(df['Consumption'].iloc[start:horz]),**props)
    ax2.set(xlabel='', ylabel='\%',title='Consumption')
    ax3.plot(tt,df['Investment'].iloc[start:horz],**props)
    ax3.set(xlabel='', ylabel='\%',title='Investment')
    ax4.plot(tt,df['Government'].iloc[start:horz],**props)
    ax4.set(xlabel='', ylabel='\%',title='Government')
    ax5.plot(tt,df['Export'].iloc[start:horz],**props)
    ax5.set(xlabel='', ylabel='\%',title='Export')    
    ax6.plot(tt,df['Import'].iloc[start:horz],**props)
    ax6.set(xlabel='',ylabel='\%',title='Import')
    for ax in [ax1, ax2, ax3,ax4,ax5, ax6]:
        ax.axvspan(tt[0],tt[history - start], facecolor='lightgray', alpha=0.5)
        ax.axhline(c='grey', lw=1)
        ax.set_ylim(bottom=100,top=106)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

multi_save(name = 'Figs_compare/comp_NA_'+file_date)    
#%% Output 
fig, (ax1)  = plt.subplots(1,1,constrained_layout=True)
#fig.suptitle('Figure 1: ', fontsize=30,fontweight='bold')

for index,Sim in enumerate(File_to_comp):
    df = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
    
    props = dict()
    props['alpha'] = 1 - 0.25 * index
    props['linestyle'] = style[index]
    props['linewidth'] = 2 - 0.5 * index
    props['color'] = colors[index]
    props['marker']= marker[index]
    props['label'] = labels[index]
    
    tt =df.index.to_numpy()[start:horz]
  
    
    ob_chng = ['OB_DY','OB_DC','OB_DI_NI','OB_DG','OB_DX','OB_DIM']
    ob_levels = ['Output' ,'Consumption','Investment','Government','Export','Import']
    for cng,level in zip(ob_chng,ob_levels):
        df[level] = df[cng] * 0 + 100    
        temp_level = 100
        for idx, row in df.iterrows():        
            row[level] = temp_level * (1+row[cng])
            temp_level = row[level]
            #print(idx, cng , row[cng], level, row[level])
            
            
    ax1.plot(tt,df['Output'].iloc[start:horz], **props)       
    ax1.set(xlabel='',ylabel='\%',title='Output')    
    #ax1.legend(loc='upper right')  
    ax1.legend()
    
    
#%% consumption, Investment

fig,((ax1, ax2), (ax3,ax4) ,(ax5, ax6)) = plt.subplots(3,2,constrained_layout=True)

#fig.suptitle('Figure 1: ', fontsize=30,fontweight='bold')

for index,Sim in enumerate(File_to_comp):
    df = pd.read_excel('Outputs/'+File_to_comp[index]+'.xlsx',sheet_name='TB_for_Summary',header=3,index_col=0)    
    
    props = dict()
    props['alpha'] = 1 - 0.25 * index
    props['linestyle'] = style[index]
    props['linewidth'] = 2 - 0.5 * index
    props['color'] = colors[index]
    props['marker']= marker[index]
    props['label'] = labels[index]
    
    tt =df.index.to_numpy()[start:horz]
          
    ax1.plot(tt,100*df['C'].iloc[start:horz], **props)       
    ax1.set(xlabel='',ylabel='\%',title='Consumption')    
    #ax1.legend(loc='upper right')  
    ax1.legend()
    
    ax2.plot(tt,100*df['I'].iloc[start:horz], **props)       
    ax2.set(xlabel='',ylabel='\%',title='Investment')    
    
    ax3.plot(tt,100*df['H_C'].iloc[start:horz], **props)       
    ax3.set(xlabel='',ylabel='\%',title='Demand for domestic intermediate goods- Consumption')    
    
    ax4.plot(tt,100*df['H_I'].iloc[start:horz], **props)       
    ax4.set(xlabel='',ylabel='\%',title='Demand for domestic intermediate goods -Investment')    
    
    ax5.plot(tt,100*df['IM_C'].iloc[start:horz], **props)       
    ax5.set(xlabel='',ylabel='\%',title='Demand for imported intermediate goods -Consumption')    
    
    ax6.plot(tt,100*df['IM_I'].iloc[start:horz], **props)       
    ax6.set(xlabel='',ylabel='\%',title='Demand for imported intermediate goods -Investment')    
    
    
    for ax in [ax1]:
        ax.axvspan(tt[0],tt[history - start], facecolor='lightgray', alpha=0.5)
        ax.axhline(c='grey', lw=1)
        #ax.set_ylim(bottom=85)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')


#trend 1.5 ?         
# ax1.plot(tt,df['Output'].iloc[start:horz],'r-')       
# ax1.set(xlabel='',ylabel='\%',title='Output')    

multi_save(name = 'Figs_compare/comp_CandI_HvsIM'+file_date)    