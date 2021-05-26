# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# African Easterly Jet (AEJ)
# 
# Author(s): 
# Giresse Turin (University of Yaounde) : giresseturin@yahoo.fr
# Thomas Webb (University of Oxford) : thomas.webb@ouce.ox.ac.uk
# Ellen Dyer (University of Oxford) : ellen.dyer@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Giresse Turin
# calculation of AEJ: AEJs_location_intensities.ncl
###############################

#OPTIONS for AEJ diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['ta', 'ua'] 

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_AEJ.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_AEJ.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_AEJ_plot.png'

starterp = '/gws/nopw/j04/launchpad/users/edyer/testing_AEJ/DIAGNOSTICS/African_Easterly_Jet/intermediary_files/'
starterpng = '/gws/nopw/j04/launchpad/users/edyer/testing_AEJ/DIAGNOSTICS/African_Easterly_Jet/plots/'
starternc = '/gws/nopw/j04/launchpad/users/edyer/testing_AEJ/DIAGNOSTICS/African_Easterly_Jet/intermediary_files/'
