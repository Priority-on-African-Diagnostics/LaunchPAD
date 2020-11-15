# -*- coding: utf-8 -*-
###############################

#OPTIONS for tracking algorithm that can be changed by the user

#what observations to process for?
obs_list = ['ERA5']

vari_list=['ua','va','ta', 'psl']

pre_processor_experiments = False
processor_calculations1 = True
processor_calculations2 = False
create_plot=False
save_plot=False

# Figure size
fig_width = 200
fig_height = 150

#file name (.p files) note: model name superseeds this string
p_file = '_TRA.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_TRA.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TRA_plot.png'

#location to write output to. Can be absolute or relative path.
starterp = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/TRA/intermediary_files/'
starterpng = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/TRA/plots/'
starternc = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/TRA/intermediary_files/'

