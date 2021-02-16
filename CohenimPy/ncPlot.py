# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:31:45 2020

@author: u30l

helpfull function for ploting and saving figure in usfull formats

"""
import numpy as np
import subprocess
# import PrettyTable as pt
from src.config import my_pd as pd
#%%
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')
#%%
#import src.config.my_plt as plt
from src.config import my_plt as plt
import matplotlib.colors as mcolors
colors = list(mcolors.TABLEAU_COLORS) 
colors1 = ['tab:blue','tab:cyan','tab:olive','tab:green','tab:gray']
colors2 = ['tab:orange','tab:red','tab:pink','tab:purple','tab:brown']

markers = ['x','o','+','^','>','.','-','<','x','o','+','^','>','.','-','<']
linestyle_str = [   'solid',      # Same as (0, ()) or '-'
                    'dotted',    # Same as (0, (1, 1)) or '.'
                    'dashed',    # Same as '--'
                    'dashdot']  # Same as '-.'
linestyle_tuple = [ (0, ()),
                    (0, (5, 3)),
                    (0, (1, 1)),
                    (0, (3, 1, 1, 1)),
                    (0, (6, 6)),                    
                    (0, (1, 2)),
                    (0, (5, 1)),
                    (0, (3, 3, 1, 3)),      
                    (0, (1, 3)),
                    (0, (3, 5, 1, 5)),                                        
                    (0, (3, 1, 1, 1, 1, 1)),                    
                    (0, (3, 3, 1, 3, 1, 3)),
                    (0, (3, 5, 1, 5, 1, 5)) ]

linestyles = linestyle_tuple
bbox1= (0.1, -0.12)
bbox2= (0.9, -0.12)
# plt.style.use('seaborn') # pretty matplotlib plots

def printest():
    print('Text pass very OK')
    return

def list_rotate(seq, n):
    if seq==[]:
        return seq
    else:    
        n = n % len(seq)
    return seq[n:]+seq[:n]
# %%
def multi_save(name = 'fig'):
    '''
    Save plt to some usefull files
    '''
    plt.tight_layout()
    plt.savefig(name+'.png',dpi=600)
    plt.savefig(name+'.pdf')
    plt.savefig(name+'.svg')
    plt.show()
    # HELP at: https://inkscape.org/he/doc/inkscape-man100.html
    # this works in cmd:
    # "C:\Program Files\Inkscape\bin\inkscape.exe" --export-filename="c:\users\u30l\source22.emf" 
    # "c:\users\u30l\source.svg"
    inkscapePath_go = r"C:/Program Files/Inkscape/bin/inkscape.exe"
    subprocess.run([inkscapePath_go, '--export-type=emf' , name+'.svg'],shell=True)
    return
# %%
def add_Rec(ax,df,col,alpha=0.3,**kwargs):
    lims = ax.get_ylim()
    ax.fill_between(x=df.index,y1=0,y2=1,where=df[col]>0,color='grey', alpha=alpha,
                    transform=ax.get_xaxis_transform(),**kwargs)
    ax.set_ylim(lims)
    return ax
# %%
def plot1ax(ax=None,columns=None,labels=None,df=None,xlabel=None,ylabel=None,title=None,
            tick_color=None,colors=None,markers=markers,
            linestyles=linestyles,bbox=None,**kwargs):
    if ylabel==None: ylabel=columns[0] 
    if ax==None: ax = plt.axes()   
    if labels==None: labels=columns
    if markers=='': markers=['' for col in columns]
    for i,col in enumerate(columns):             
        if colors!=None:             
            kwargs['color'] = colors[i]    
        ax = df[col].dropna().plot(ax=ax,label=labels[i],marker=markers[i],
                                   linestyle=linestyles[i],**kwargs)  # color=colors[i]
    #if xlabel=='': ax.set_xlabel(xlabel='')  
    ax.set_title(title)  
    ax.set_xlabel(xlabel=xlabel)  
    ax.set_ylabel(ylabel=ylabel)
    if tick_color!=None:
        ax.tick_params(axis='y', colors=tick_color)
        ax.yaxis.label.set_color(tick_color)
    ax.legend(bbox_to_anchor=bbox)   
    return ax

def plot2axs(ax1=None,
             columns1=None,columns2=None,
             labels1=None,labels2=None,
             df=None,df2=None,
             ylabel1=None,ylabel2=None,
             colors1=colors1,colors2=colors2,
             markers=markers,linestyles=linestyles,
             bbox1=None,bbox2=None,**kwargs):
    if df2==None: df2=df 
    ax1 = plot1ax(ax=ax1,columns=columns1,labels=labels1,df=df,ylabel=ylabel1,tick_color=colors1[0], colors=colors1,
                  markers=markers,linestyles=linestyles,bbox=bbox1,**kwargs)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis   
    ax2.spines['left'].set_color(colors1[0])    

    n=len(columns1)
    if colors2==None: colors2=list_rotate(colors1, n)
    markers = list_rotate(markers, n)    
    linestyles=list_rotate(linestyles, n)    
    ax2 = plot1ax(ax=ax2,columns=columns2,labels=labels2,df=df2,ylabel=ylabel2,tick_color=colors2[0], colors=colors2,
                  markers=markers,linestyles=linestyles,bbox=bbox2,**kwargs)
    ax2.spines['right'].set_color(colors2[0])    
    #ax2.spines['top'].set_color('')                 
    return ax1,ax2

def path_in2D(columnX,columnY,df=[],ylabel=None,xlabel=None,
             color=colors[0],marker=markers[0],linestyles=linestyles):
    if xlabel==None: 
        xlabel=columnX 
    if ylabel==None: 
        ylabel=columnY    
   
    x = df[columnX]
    y = df[columnY]
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u
    pos_y = y[:-1] + v
    # norm = np.sqrt(u**2+v**2)       

    ax=df.plot.scatter(columnX, columnY,s=100,marker=marker,color=color)
    ax.quiver(pos_x, pos_y, u, v, scale_units='xy',angles="xy", pivot="tip", scale=1,
              linestyles=linestyles[0],color=color)
    ax.set_xlabel(xlabel=xlabel)
    ax.set_ylabel(ylabel=ylabel)
    return ax