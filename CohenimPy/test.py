# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %% [markdown]
# # Israel Credit Market  - Basic Ampirics 
# November 2020
# 
# This Notebook get the Data from BoI FAME system (van Excel).
# 
# Then we show
# 
# * National Accounts
# * Credit amounts
# * Calculate leverage ratios
# * Intrest Rates

# %%
## Using Jupter and Spyder\Atom Together
## https://medium.com/@rrfd/cookiecutter-data-science-organize-your-projects-atom-and-jupyter-2be7862f487e
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
get_ipython().run_line_magic('matplotlib', 'inline')


# %%
# my functions and oter iports
import config
from config import my_pd as pd
from config import my_plt as plt
from config import my_colors as colors
file_date = config.file_date
import ncDate
from ncDate import period
import ncPlot
import ncStat
from ncPlot import multi_save, add_Rec, plot1ax, plot2axs  
from ncStat import ols_fit,regs_plot

# very importent - get Project Main Path
project_path = config.project_path
current_NB_path = 'src/data/'
import os
os.chdir(project_path)


# %%
import numpy as np
#import seaborn as sns  # Machin Learning module

import statsmodels as st
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose


# %%
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')


# %%
# get US data for benchmarking:
import src.data.read_from_Fred as fred
path='data/processed/'
df_US   = fred.Get_data(path)

# %% [markdown]
# ### Loading the data and make first impration about it
#  __VERY IMPORTENT__ : Pataya \ FAME excel file have hiden sheet (this is real SHEET)!!!
# so always Check in Excel under File menu, "Check if there are problems" and "check Doc"
# so we must use sheet_name=1 __or__ use explicit sheet name
# %% [markdown]
# ##  A. Israe National Accounts

# %%
path = 'data/raw/Pataya_Activity/'
file_name = 'Fame_NationalAccount.xlsx'
nrows=8
df_NA_info = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,nrows=nrows)
#df_NA_info


# %%
nrows=8
df_NA = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=nrows)
df_NA.index.name = 'date'
#df_NA


# %%
lamb = 1600
used_col = ['GDP.Q_N', 'C.Q_N' , 'I.Q_N'  ]
for col in used_col:
    df_NA[col+'_MA'] = df_NA[col].rolling(window=4).mean()
    df_NA[col+'_SA'] = seasonal_decompose(df_NA[col].dropna(), model='additive').trend
    df_NA[col+'_HP_cycle'], df_NA[col+'_HP_trend'] = sm.tsa.filters.hpfilter(df_NA[[col]].dropna(), lamb=lamb)
    
    mask = period(df_NA.index,start='2013-01-01')
    ax= plot1ax(columns=[col,col+'_MA',col+'_HP_trend',col+'_SA'], df=df_NA[mask],markers='',xlabel='',logy=True)
    add_Rec(ax,df_US,'ISRRECM')
    plt.show()

# %% [markdown]
# ## B. All Debt by Segmentation

# %%
#pataya_Debt_total
path = 'data/raw/Pataya_Credit/' 
file_name = 'All_Credit_Segmentation.xlsx'
nrows=7
df_CreditSeg_info = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,nrows=nrows)
#df_CreditSeg_info


# %%
df_CreditSeg = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=7)
#alternative: pd.read_excel(file_path_name,sheet_name=1,index_col=0,header=0,skiprows=list(range(1,8)))
df_CreditSeg.index.name = 'date'
new_columns = [col.split('.')[0] for col in df_CreditSeg.columns]
df_CreditSeg.columns = new_columns

# %% [markdown]
#  **Bug** fixed : debt_households_nonhousing_total.m is wrong until ~1999 
# 

# %%
correct_values = df_CreditSeg['debt_hh_housing_debt'].dropna()
df_CreditSeg['debt_households_nonhousing_total'] = df_CreditSeg.loc[correct_values.index,['debt_households_nonhousing_total']]


# %%
df_CreditSeg['debt_total'] = df_CreditSeg['debt_business_sector']+df_CreditSeg['debt_households']


# %%
# Combine National Acount and Debt
df_Amount = pd.merge(df_NA,df_CreditSeg,how='inner',left_index=True,right_index = True)
#df_Amount

# %% [markdown]
# ### Calculation of Debt to GDP ratios
# $$ DoY_t = B_t / \sum_{\tau=t-4}^{t}Y_\tau $$
# 
# 

