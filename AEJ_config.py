# -*- coding: utf-8 -*-
###############################

#OPTIONS for AEJ diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['ua']  

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

thresh = -6.0

#file name (.p files) note: model name superseeds this string
p_file = '_AEJ.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_AEJ.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_AEJ_plot.png'

starterp = '/home/users/twouce/github/LaunchPAD/files/p/'
starterpng = '/home/users/twouce/github/LaunchPAD/files/png/'
starternc = '/home/users/twouce/github/LaunchPAD/files/nc/'
