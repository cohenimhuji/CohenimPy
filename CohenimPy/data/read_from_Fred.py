# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] slideshow={"slide_type": "slide"}
# #### November 2020
# #### Nimrod Cohen

# %% [markdown]
# # FRED - get US DATA
# https://pandas-datareader.readthedocs.io/en/latest/index.html#
#
#
# https://medium.com/swlh/pandas-datareader-federal-reserve-economic-data-fred-a360c5795013

# %% [markdown]
# nimrod.cohen@boi.org.il
# Your registered API key is:
# 487fde0d8e221dc44a0cd8a8cffca504
# Documentation is available on the St. Louis Fed web services website.

# %% [markdown]
# ### fredapi
#
# ##### conda install   :  %conda install -c conda-forge fredapi
#
# https://mortada.net/python-api-for-fred.html
#
# there is also : %pip install pandas-datareader
# %%
import src.config as config
file_date = config.file_date
project_path = config.project_path

import pandas as pd    # Statistic module
pd.set_option('precision', 1)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
# Reduce decimal points to 2
pd.options.display.float_format = '{:,.2f}'.format
# %%
import os
os.chdir(project_path)
path = 'data/external/fromFRED/' 
try: 
    os.makedirs(path)
    print('path created')
except OSError: 
    pass
# %%
from fredapi import Fred as fred
fred = fred(api_key='487fde0d8e221dc44a0cd8a8cffca504')
# %%
id = ['TERMCBCCINTNS','TERMCBCCALLNS','FEDFUNDS','PCE','GPDI','GDP','CMDEBT','CPIAUCSL',
          'USRECM','USARECM', 'ISRRECM', 'ISRRECP', 'ISRREC']

def Get_from_FRED(id=id,path=path):    
    data = list()
    info = list()
    id_for_loop = id.copy()
    while id_for_loop:
        for i in id_for_loop:
            print(i, 'trying...')
            try:
                series = fred.get_series(i)
                series_info = fred.get_series_info(i)
                print('secceed.')
                data.append(series)
                info.append(series_info)
                id_for_loop.remove(i)
            except IOError:
                print('did not secceed!')

    df_info = pd.DataFrame(info).T
    df_info.columns = list(df_info.loc['id'])

    df_US = pd.DataFrame(data).T
    df_US.columns= df_info.columns
    df_US.index.name = 'date'

    df_US.to_csv(path+'fromFRED_data'+file_date+'.csv')
    df_info.to_csv(path+'fromFRED_info'+file_date+'.csv')
    df_US.to_csv(path+'fromFRED_data.csv')
    df_info.to_csv(path+'fromFRED_info.csv')
    return

#import CohenimPy.ncDate as ncData

def Get_data(path=path):    
    return ncData.Get_data(path+'fromFRED_data.csv')

def Get_info(path=path):
    return pd.read_csv(path+'fromFRED_info.csv',index_col=0)