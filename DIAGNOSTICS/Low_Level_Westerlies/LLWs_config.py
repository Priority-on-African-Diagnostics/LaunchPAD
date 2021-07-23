# -*- coding: utf-8 -*-
###############################

#OPTIONS that can be changed by the user

#years to measure over?
yearStart = 1980
yearEnd = 2010

seas = 'son'

#What lat/lon is required? (prime meridian is assumed zero)
lonWest = -10
lonEast = 40
latSouth = -25
latNorth = 25

pressLow=92500

#what observations to process for?
obs_list = ['MERRA2','ERA5','ERA-Interim']

vari_list=['wap','ua','hus','ta','psl']

pre_processor_experiments = True
processor_calculations = True
create_plot=True
save_plot=True

#file name (.p files) note: model name superseeds this string
p_file = '_LLW.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_LLW.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_LLW_plot.png'

#location to write output to. Can be absolute or relative path.
starterp = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Low_Level_Westerlies/intermediary_files/'
starterpng = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Low_Level_Westerlies/plots/'
starternc = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Central_African_Easterlies/intermediary_files/Low_Level_Westerlies/intermediary_files/'
