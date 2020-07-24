# -*- coding: utf-8 -*-
###############################

#OPTIONS for WAHL diagnostic that can be changed by the user
#model name list? 

#pick from these models:

vari_list=['ts']
obs_list = ['HadISST']

#what do you want script to do?
pre_processor_experiments = False
processor_calculations = False
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

starterp = '/home/users/twouce/github/KNUST/files/p/'
starterpng = '/home/users/twouce/github/KNUST/files/png/'
starternc = '/home/users/twouce/github/KNUST/files/nc/'

