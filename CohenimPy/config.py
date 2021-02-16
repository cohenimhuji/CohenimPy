# -*- coding: utf-8 -*-
# %%
"""
Created on Mon Nov 16 11:23:37 2020

@author: u30l
"""

ShowSysPath = True
if ShowSysPath:
    import sys
    print (Config at '\n'.join(sys.path))
#%% Configure the matplotlib plt
import matplotlib.pyplot as my_plt

figsize_scale = 0.66
my_plt.rcParams['figure.figsize'] =[16*figsize_scale, 9*figsize_scale] # [6.4, 4.8]
my_plt.rcParams['axes.labelsize'] = 18
my_plt.rcParams['axes.titlesize'] = 20
#my_plt.rcParams['axes.facecolor'] = None # ? for Dark Theme's...
my_plt.rcParams['font.size'] = 16
my_plt.rcParams['lines.linewidth'] = 2.0
my_plt.rcParams['lines.markersize'] = 9
my_plt.rcParams['legend.fontsize'] = 14

my_plt.rcParams.update({
    'savefig.dpi' : 75,
    'figure.autolayout': False,
    'text.usetex': True,
    'font.family': 'serif',
    #"pgf.texsystem":  "pdflatex",#"xelatex",
    # "font.serif": ["Palatino"], # or Times, Palatino, New Century Schoolbook, Bookman, Computer Modern Roman 
    # font.sans-serif    : Helvetica, Avant Garde, Computer Modern Sans serif    
    # Here we can call Latex directly:    
    'text.latex.preamble' : r'\usepackage{fourier} \usepackage{underscore} \usepackage{fontawesome}'
    # \usepackage{amsmath} \usepackage[T1]{fontenc} \usepackage[utf8x]{inputenc}'
})
# \usepackage{underscore} : to neglict tex '_' . otherwise the latex dosent work!

# Alternativily:
# my_plt.rc('text', usetex=True)
# my_plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{fourier}')       
# or:
# my_plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}, \usepackage{fourier}'

# my_plt.style.use('seaborn') # pretty matplotlib plots

#%%
import pandas as my_pd    # Statistic module
my_pd.set_option('precision', 1)
my_pd.set_option('display.max_columns', None)
my_pd.set_option('display.max_colwidth', None)
# Reduce decimal points to 2
my_pd.options.display.float_format = '{:,.2f}'.format

# %%

import src.funct.proj_tree as tree
project_path = tree.get_project_root() 
figs_path = 'reports/WorkingPaper_LaTeX/WP_figures/'

#tree.print_tree(project_path)

# %%
from datetime import datetime
now = datetime.now()
file_date = '_'+str(now.year)+'_'+str(now.month)+'_'+str(now.day)+'_'+str(now.hour)+'_'+str(now.minute)