# %%
df_Amount['DoY_total'] = 1000 * df_Amount['debt_total'] / (4 * df_Amount['GDP.Q_N_MA'])
df_Amount['DoY_business_sector'] = 1000 * df_Amount['debt_business_sector'] / (4 * df_Amount['GDP.Q_N_MA'])
df_Amount['DoY_households'] = 1000 * df_Amount['debt_households'] / (4 * df_Amount['GDP.Q_N_MA'])
df_Amount['DoY_households_nonhousing_total'] = 1000 * df_Amount['debt_households_nonhousing_total'] / (4 * df_Amount['GDP.Q_N_MA'])
df_Amount['DoY_hh_housing_debt'] = 1000 * df_Amount['debt_hh_housing_debt'] / (4 * df_Amount['GDP.Q_N_MA'])
#df_Amount['DoY prox'] = 100*1000 * df_Amount['debt_households_nonhousing_total'] /(df_Amount['Consumption SA'] + df_Amount['Investments SA'])
#df_Amount['DoY YoY'] = df_Amount['DoY MA'].pct_change(periods=4)


# %%
title='Debt for Business vs HH\'s (housing vs nonhousing)'
sel_Debt = ['debt_business_sector','debt_households',
          'debt_households_nonhousing_total', 'debt_hh_housing_debt']
ax= plot1ax(columns=sel_Debt,ylabel='Debt',df=df_Amount,markers='',xlabel='',title=title)
add_Rec(ax,df_US,'ISRRECM');    


# %%
title='Leverage (DoY) for Business vs HH\'s (housing vs nonhousing)'
sel_DoY = ['DoY_total','DoY_business_sector','DoY_households',
          'DoY_households_nonhousing_total','DoY_hh_housing_debt']
ax= plot1ax(columns=sel_DoY,ylabel='DoY',df=df_Amount,markers='',xlabel='',title=title,bbox=(1., 0.9))
add_Rec(ax,df_US,'ISRRECM');    


# %%
sel_debt_HH = ['debt_households_nonhousing_total','debt_hh_housing_debt']
title='HH Debt (housing vs nonhousing)'
ax = df_Amount[sel_debt_HH].plot.area()
plot1ax(ax=ax,columns=['debt_households'],ylabel='DoY',df=df_Amount,markers='',xlabel='',title=title,linewidth=5)
add_Rec(ax,df_US,'ISRRECM');


# %%
select_debt_HH = ['DoY_households_nonhousing_total',
                  'DoY_hh_housing_debt']
ax2 = df_Amount[['DoY_households']].plot(linewidth=5)
df_Amount[select_debt_HH].plot.area(ax=ax2)
ax2.set_title('DoY housing vs nonhousing')
add_Rec(ax2,df_US,'ISRRECM');


# %%
debt_HH_indexation = ['debt_households_fx_inedxed',
                      'debt_households_cpi_inedxed',
                      'debt_households_uninedxed']
ax = df_CreditSeg[['debt_households']].plot(linewidth=5)
df_CreditSeg[debt_HH_indexation].plot.area(ax=ax,figsize=(16/2,9/2))
ax.set_title('HH Debt by indexation')
add_Rec(ax,df_US,'ISRRECM');


# %%
debt_HH_toBanks = ['debt_households_to_banks_nonhousing',
                   'debt_hh_housing_loans_to_banks']
ax = df_CreditSeg[['debt_households']].plot(linewidth=3)
df_CreditSeg[['debt_households_to_banks']].plot(ax=ax,linewidth=5)
df_CreditSeg[debt_HH_toBanks].plot.area(ax=ax,figsize=(16/2,9/2))
ax.set_title('HH Debt to Banks (housing vs nonhousing)')
add_Rec(ax,df_US,'ISRRECM');


# %%
debt_HH_toBanks = ['debt_households_to_banks_nonhousing',
                   'debt_hh_housing_loans_to_banks',
                   'debt_households_to_banks_current_accounts']
ax = df_CreditSeg[['debt_households_to_banks']].plot(linewidth=5)
df_CreditSeg[debt_HH_toBanks].plot(ax=ax,figsize=(16/2,9/2))
ax.set_title('HH Debt to Banks (housing vs nonhousing and overdraft)')
add_Rec(ax,df_US,'ISRRECM');


# %%
debt_business_indexation = ['debt_business_sector_cpi_inedxed',
                            'debt_business_sector_fx_inedxed',
                            'debt_business_sector_uninedxed']
ax = df_CreditSeg[['debt_business_sector']].plot(linewidth=5)
df_CreditSeg[debt_business_indexation].plot.area(ax=ax,figsize=(16/2,9/2))
ax.set_title('Business Debt by indexation')
add_Rec(ax,df_US,'ISRRECM');


