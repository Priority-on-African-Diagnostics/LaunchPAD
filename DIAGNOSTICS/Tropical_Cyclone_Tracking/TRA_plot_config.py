# -*- coding: utf-8 -*-
###############################
import TRA_config

#If 1, use pickle files. If 2, use txt files.
pickle_or_txt = 2

#model name list?
obs = 'ERA5'
tra_mod_list = ['CNRM-CM6-1','CNRM-CM6-1-HR']

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

home_add ='/gws/nopw/j04/launchpad/users/edyer/TRA_final/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/plots/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'


