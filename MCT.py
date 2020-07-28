# -*- coding: utf-8 -*-
#####################################
# Diagnostics to calculate the      #
# Mozambique Channel Trough (MCT)   #
# index from ERA-interim and CMIP   #
# models.                           #
#                                   #
# The MCT index defined as the area #
# averaged of the relative vorticity#
# in the south Mozambique Channel   #
#                                   #
# Author(s): RB, TLW                #
#####################################


#################################
# Import required libraries
#################################

import os
import iris
import iris.coords
import iris.analysis
import iris.analysis.cartography
import iris.plot as iplt
import iris.quickplot as qplt
from iris.experimental.equalise_cubes import equalise_attributes
import matplotlib.pyplot as plt
import iris.coord_categorisation 
import numpy as np
import numpy.ma as ma
import sys
import cartopy
import cartopy.crs as ccrs
import matplotlib.dates as mdates
import collections
import cartopy
import cartopy.crs as crs
import cartopy.feature as cfeature
import cloudpickle as pickle
from config.find_files import *
from config.config import *
from config.config_functions import *
from MCT_config import *
from windspharm.iris import VectorWind

################################

###############################
#unpickle files
###############################
    
def unpickle_cubes(path):
    """Load cube list from path."""
    with open(path, 'rb') as fh:
        cubes = pickle.load(fh)
    return cubes
    
################################

###############################
#Extraction function(s)
###############################

def load_expt(expt, vari):
     CL = iris.load(monthly_file_location(expt, vari), pressure_level(expt, 85000) & year_bounds(1980, 2006))
     CU = cube_concatenator(CL)
     
     return CU

################################

###############################
#Calculation function(s)
###############################

def calc_MCT(expt):

     #assign ua and va stored cubes
 
     ua = unpickle_cubes(starterp+expt+'_'+'ua'+p_file)
     va = unpickle_cubes(starterp+expt+'_'+'va'+p_file) 
     
     ua.data[ua.data > 2000] = 0.0
     va.data[va.data > 2000] = 0.0
     
     ua=climatology(ua)
     va=climatology(va)
     
     
     delta_latitude = 180/180.0
     sample_points = [('longitude', ua.coord('longitude').points),('latitude',  np.linspace(90 - 0.5 * delta_latitude,-90 + 0.5 * delta_latitude,180))]
     ua_r = ua.interpolate(sample_points, iris.analysis.Linear())
     va_r = va.interpolate(sample_points, iris.analysis.Linear())
       
     wa = VectorWind(ua_r,va_r)

     xi = wa.vorticity()
     
     xi=xi.extract(lat_bounds(-26, -16) & lon_bounds(35, 44))
          
     xi = xi.collapsed(['longitude', 'latitude'],iris.analysis.MEAN)

     return xi

################################

###############################
#Plotting function(s)
###############################

def plot_MCT(expt):

     xi = unpickle_cubes(starterp+expt+'_'+'_'+p_file)
     xi2=iris.analysis.maths.multiply(xi,1e6)

     plt.plot(mon_names, xi2.data, label=expt)
    	 
     return None

######################################

###############################
#main execution
###############################

if pre_processor_experiments:
    print('entering PRE-PROCESSOR models routine')
   
###############################
#extraction control
###############################
    green_list = create_greenlist(vari_list)
    green_list = green_list + obs_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" )) 
    for expt in green_list:
        for vari in vari_list:
             pickle.dump(load_expt(expt,vari), open(starterp+expt+'_'+vari+p_file, "wb" ))
             #iris.io.save(cube_return, starternc+expt+'_'+vari+nc_file)
        print('data from '+expt+' pre-processed sucessfully')
    
###############################
#calculation control
###############################

if processor_calculations:
    print('entering CALCULATION models routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:  
        for vari in vari_list: 
            print(expt)        

            cube_return = calc_MCT(expt)
            pickle.dump(cube_return, open(starterp+expt+'_'+'_'+p_file, "wb"))

        print('data from '+expt+' calculated sucessfully')              
     
###############################
#plot control
###############################
if create_plot:
    print('entering PLOTTING routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        plot_MCT(expt)
    if save_plot:
        plt.legend()
            #plt.show()
        plt.savefig(starterpng+'_MCT_plot_'+plot_file, bbox_inches='tight',dpi=100)
    else:
        plt.legend()
        plt.show()
    print('data plotted sucessfully')
	 
###############################
#End of file
###############################