# %%
select_debt_business = ['debt_business_sector_to_banks_total',
                        'total_debt_busniness_from_nonres',
                        'debt_business_loans_from_abroad',
                        'total_debt_busniness_from_households']
ax = df_CreditSeg[['debt_business_sector']].plot(linewidth=5)
df_CreditSeg[select_debt_business].plot(ax=ax,figsize=(16/2,9/2))
ax.set_title('Business Debt to Banks')
add_Rec(ax,df_US,'ISRRECM');

# %% [markdown]
# ## C. Bank Credit Detailed

# %%
path = 'data/raw/Pataya_Credit/' 
file_name = 'Banks_Credit_Detaeild.xlsx'
nrows=7


# %%
df_BanksCredit_info = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,nrows=nrows)
#df_BanksCredit_info


# %%
#df_BanksCredit_info[['אשראי-לא צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-סכום',
#                    'אשראי-צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-סכום']]


# %%
df = df_BanksCredit_info.transpose()
df=df.reset_index()
df=df.rename(columns={"index": "Description"})
df=df.set_index('FAMEDATE')


# %%
get_cols = ['s285801.m_99010','s285802.m_99010','s285800.m_99010','s285744.m_99010',
            's285745.m_99010','s286241.m_99010','s286240.m_99010','s286631.m_99010','s286630.m_99010']
get_cols_short = [el.split('.')[0] for el in get_cols]
df_interesting_col = df.loc[get_cols,['Description']]
interesting_col = list(df_interesting_col['Description'])
#interesting_col


# %%
#- s285801: הריבית על אשראי חדש שניתן למשקי בית (ללא הלוואות לדיור וללא בנקאות פרטית) במגזר השקלי הלא צמוד
#- s285802: תקופת פירעון סופי של אשראי חדש במגזר השקלי הלא צמוד, משקי בית (ללא הלוואות לדיור וללא בנקאות פרטית) (שנים)
#- s285800: האשראי שניתן במגזר השקלי הלא צמוד למשקי בית (ללא הלוואות לדיור) (מיליארדי ש"ח)
#- s285744: שיעור הריבית של אשראי חדש שניתן למשקי בית (ללא הלוואות לדיור וללא בנקאות פרטית)- הלוואות עד 3 חודשים, לא צמודות בריבית קבועה
#- s285745 :תקופת פירעון סופי של אשראי חדש שניתן למשקי בית (ללא הלוואות לדיור וללא בנקאות פרטית)- הלוואות עד 3 חודשים, לא צמודות בריבית קבועה (שנים)
#- s286241: "הריבית על אשראי חדש שניתן למשקי בית (ללא הלוואות לדיור) במגזר צמוד מדד"
#- s286240: האשראי שניתן במגזר צמוד מדד למשקי בית (ללא הלוואות לדיור) (מיליוני ש"ח)
#- s286631: "הריבית על אשראי חדש שניתן למשקי בית (ללא הלוואות לדיור) במגזר צמוד ונקוב מט""ח"
#- s286630: האשראי שניתן במגזר צמוד ונקוב מט"ח למשקי בית (ללא הלוואות לדיור) (מיליארדי ש"ח)
#- s285800 + s286240 + s286630 : האשראי החדש שניתן למשקי בית שלא לדיור, בכל סוגי ההצמדה (מיליארדי ש"ח)                                                 


# %%
# Get Bank Credit Data
df_BanksCredit = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,skiprows=list(range(1,8)))
df_BanksCredit.index.name = 'date'
#df_BanksCredit.head(5)


# %%
df_BanksCredit['HH_NoHousing_uninedxed_IR'] = df_BanksCredit['אשראי-לא צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-שיעור הריבית']
df_BanksCredit['HH_NoHousing_uninedxed_Maturity'] = df_BanksCredit['אשראי-לא צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-תקופת פירעון סופית']
df_BanksCredit['HH_NoHousing_uninedxed_Debt'] = df_BanksCredit['אשראי-לא צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-סכום']
df_BanksCredit['HH_VeryShort_uninedxed_IR'] = df_BanksCredit['אשראי-לא צמוד-משקי בית-עד 3 חודשים-ריבית קבועה-שיעור הריבית']
df_BanksCredit['HH_VeryShort_uninedxed_Maturity'] = df_BanksCredit['אשראי-לא צמוד-משקי בית-עד 3 חודשים-ריבית קבועה-תקופת פירעון סופית']
df_BanksCredit['HH_NoHousing_inedxed_IR'] = df_BanksCredit['אשראי-צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-שיעור הריבית']
df_BanksCredit['HH_NoHousing_inedxed_Debt'] = df_BanksCredit['אשראי-צמוד-משקי בית-סה"כ משקי בית (ללא הלוואות לדיור)-סה"כ-סכום']
df_BanksCredit['HH_NoHousing_FXinedxed_IR'] = df_BanksCredit['אשראי-צמוד מט"ח-משקי בית-סה"כ משקי בית (ללא הלוואות בדיור)-סה"כ-שיעור הריבית']
df_BanksCredit['HH_NoHousing_FXinedxed_Debt'] = df_BanksCredit['אשראי-צמוד מט"ח-משקי בית-סה"כ משקי בית (ללא הלוואות בדיור)-סה"כ-סכום']


