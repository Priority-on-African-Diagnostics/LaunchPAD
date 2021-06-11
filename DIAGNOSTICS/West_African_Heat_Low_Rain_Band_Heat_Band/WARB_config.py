# -*- coding: utf-8 -*-
###############################

obs_list = ['GPCP']  
vari_list = ['pr']
#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_WARB.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_WARB.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_WARB_plot.png'

home_add ='/gws/nopw/j04/launchpad/users/edyer/testing_WAHL/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band'

starterp = home_add+'/p/'
starterpng = home_add+'/png/'
starternc = home_add+'/nc/'
