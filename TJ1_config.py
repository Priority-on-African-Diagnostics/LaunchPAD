# -*- coding: utf-8 -*-
###############################

#OPTIONS for TJ1 diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5']

vari_list = ['ua','va','hus']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = True 
processor_calculations = True
create_plot = True
save_plot = True

#wind vector threshold
thresh = 5


#file name (.p files) note: model name superseeds this string
p_file = '_TJ1.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_TJ1.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TJ1_plot.png'

starterp = '/home/users/twouce/github/LaunchPAD/files/p/'
starterpng = '/home/users/twouce/github/LaunchPAD/files/png/'
starternc = '/home/users/twouce/github/LaunchPAD/files/nc/'