# %%
cols_IR = ['HH_NoHousing_uninedxed_IR','HH_VeryShort_uninedxed_IR',
          'HH_NoHousing_inedxed_IR','HH_NoHousing_FXinedxed_IR']
cols_Credit = ['HH_NoHousing_uninedxed_Debt','HH_NoHousing_inedxed_Debt','HH_NoHousing_FXinedxed_Debt']         
cols_Maturity = ['HH_NoHousing_uninedxed_Maturity','HH_VeryShort_uninedxed_Maturity']


# %%
ax1 = df_BanksCredit[cols_IR].dropna().plot()
ax2 = df_BanksCredit[cols_Credit].dropna().plot()
ax2 = df_BanksCredit[cols_Maturity].dropna().plot()

# %% [markdown]
# ## D. Intrest Rates

# %%
path = 'data/raw/Pataya_Credit/' 
file_name = 'Monetary_FinMarket_n_Rates.xlsx'
nrows=7
df_IRs_info = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,nrows=nrows)
#df_IRs_info


# %%
df_IRs = pd.read_excel(path+file_name,sheet_name='גיליון1',index_col=0,header=0,skiprows=list(range(1,8)))
df_IRs.index.name = 'date'
#df_IRs


# %%
col_dict =  {'עו"ש וחח"ד ביתרת חובה':'Overdraft IR',
             'ריבית משוקללת על אשראי למשקי בית שלא לדיור, לעסקים זעירים וקטנים – מט"י לא צמוד – בריבית קבועה – עד 3 חודשים':'HH 3m IR',
             'ריבית בנק ישראל - ממוצע חודשי':'BoI IR',
             'ריבית בנק ישראל (אפקטיבית) - ממוצע חודשי':'BoI IR 2',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - צמוד מדד - ריבית קבועה ':'Mortgage fixed real rate',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - צמוד מדד - ריבית משתנה ':'Mortgage floating real rate',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - לא צמוד - ריבית קבועה':'Mortgage fixed nominal rate',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - לא צמוד - ריבית משתנה ':'Mortgage floating nominal rate',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - מט"ח וצמוד מט"ח - ריבית קבועה':'Mortgage fixed foreign rate',
             'שיעור ריבית על אשראי שניתן למטרת מגורים - מט"ח וצמוד מט"ח - ריבית משתנה ':'Mortgage floating foreign rate',
             'תשואה נומינלית מעקום אפס לשנה':'nominal 1Y rate',
             'תשואה נומינלית מעקום אפס לשנתיים':'nominal 2Y rate'
            }
df_IRs.rename(columns = col_dict, inplace=True)

df_IRs['Spread Mortgage'] = df_IRs['Mortgage floating nominal rate'] - df_IRs['BoI IR']
df_IRs['Spread 3m HH'] = df_IRs['HH 3m IR'] - df_IRs['BoI IR']
df_IRs['Spread Overdraft'] = df_IRs['Overdraft IR'] - df_IRs['BoI IR']
df_IRs['Borrowers IR (BER model)'] = df_IRs['Spread Overdraft']                                         - df_IRs['Spread Overdraft'].mean()                                         + df_IRs['BoI IR']
selected = ['Overdraft IR', 'HH 3m IR', 'BoI IR', 'BoI IR 2','Mortgage floating nominal rate',
            'Spread Mortgage','Spread 3m HH','Spread Overdraft','Borrowers IR (BER model)']
for col in selected:
    df_IRs[col+' Quarterly'] = df_IRs[col].rolling(window=3,center=True).mean()


# %%
df_ISR = pd.merge(df_Amount,df_IRs,how='inner',left_index=True, right_index=True)
df_ISR['const'] = 1


# %%
toPlot = ['Overdraft IR Quarterly','Borrowers IR (BER model) Quarterly','BoI IR Quarterly','HH 3m IR Quarterly']
mask = period(df_ISR.index,start='1995-01-01')
ax = df_ISR.loc[mask,toPlot].plot()
add_Rec(ax,df_US,'ISRRECM');


