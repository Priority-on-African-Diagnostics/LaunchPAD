# -*- coding: utf-8 -*-
###############################

#OPTIONS for tracking algorithm that can be changed by the user

#what observations to process for?
obs_list = ['ERA5']

vari_list=['ua','va','zg']

scale_fact = 20.0
lon_step = 5
lat_step = 2

#Step by step 1.3
mon1='Mar'
mon2='Nov'

jet_threshold=10

pre_processor_experiments = True
processor_calculations = True
create_plot=True
save_plot=True

# Figure size
fig_width = 200
fig_height = 150

#file name (.p files) note: model name superseeds this string
p_file = '_WAWJ.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_WAWJ.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_WAWJ_plot.png'

#location to write output to. Can be absolute or relative path.

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Westerly_Jet/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Westerly_Jet/png/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Westerly_Jet/intermediary_files/'

