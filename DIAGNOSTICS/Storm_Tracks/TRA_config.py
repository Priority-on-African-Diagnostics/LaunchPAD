# -*- coding: utf-8 -*-
###############################

#OPTIONS for tracking algorithm that can be changed by the user

#what observations to process for?
obs_list = ['ERA5']

vari_list=['ua','va','ta', 'psl', 'uas', 'vas']

pre_processor_experiments = True
processor_calculations1 = True
processor_calculations2 = True
create_plot=True
save_plot=True

# Figure size
fig_width = 200
fig_height = 150

#file name (.p files) note: model name superseeds this string
p_file = '_TRA.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_TRA.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TRA_plot.png'

#location to write output to. Can be absolute or relative path.
home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Storm_Tracks/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Storm_Tracks/png/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Storm_Tracks/intermediary_files/'

