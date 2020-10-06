# -*- coding: utf-8 -*-

###############################
# Start of file:
#
# Mozambique Channel Trough (MCT)
# MCT index defined as the area averaged of the relative vorticity
# in the south Mozambique Channel
# 
# Author(s): 
# Rondro Barimalala (University of Cape Town) : rondrotiana.barimalala@uct.ac.za
# Thomas Webb (University of Oxford): thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Rondro Barimalala
# calculation of MCT
###############################

obs_list = ['ERA-Interim']
vari_list=['ua','va']

pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_MCT.p'
 
#file name (.nc file) note: model name superseeds this string
nc_file = '_MCT.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_MCT_plot.png'

starterp = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/MCT/intermediary_files/'
starterpng = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/MCT/plots/'
starternc = '/home/users/twouce/github/LaunchPAD/DIAGNOSTICS/MCT/intermediary_files/'

