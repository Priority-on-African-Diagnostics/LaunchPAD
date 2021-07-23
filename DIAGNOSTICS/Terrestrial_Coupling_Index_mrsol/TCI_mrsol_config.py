# -*- coding: utf-8 -*-
###############################

#OPTIONS for TCI diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

#vari_list = ['hfls','mrsol','depth']  #std dev will be calculated for first
                            #var in this list
vari_list = ['hfls','mrsol']  #std dev will be calculated for first
                              #var in this list

#what do you want script to do?
pre_processor_experiments = True 
processor_calculations = True
create_plot = True
save_plot = True

#years to measure over?
yearStart = 1985
yearEnd = 2014

#What lat/lon is reuired? (prime meridian is assumed zero)
lonWest = -20
lonEast = 54
latSouth = -36
latNorth = 41

#file name (.p files) note: model name superseeds this string
p_file = '_TCI_mrsol.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_TCI_mrsol.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TCI_mrsol_plot.png'

#TCI input variable
fmod = 'mrsos_tas'

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Terrestrial_Coupling_Index_mrsol'

starterp = home_add+'/intermediary_files/'
starterpng = home_add+'/png/'
starternc = home_add+'/intermediary_files/'
