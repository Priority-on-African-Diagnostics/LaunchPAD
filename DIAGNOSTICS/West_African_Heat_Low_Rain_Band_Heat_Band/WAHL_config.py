# -*- coding: utf-8 -*-
###############################

obs_list = ['ERA-Interim','ERA5']#, 'MERRA2']
vari_list = ['zg']
#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_WAHL.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_WAHL.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_WAHL_plot.png'

home_add ='/gws/nopw/j04/launchpad/users/edyer/experiment/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/plots/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/intermediary_files/'

