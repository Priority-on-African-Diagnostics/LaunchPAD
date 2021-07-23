# -*- coding: utf-8 -*-
###############################
#general options
import collections

#HARDCODED OPTIONS

#generate a dictionary with months
mon_list = collections.OrderedDict()
mon_list ={'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

mod_list = ['UKESM1-0-LL', 'CNRM-CM6-1', 'MRI-ESM2-0', 'GISS-E2-1-G', 'MPI-ESM-1-2-HAM', 'IPSL-CM6A-LR', 'MIROC6', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'NorESM2-LM', 'TaiESM1', 'CNRM-ESM2-1', 'NorESM2-MM', 'BCC-CSM2-MR', 'BCC-ESM1', 'CAMS-CSM1-0', 'FGOALS-f3-L', 'FGOALS-g3', 'CanESM5', 'ACCESS-ESM1-5', 'ACCESS-CM2', 'INM-CM4-8', 'INM-CM5-0', 'HadGEM3-GC31-MM', 'CESM2', 'NorCPM1', 'NESM3', 'SAM0-UNICON']


mon_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
seasons = ['djf','mam','jja','son']
seasn = {'son': 'SON', 'mam': 'MAM', 'jja': 'JJA', 'djf': 'DJF'}

#in case diagnostic crosses prime meridian - fix
lonC1 = 361
lonC2 = 0

CMIP6_extn = '_*.nc'
obs_extn = '.nc'
