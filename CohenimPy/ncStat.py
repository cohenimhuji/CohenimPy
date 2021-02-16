# -*- coding: utf-8 -*-
# Nimrod Cohen, November 2020
# %% code_folding=[]
# my functions and oter iports
import src.config as config
from src.config import my_pd as pd
from src.config import my_plt as plt

import numpy as np
import statsmodels.api as sm


# %%
def col_that(name_str,columns):
    return [col for col in columns if name_str in col]
# %%
def YoY(name ,df ,ahead=0, calc_type='Level'):
    '''
    take quarterly data (as GDP) and calculate Year on Year change
    
    name: a variable in *quartertly* amount and freqency, like Qyarterly GDP

    ahead: number of years ahead

    calc_type='Level': e.g. YoY GDP growth

    calc_type='LeRatiovel': e.g. YoY change in leverage ratio

    '''    
    Q = 4*ahead  # ahead in terms of quarters
    col_Yearly = name+'_Yearly'
    if ahead==0:
        col_YoY = name+'_YoY'
    else:
        col_YoY = name+'_YoY_'+str(ahead)+'Y_ahead'        
    if calc_type=='Level':
        df[col_Yearly]=df[name].rolling(window=4).sum()
        df[col_YoY]=df[col_Yearly].pct_change(periods=4).shift(periods=-Q)
        #df[col_YoY+'_TEST']= (df[col_Yearly]/df[col_Yearly].shift(periods=4)-1).shift(periods=-Q)
    elif calc_type=='Ratio':
        df[col_Yearly]=df[name].rolling(window=4).mean()
        df[col_YoY]=df[col_Yearly].diff(periods=4).shift(periods=-Q)
        df[col_YoY+'_TEST']= (df[col_Yearly] - df[col_Yearly].shift(periods=4)).shift(periods=-Q)
               
    return df
# %%
quantiles = [0.05, 0.25, 0.5, 0.75, 0.95] 
quantiles_few = [0.1, 0.5, 0.9] 

# %% 
# Function for Simple Linear Regression (one regressor) 
#
def get_QRparams(x_name,QRmod,q):
    res = QRmod.fit(q=q)      
    return [q, res.params['const'], res.params[x_name]] + res.conf_int().loc[x_name].tolist()

def QR_table(x_name, y_name, df, quantiles=quantiles):
    df = sm.add_constant(df)
    QRmod = sm.QuantReg(endog=df[y_name], exog=df[['const',x_name]], missing='drop')
    QRparams = [get_QRparams(x_name,QRmod,q) for q in quantiles]
    QRparams = pd.DataFrame(QRparams, 
                            columns=['quantile', 'Intescept', 'b', 'lb', 'ub'])
    return QRparams

def ols_fit(x_name, y_name, df):
    df = sm.add_constant(df)
    fit = sm.OLS(endog=df[y_name], exog=df[['const',x_name]], missing='drop').fit()    
    return fit

def ols_table(x_name, y_name, df):
    fit = ols_fit(x_name, y_name, df)
    params = [fit.params['const'], 
              fit.params[x_name]] + fit.conf_int().loc[x_name].tolist()    
    params = pd.DataFrame(params, index=['Intescept', 'b', 'lb', 'ub']).T
    return params

# %%
def linearFunc(a,b,x):
    return a + b * x

def regs_plot(x_name, y_name, df, labelX=None, labelY=None, quantiles=quantiles,add_00_grid=True,**kwargs):   
    '''
    add_00_grid: 

    '''
    if labelX==None: labelX=x_name
    if labelY==None: labelY=y_name
    df = sm.add_constant(df)
    QR_tb = QR_table(x_name, y_name, df, quantiles) 
    ols_tb = ols_table(x_name, y_name, df)
    # plot QR lines
    x = np.linspace(df[x_name].min(), df[x_name].max(), 100)
    ax = plt.axes()
    for i in QR_tb.index:
        y = linearFunc(QR_tb.loc[i,'Intescept'], QR_tb.loc[i,'b'],x)
        ax.plot(x, y, linestyle='dotted', color='grey',
                label='Quantile Req '+str(QR_tb.loc[i,'quantile']))
    
    # plot OLS lines
    y = linearFunc(ols_tb.loc[0,'Intescept'], ols_tb.loc[0,'b'],x)
    ax.plot(x, y, color='red', label='OLS')
    
    # plot Data 
    ax.scatter(df[x_name], df[y_name], alpha=0.5,marker='x',label='Data',**kwargs)
        
    # plot ols predicted values
    ## df['ols_predicted'] = ols_fit(y_name, x_name, df).predict(df[['const',x_name]])
    ##ax.scatter(df[x_name], df['ols_predicted'], alpha=0.5,label='predicted')
    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),ncol=1, 
              fancybox=True, shadow=True)
    ax.set_xlabel(labelX)    
    ax.set_ylabel(labelY)    
    if add_00_grid:
        ax.axvline(x=0,linestyle='--',alpha=0.5,linewidth=2, color='black')
        ax.axhline(y=0,linestyle='--',alpha=0.5,linewidth=2, color='black')
    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    return ax