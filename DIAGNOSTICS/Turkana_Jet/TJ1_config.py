# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# Turkana Jet (TJ1)
# 
# Author(s): 
# Oscar Lino (University of Nairobi) : lino@students.uonbi.ac.ke
# Ellen Dyer (University of Oxford) : ellen.dyer@ouce.ox.ac.uk
# Thomas Webb (University of Oxford) : thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Oscar Lino
###############################

#OPTIONS for TJ1 diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['ua','va','hus']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_TJ1.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_TJ1.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_TJ1_plot.png'

starterp = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Turkana_Jet/intermediary_files/'
starterpng = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Turkana_Jet/plots/'
starternc = '/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/LaunchPAD/DIAGNOSTICS/Turkana_Jet/intermediary_files/'
