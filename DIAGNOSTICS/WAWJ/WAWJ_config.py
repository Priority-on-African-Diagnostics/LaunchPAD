# -*- coding: utf-8 -*-
###############################

#OPTIONS for tracking algorithm that can be changed by the user

#what observations to process for?
obs_list = ['ERA5']

vari_list=['ua','va']

scale_fact = 4.5
lon_step = 5
lat_step = 2

#Step by step 1.3
mon1='Mar'
mon2='Nov'

pre_processor_experiments = False
processor_calculations = False
create_plot=True
save_plot=False

# Figure size
fig_width = 200
fig_height = 150

#file name (.p files) note: model name superseeds this string
p_file = '_WAWJ.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_WAWJ.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_WAWJ_plot.png'

#location to write output to. Can be absolute or relative path.
starterp = '/home/users/twouce/github/UCT/files/p/'
starterpng = '/home/users/twouce/github/UCT/files/png/'
starternc = '/home/users/twouce/github/UCT/files/nc/'

jet_threshold=10
