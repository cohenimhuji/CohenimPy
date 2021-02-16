# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:23:37 2020

@author: u30l
"""
from datetime import datetime
from src.config import my_pd as pd


# %%
def period(index, **kwargs):
    '''
        'start' and 'end' in this format:  '2009-11-01'
    '''
    #start,end = index[0],index[-1]
    start,end = index.min(),index.max()
    if start>end:
        return
    if 'start' in kwargs.keys():
        start = datetime.fromisoformat(kwargs['start'])
    if 'end' in kwargs.keys():
        end = datetime.fromisoformat(kwargs['end'])
    return [(t>= start)and(t<= end) for t in index]


def Get_data(file):
    df = pd.read_csv(file,index_col=0)
    df.index = pd.to_datetime(df.index)
    return df