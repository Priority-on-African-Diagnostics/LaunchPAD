# -*- coding: utf-8 -*-
###############################

#OPTIONS for TCI diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['hfls','mrsos']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = False
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_TCI.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_TCI.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TCI_plot.png'

#TCI input variable
fmod = 'mrsos_tas'

starterp = '/home/users/twouce/github/LaunchPAD/files/p/'
starterpng = '/home/users/twouce/github/LaunchPAD/files/png/'
starternc = '/home/users/twouce/github/LaunchPAD/files/nc/'
