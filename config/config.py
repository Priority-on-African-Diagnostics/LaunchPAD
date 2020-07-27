# -*- coding: utf-8 -*-
###############################
#general options
import collections

#HARDCODED OPTIONS

#generate a dictionary with months
mon_list = collections.OrderedDict()
mon_list ={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

mod_list = ['UKESM1-0-LL','CNRM-CM6-1', 'MRI-ESM2-0', 'GFDL-CM4','GISS-E2-1-G','HadGEM3-GC31-LL','TaiESM1','AWI-CM-1-1-MR','BCC-CSM2-MR','BCC-ESM1','CAMS-CSM1-0','FGOALS-f3-L','FGOALS-g3','CanESM5','CNRM-ESM2-1','ACCESS-ESM1-5','ACCESS-CM2','E3SM-1-1','FIO-ESM-2-0','MPI-ESM-1-2-HAM','INM-CM4-8','INM-CM5-0','IPSL-CM6A-LR','MIROC6','HadGEM3-GC31-MM','MPI-ESM1-2-HR','MPI-ESM1-2-LR','CESM2','NorCPM1','NorESM2-LM','NorESM2-MM','NESM3','SAM0-UNICON']


mon_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
seasons = ['djf','mam','jja','son']
seasn = {'son': 'SON', 'mam': 'MAM', 'jja': 'JJA', 'djf': 'DJF'}

#in case diagnostic crosses prime meridian - fix
lonC1 = 361
lonC2 = 0

#WAHL input variable
CMIP_WAHL_out = 'zg'

CMIP6_extn = '_*.nc'
obs_extn = '.nc'

#track input variables
CMIP_psl_out = 'psl'

CMIP_WAWJ_out = 'zg'

 
     

