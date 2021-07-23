# -*- coding: utf-8 -*-

import collections
#DO NOT ALTER FILE
#harcoded options for find_files.py

#lists for find_files

#model dictionary
group_list = collections.OrderedDict()
#varient dictionary
var_list = collections.OrderedDict()
#grid label dictionary
g_list = collections.OrderedDict()

group_list ={'UKESM1-0-LL':'MOHC','CNRM-CM6-1':'CNRM-CERFACS', 'MRI-ESM2-0':'MRI', 'GFDL-CM4':'NOAA-GFDL','GISS-E2-1-G':'NASA-GISS','HadGEM3-GC31-LL':'MOHC','TaiESM1':'AS-RCEC','AWI-CM-1-1-MR':'AWI','BCC-CSM2-MR':'BCC','BCC-ESM1':'BCC','CAMS-CSM1-0':'CAMS','FGOALS-f3-L':'CAS','FGOALS-g3':'CAS','CanESM5':'CCCma','CNRM-ESM2-1':'CNRM-CERFACS','ACCESS-ESM1-5':'CSIRO','ACCESS-CM2':'CSIRO-ARCCSS','FIO-ESM-2-0':'FIO-QLNM','MPI-ESM-1-2-HAM':'HAMMOZ-Consortium','INM-CM4-8':'INM','INM-CM5-0':'INM','IPSL-CM6A-LR':'IPSL','MIROC6':'MIROC','HadGEM3-GC31-MM':'MOHC','MPI-ESM1-2-HR':'MPI-M','MPI-ESM1-2-LR':'MPI-M','CESM2':'NCAR','NorCPM1':'NCC','NorESM2-LM':'NCC','NorESM2-MM':'NCC','NESM3':'NUIST','SAM0-UNICON':'SNU'}
var_list ={'UKESM1-0-LL':'r1i1p1f2','CNRM-CM6-1':'r1i1p1f2', 'MRI-ESM2-0':'r1i1p1f1', 'GFDL-CM4':'r1i1p1f1','GISS-E2-1-G':'r1i1p1f1','HadGEM3-GC31-LL':'r1i1p1f3','TaiESM1':'r1i1p1f1','AWI-CM-1-1-MR':'r1i1p1f1','BCC-CSM2-MR':'r1i1p1f1','BCC-ESM1':'r1i1p1f1','CAMS-CSM1-0':'r1i1p1f1','FGOALS-f3-L':'r1i1p1f1','FGOALS-g3':'r1i1p1f1','CanESM5':'r1i1p1f1','CNRM-ESM2-1':'r1i1p1f2','ACCESS-ESM1-5':'r1i1p1f1','ACCESS-CM2':'r1i1p1f1','FIO-ESM-2-0':'r1i1p1f1','MPI-ESM-1-2-HAM':'r1i1p1f1','INM-CM4-8':'r1i1p1f1','INM-CM5-0':'r1i1p1f1','IPSL-CM6A-LR':'r1i1p1f1','MIROC6':'r1i1p1f1','HadGEM3-GC31-MM':'r1i1p1f3','MPI-ESM1-2-HR':'r1i1p1f1','MPI-ESM1-2-LR':'r1i1p1f1','CESM2':'r1i1p1f1','NorCPM1':'r1i1p1f1','NorESM2-LM':'r1i1p1f1','NorESM2-MM':'r1i1p1f1','NESM3':'r1i1p1f1','SAM0-UNICON':'r1i1p1f1'}
g_list ={'UKESM1-0-LL':'gn','CNRM-CM6-1':'gr', 'MRI-ESM2-0':'gn', 'GFDL-CM4':'gr1','GISS-E2-1-G':'gn','HadGEM3-GC31-LL':'gn','TaiESM1':'gn','AWI-CM-1-1-MR':'gn','BCC-CSM2-MR':'gn','BCC-ESM1':'gn','CAMS-CSM1-0':'gn','FGOALS-f3-L':'gr','FGOALS-g3':'gn','CanESM5':'gn','CNRM-ESM2-1':'gr','ACCESS-ESM1-5':'gn','ACCESS-CM2':'gn','FIO-ESM-2-0':'gn','MPI-ESM-1-2-HAM':'gn','INM-CM4-8':'gr1','INM-CM5-0':'gr1','IPSL-CM6A-LR':'gr','MIROC6':'gn','HadGEM3-GC31-MM':'gn','MPI-ESM1-2-HR':'gn','MPI-ESM1-2-LR':'gn','CESM2':'gn','NorCPM1':'gn','NorESM2-LM':'gn','NorESM2-MM':'gn','NESM3':'gn','SAM0-UNICON':'gn'}

#g_list for daily files is different
g_day_list = collections.OrderedDict()
g_day_list ={'UKESM1-0-LL':'gn','CNRM-CM6-1':'gr', 'MRI-ESM2-0':'gn', 'GFDL-CM4':'gr2','GISS-E2-1-G':'gn','HadGEM3-GC31-LL':'gn','TaiESM1':'gn','AWI-CM-1-1-MR':'gn','BCC-CSM2-MR':'gn','BCC-ESM1':'gn','CAMS-CSM1-0':'gn','FGOALS-f3-L':'gr','FGOALS-g3':'gn','CanESM5':'gn','CNRM-ESM2-1':'gr','ACCESS-ESM1-5':'gn','ACCESS-CM2':'gn','FIO-ESM-2-0':'gn','MPI-ESM-1-2-HAM':'gn','INM-CM4-8':'gr1','INM-CM5-0':'gr1','IPSL-CM6A-LR':'gr','MIROC6':'gn','HadGEM3-GC31-MM':'gn','MPI-ESM1-2-HR':'gn','MPI-ESM1-2-LR':'gn','CESM2':'gn','NorCPM1':'gn','NorESM2-LM':'gn','NorESM2-MM':'gn','NESM3':'gn','SAM0-UNICON':'gn'}
# directory hardcoded listings
CMIP6_base = '/badc/cmip6/data/CMIP6/CMIP/'
CMIP6_type = '/historical/'
CMIP6_time_6 = '/6hrPlevPt/'
CMIP6_time_mon = '/Amon/'
CMIP6_time_day = '/day/'
CMIP6_file = '/latest/'
dash = '/'

obs_base='/gws/nopw/j04/launchpad/observations/'
obs_mon='/mon/'
obs_six='/6am/'
