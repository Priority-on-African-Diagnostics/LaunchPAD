# -*- coding: utf-8 -*-
###############################

obs_list = ['ERA-Interim'] #'ERA5', 'MERRA2', 
vari_list = ['zg','ts', 'pr']
#what do you want script to do?
pre_processor_experiments = False
processor_calculations = False
create_plot = True
save_plot = False

#file name (.p files) note: model name superseeds this string
p_file = '_WAHL.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_WAHL.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_WAHL_plot.png'

home_add ='/home/users/twouce/github/LaunchPAD/files'

starterp = home_add+'/p/'
starterpng = home_add+'/png/'
starternc = home_add+'/nc/'
