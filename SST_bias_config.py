# -*- coding: utf-8 -*-
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

home_add ='/home/users/twouce/github/LaunchPAD'

starterp = home_add+'/files/p/'
starterpng = home_add+'/files/png/'
starternc = home_add+'/files/nc/'