# %%
Israel_Spread = ['Spread Mortgage Quarterly','Spread 3m HH Quarterly', 'Spread Overdraft Quarterly']
mask = period(df_ISR.index,start='1994-01-01')
ax = df_ISR.loc[mask,Israel_Spread].plot()
df_US['spread CC Accounts Assessed'].dropna().plot(ax=ax,label='US: spread CC Accounts Assessed',linestyle='--')
plt.title('IR Spreads for HH debt (ISR vs US)')
add_Rec(ax,df_US,'ISRRECM')
plt.legend(bbox_to_anchor=(1, -0.12));


# %%
mask = period(df_ISR.index,start='1994-01-01')
ax=df_ISR.loc[mask,['Spread Overdraft Quarterly']].plot()
add_Rec(ax,df_US,'ISRRECM');


# %%
fig, (ax1,ax2) = plt.subplots(nrows=1, ncols=2)
df_ISR.loc[mask,Israel_Spread].mean().plot(marker = 'x',ax=ax1)
ax1.set(title='Spread (mean)')
df_ISR.loc[mask,Israel_Spread].std().plot.bar(stacked=True,ax=ax2)
ax2.set(title='standard daviations');


# %%
#with plt.xkcd():
if True:
    col1=['Spread Overdraft Quarterly']
    col2=['DoY_households_nonhousing_total']
    start = str(df_ISR[col1].dropna().index[0].date())    
    end = str(df_ISR[col1].dropna().index[-1].date())    
    #mask = period(df_ISR.index,start=start)#start = '2015-02-01'

    ax1 = plot1ax(columns=col1,ylabel ='% Spread ' , df=df_ISR[col1+col2])    
    #add_Rec(ax1,df_US,'ISRRECM')
    #ax2.set_title('Israel \n (period: '+start+' to '+end+')')    
    #ax2.axvline(x='2009-03-31' ,linewidth=4, color=colors[2],linestyle=':',alpha=0.5)
    #ax2.axvline(x='2015-03-31' ,linewidth=4, color=colors[2],linestyle=':',alpha=0.5)


# %%
#with plt.xkcd():
if True:
    col1=['Spread Overdraft Quarterly']
    col2=['DoY_households_nonhousing_total']
    start = str(df_ISR[col1].dropna().index[0].date())    
    end = str(df_ISR[col1].dropna().index[-1].date())    
    mask = period(df_ISR.index,start=start,end=end)#start = '2015-02-01'

    ax1,ax2 = plot2axs(columns1=col1,columns2=col2,
                       ylabel1 ='% Spread', ylabel2='Leverage (Debt Over GDP)',
                       df=df_ISR.loc[mask,col1+col2],
                       markers='',colors=colors,linestyles=['-','--'])
                       #bbox1=(0.4, -0.12),bbox2=(1.1, -0.12))    
    add_Rec(ax1,df_US,'ISRRECM')
    ax2.set_title('Israel \n (period: '+start+' to '+end+')')    
    ax2.axvline(x='2009-03-31' ,linewidth=4, color=colors[2],linestyle=':',alpha=0.5)
    ax2.axvline(x='2015-03-31' ,linewidth=4, color=colors[2],linestyle=':',alpha=0.5)


# %%
ncPlot.path_in2D(columnX =colX[0], columnY=colY[0], df=df_ISR);

# %% [markdown]
# ### Export Files

# %%
toExport = ['GDP','GDP SA','debt_households_nonhousing_total',
                        'HH Debt to GDP','HH Debt to prox GDP','HH Debt to Consumption',
                        'Overdraft IR Quarterly','BoI IR Quarterly',
                        'Spread Overdraft Quarterly','Borrowers IR (BER model) Quarterly']


# %%
path = 'data/processed/' 
df_ISR.to_csv(path+'ISR_data.csv')
df_BanksCredit.to_csv(path+'ISR_Banks_data.csv')


# %%
os.chdir(current_NB_path)
###################################################
### IMPORTENT : update Notebook file_name below ###
###################################################
## Print Notebook wo code (inputs)
get_ipython().system('jupyter nbconvert 2.0-c-ISR_data_exploreation.ipynb --no-input --no-prompt --to pdf')

# to try also https://ipypublish.readthedocs.io/en/latest/ : 
# !nbpublish -f latex_ipypublish_all -pdf file_name.ipynb
# also sphinx and jupinx and more....
os.chdir(project_path)


# %%



