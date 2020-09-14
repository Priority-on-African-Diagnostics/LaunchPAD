# -*- coding: utf-8 -*-
###############################

#OPTIONS for AEJ diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5']

vari_list = ['ua']  

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True


#years to measure over?
yearStart = 1980
yearEnd = 2005

#What lat/lon is required? (prime meridian is assumed zero)
lonWest = 14
lonEast = 24
latSouth = -36
latNorth = 41

press1 = 60000
press2 = 70000

thresh = -6.0

#file name (.p files) note: model name superseeds this string
p_file = '_AEJ.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_AEJ.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_AEJ_plot.png'

new_dir='/home/users/twouce/github/LaunchPAD/'
starterp = new_dir#'/gws/nopw/j04/launchpad/users/edyer/UoY/files/p/'
starterpng = new_dir#'/gws/nopw/j04/launchpad/users/edyer/UoY/files/png/'
starternc = new_dir#'/gws/nopw/j04/launchpad/users/edyer/UoY/files/nc/'
