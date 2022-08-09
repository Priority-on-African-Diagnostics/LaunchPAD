# -*- coding: utf-8 -*-
###############################

#OPTIONS for tracking algorithm that can be changed by the user

#what observations to process for?
obs_list = ['ERA5']
#tra_mod_list = ['CNRM-CM6-1','CNRM-CM6-1-HR']
tra_mod_list = ['CNRM-CM6-1-HR']

vari_list=['ua','va','ta', 'psl', 'uas', 'vas']

years = [1990, 2009]

pre_processor_experiments = False
processor_calculations1 = True
processor_calculations2 = True

# Figure size
fig_width = 200
fig_height = 150

#file name (.p files) note: model name superseeds this string
p_file = '_TRA.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_TRA.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TRA_plot.png'

home_add='/gws/nopw/j04/launchpad/users/edyer/TRA_final/'

#location to write output to. Can be absolute or relative path.
starterp =  home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'
starterpng =  home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/plots/'
starternc =  home_add+'LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/intermediary_files/'

