# -*- coding: utf-8 -*-
###############################

#OPTIONS for ACI diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['tas','hfls']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = False
processor_calculations = False
create_plot = True
save_plot = False

#file name (.p files) note: model name superseeds this string
p_file = '_ACI.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_ACI.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_ACI_plot.png'

#ACI input variable
fmod = 'hfls_tas'

starterp = '/home/users/twouce/github/LaunchPAD/files/p/'
starterpng = '/home/users/twouce/github/LaunchPAD/files/png/'
starternc = '/home/users/twouce/github/LaunchPAD/files/nc/'
