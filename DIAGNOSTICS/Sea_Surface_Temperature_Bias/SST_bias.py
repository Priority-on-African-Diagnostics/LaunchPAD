# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# Sea-Surface Temperature Bias (SST)
# 
# Author(s): 
# Apphia Ackon (KNUST, Ghana) : ackonaphia5@gmail.com
# Thomas Webb (University of Oxford): thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Apphia Ackon
###############################

###############################
#import required libraries
###############################

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
import cartopy.crs as crs
import cartopy.feature as cfeature
import cloudpickle as pickle
import cf_units as unit

from SST_bias_config import *
sys.path.insert(1,home_add+'LaunchPAD/files/CONFIG')
from find_files import *
from config import *
from config_functions import *

###############################
#unpickle files
###############################
    
def unpickle_cubes(path):
    """Load cube list from path."""
    with open(path, 'rb') as fh:
        cubes = pickle.load(fh)
    return cubes

###############################
#extraction function(s) models
###############################

def load_expt(expt, vari):

     if expt in mod_list:
       cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(latSouth, latNorth) & \
                            year_bounds(yearStart, yearEnd))
       cube = cube_concatenator(cube_list)
       cube = cube.intersection(longitude=(lonWest, lonEast))
       
     else:
       cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(latSouth, latNorth) & \
                         lon_bounds(lonWest,lonEast) & year_bounds(yearStart, yearEnd))
       cube = cube_concatenator(cube_list)
       
     cube = unit_converter(cube)
     
     return cube

###############################
#Calculation function(s)
###############################

def calc_bias(mod_seas,obs_seas,seas):
    
    #season select
    obs_seas = obs_seas.extract(iris.Constraint(clim_season=seas))
    mod_seas = mod_seas.extract(iris.Constraint(clim_season=seas))

    #regrid model temperatures
    mod_seas = mod_seas.regrid(obs_seas, iris.analysis.Linear())
    #bias calculation
    bias_seas = mod_seas - obs_seas

    return bias_seas

###############################
#Plotting function(s)
###############################

def plot_SST(expt,seasons):
     
     plt.figure(figsize=(5, 5))
     clevs = np.arange(-4.8,5.2,0.4)

     for seas in seasons:
       bias = unpickle_cubes(starterp+expt+'_'+'sstbias_'+seas+p_file)

       plt.subplot(2,2,seasons.index(seas)+1)
       cf = iplt.contourf(bias,clevs,cmap='RdBu_r',extend='both')
       plt.gca().coastlines()
       plt.gca().set_extent((lonWest,lonEast,latSouth,latNorth))
       plt.title(seasn[seas])

     colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
     colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
     colorbar.set_label('K')
     plt.suptitle(expt+' SST biases')


     if save_plot:
       plt.savefig(starterpng+expt+plot_file, bbox_inches='tight',dpi=100)
 
     else:
       iplt.show()

     return None

###############################
#main execution
###############################
if pre_processor_experiments:

    print('entering pre-processor models routine')
   
###############################
#extraction control
###############################
    green_list = create_greenlist(vari_list)
    green_list = green_list + obs_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    
    for expt in green_list:   
      for vari in vari_list:
          cube_return = load_expt(expt, vari)
          pickle.dump(cube_return, open(starterp+expt+'_'+vari+p_file, "wb" ))
          #iris.io.save(cube_return, starternc+expt+'_'+vari+nc_file)
      print('data from '+expt+' pre-processed sucessfully')
    


###############################
#calculation control
###############################

if processor_calculations:
    vari=vari_list[0] #diagnostic specific
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
      
    print('entering CALCULATION routines')
    for obs in obs_list:
      obs_sst_cube = unpickle_cubes(starterp+obs+'_'+vari+p_file)
      obs_seas = season_all(obs_sst_cube)
      green_list.remove(obs)

    for mod in green_list:
      mod_sst_cube = unpickle_cubes(starterp+mod+'_'+vari+p_file)
      mod_seas = season_all(mod_sst_cube)
      
      for seas in seasons:
        sst_bias = calc_bias(mod_seas,obs_seas,seas)

        pickle.dump(sst_bias, open(starterp+mod+'_'+'sstbias_'+seas+p_file, "wb"))
        #iris.io.save(sst_bias, starternc+mod+'_'+'sstbias_'+seas+nc_file) 

    print('calculation complete')

###############################
#Plotting control
###############################

if create_plot:

     print('entering PLOTTING routines')
     green_list =  unpickle_cubes(starterp+'green_list'+p_file)
     for obs in obs_list:
          green_list.remove(obs)
	     
     for expt in green_list:
       plot_SST(expt,seasons)
       plt.clf()

     print('plotting complete')


#End of file
###############################

