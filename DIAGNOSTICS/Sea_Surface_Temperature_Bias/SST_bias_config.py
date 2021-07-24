# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# Sea-Surface Temperature Bias (SST)
# 
# Author(s): 
# Apphia Ackon (KNUST, Ghana) : ackonaphia5@gmail.com
# Thomas Webb (University of Oxford): thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Apphia Ackon
###############################

vari_list=['ts']
obs_list = ['HadISST']

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#years to measure over?
yearStart = 1981
yearEnd = 2014

#What lat/lon is required? (prime meridian is assumed zero)
lonWest = -25
lonEast = 25
latSouth = -40
latNorth = 25

#file name (.p files) note: model name superseeds this string
p_file = '_SST.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_SST.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_SST_bias_plot.png'

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Sea_Surface_Temperature_Bias/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Sea_Surface_Temperature_Bias/png/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Sea_Surface_Temperature_Bias/intermediary_files/'


