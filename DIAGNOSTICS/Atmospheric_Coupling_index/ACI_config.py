# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# Atmospheric Coupling Index
# 
# Author(s): 
# Anthony Mwanthi (University of Nairobi) : mmwanthi@gmail.com
# Ellen Dyer (University of Oxford) : ellen.dyer@ouce.ox.ac.uk
# Thomas Webb (University of Oxford): thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Anthony Mwanthi
# calculation of Atmospheric Coupling Index Diagnostic
###############################

#OPTIONS for ACI diagnostic that can be changed by the user

#model name list?
obs_list = ['ERA5','MERRA2']

vari_list = ['tas','hfls']  #std dev will be calculated for first
                            #var in this list

#what do you want script to do?
pre_processor_experiments = True
processor_calculations = True
create_plot = True
save_plot = True

#file name (.p files) note: model name superseeds this string
p_file = '_ACI.p'

#file name (.nc file) note: model name superseeds this string
nc_file = '_ACI.nc'

#file name (.png plot) note: model name superseeds this string
plot_file = '_ACI_plot.png'

#ACI input variable
fmod = 'hfls_tas'

home_add ='/gws/nopw/j04/launchpad/users/edyer/LaunchPAD_config/'

starterp = home_add+'LaunchPAD/DIAGNOSTICS/Atmospheric_Coupling_index/intermediary_files/'
starterpng = home_add+'LaunchPAD/DIAGNOSTICS/Atmospheric_Coupling_index/plots/'
starternc = home_add+'LaunchPAD/DIAGNOSTICS/Atmospheric_Coupling_index/intermediary_files/'

