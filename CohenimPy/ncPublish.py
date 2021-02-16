# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:31:45 2020

@author: Nimrod Cohen

helpfull function for phblishing

"""
import subprocess
import os
import src.config as config

# %%
def NBtoTex(current_NB_path,nb_name):    
    project_path = config.project_path    
    os.chdir(current_NB_path)
    ###################################################
    ### IMPORTENT : update Notebook file_name below ###
    ###################################################
    ## Print Notebook wo code (inputs)

    #!jupyter nbconvert 2.0-c-ISR_data_exploreation.ipynb --no-input --no-prompt --to pdf
    
    #--template nc_article
    go = r"jupyter nbconvert" # or path + .exe ?
    #subprocess.run([go,  nb_name+'.ipynb', '--no-input --to latex --no-prompt',shell=True])
    subprocess.run(['!jupyter nbconvert'])
    
    # to try also https://ipypublish.readthedocs.io/en/latest/ : 
    # !nbpublish -f latex_ipypublish_all -pdf file_name.ipynb
    # also sphinx and jupinx and more....
    os.chdir(project_path)   
    return 