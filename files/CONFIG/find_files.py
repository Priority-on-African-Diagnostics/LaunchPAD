# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Tom Webb
# Contact: thomas.webb@ouce.ox.ac.uk
# To find the files needed by diagnostics on JASMIN
# using absolute paths (CEDA archive)
# used for all diagnostics (6hourly, monthly and daily)
###############################

import collections
from config_find_files import *

#Level 1 6hour data
#in: mod - model, e.g. CNRM-CM6-1, vari - variable in CMIP notation, e.g. zg
#out: mod_dir - listing of all files of mod and vari as absolute paths
def level1_6hr(mod,vari):

    group = group_list[mod]
    var = var_list[mod]
    g = g_list[mod]

    mod_dir = CMIP6_base+group+dash+mod+CMIP6_type+var+CMIP6_time_6+vari+dash+g+CMIP6_file

    return mod_dir

#Level 1 monthly data
#in: mod - model, e.g. CNRM-CM6-1, vari - variable in CMIP notation, e.g. zg
#out: mod_dir - listing of all files of mod and vari as absolute paths    
def level1_mon(mod,vari):

    group = group_list[mod]
    var = var_list[mod]
    g = g_list[mod]

    if vari == 'mrsos':
      mod_dir = CMIP6_base+group+dash+mod+CMIP6_type+var+'/Lmon/'+vari+dash+g+CMIP6_file
    elif vari == 'mrsol':
      mod_dir = CMIP6_base+group+dash+mod+CMIP6_type+var+'/Emon/'+vari+dash+g+CMIP6_file
    else:
      mod_dir = CMIP6_base+group+dash+mod+CMIP6_type+var+CMIP6_time_mon+vari+dash+g+CMIP6_file

    return mod_dir

#Level 1 daily data
#in: mod - model, e.g. CNRM-CM6-1, vari - variable in CMIP notation, e.g. zg
#out: mod_dir - listing of all files of mod and vari as absolute paths    
def level1_day(mod,vari):

    group = group_list[mod]
    var = var_list[mod]
    g = g_day_list[mod]

    mod_dir = CMIP6_base+group+dash+mod+CMIP6_type+var+CMIP6_time_day+vari+dash+g+CMIP6_file

    return mod_dir

def level1_obs_mon(obs):

    obs_dir = obs_base+obs+obs_mon

    return obs_dir

def level1_obs_6hr(obs):

    obs_dir = obs_base+obs+obs_six

    return obs_dir
