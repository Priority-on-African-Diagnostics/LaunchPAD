# -*- coding: utf-8 -*-
###############################

#OPTIONS for CAF diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2','ERA-Interim']

#obs for bias
bias_obs = 'ERA5'

vari_list = ['ua','pr']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#years to measure over?
yearStart = 1980
yearEnd = 2014

months = ['Mar','Apr','May']

#What lat/lon is required? (prime meridian is assumed zero)
# Extent for bias plot
latS = -15
latN = 10
lonW = 0
lonE = 45

# Extent for bias metric
latSa = -8
latNa = 2
lonWa = 15
lonEa = 34

# Extent for pr metric
latSb = -4
latNb = 4
lonWb = 33
lonEb = 42

#pressure level
press = 70000

#file name (.p files) note: model name superseeds this string
p_file = '_CAF.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_CAF.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_CAF_plot.png'

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Central_African_Easterlies/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Central_African_Easterlies/plots/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Central_African_Easterlies/intermediary_files/'
