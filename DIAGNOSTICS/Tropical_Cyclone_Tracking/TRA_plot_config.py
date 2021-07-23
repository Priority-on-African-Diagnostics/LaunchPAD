# -*- coding: utf-8 -*-
###############################

#If 1, use pickle files. If 2, use txt files.
pickle_or_txt = 1

#model name list?
obs = 'ERA5'

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

starterp = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/'#files/p/'
starterpng = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking/'#files/png/'
starternc = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Tropical_Cyclone_Tracking'#files/nc/'
