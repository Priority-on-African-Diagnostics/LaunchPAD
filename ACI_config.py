# -*- coding: utf-8 -*-
###############################

#OPTIONS for ACI diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['tas','hfls']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = True 
processor_calculations = True
create_plot = True
save_plot = True

#years to measure over?
yearStart = 1985
yearEnd = 2014

#What lat/lon is required? (prime meridian is assumed zero)
lonWest = -20
lonEast = 54
latSouth = -36
latNorth = 41

#file name (.p files) note: model name superseeds this string
p_file = '_ACI.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_ACI.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_ACI_plot.png'

#ACI input variable
fmod = 'hfls_tas'

starterp = '/home/users/edyer/UoN/files/p/'
starterpng = '/home/users/edyer/UoN/files/png/'
starternc = '/home/users/edyer/UoN/files/nc/'
