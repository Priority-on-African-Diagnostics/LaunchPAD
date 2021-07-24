# -*- coding: utf-8 -*-
###############################

#If 1, use pickle files. If 2, use txt files.
pickle_or_txt = 2

#model name list?
obs = 'ERA5'
tra_mod_list = ['CNRM-CM6-1-HR']

#what do you want script to do?
pre_processor_experiments = True 
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_tra.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_tra.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_tra_plot.png'

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/png/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'


