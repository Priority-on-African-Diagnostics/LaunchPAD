# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Ellen Dyer, Anthony Mwanthi
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Anthony Mwanthi
# calculation of Atmospheric Coupling Index Diagnostic
###############################

###############################
#import required libraries
###############################

import os
import iris
import iris.coords
import iris.analysis
import iris.analysis.cartography
import iris.analysis.stats
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
import find_files
from config.find_files import *
from config.config import *
from config.config_functions import *
from ACI_config import *


###############################
#unpickle files
###############################
    
def unpickle_cubes(path):
    """Load cube list from path."""
    with open(path, 'rb') as fh:
        cubes = pickle.load(fh)
    return cubes

###############################
#Extraction function(s)
###############################

def load_expt(expt, vari):

    cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(latSouth-5, latNorth+5) & \
                            year_bounds(yearStart, yearEnd))
    cube = cube_concatenator(cube_list)
    cube = cube.intersection(longitude=(lonWest, lonEast),ignore_bounds=True)
       
    return cube

###############################
#Calculation function(s)
###############################

def calc_ACI(var1,var2,seas):

    #season select
    var1_seas = var1.extract(iris.Constraint(clim_season=seas))
    var2_seas = var2.extract(iris.Constraint(clim_season=seas))
    var1_seas = var1_seas.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)
    var2_seas = var2_seas.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)

    #calculate Pearson correlation
    ccr = iris.analysis.stats.pearsonr(var1_seas, var2_seas,corr_coords='time')

    #calculate standard deviation of tas
    stdd = var1_seas.collapsed('time', iris.analysis.STD_DEV)

    aci = ccr*stdd
     
    return aci

###############################
#Plotting function(s)
###############################

def plot_ACI(expt,seasons):

    plt.figure(figsize=(7, 7))
    clevs = np.arange(-1,1.2,0.2)

    for seas in seasons:
      aci = unpickle_cubes(starterp+expt+'_aci_'+fmod+'_'+seas+p_file)

      plt.subplot(2,2,seasons.index(seas)+1)
      cf = iplt.contourf(aci,clevs,cmap='RdBu_r',extend='both')
      plt.gca().coastlines()
      plt.gca().add_feature(cfeature.BORDERS,linewidth=0.2)
      plt.gca().add_feature(cfeature.OCEAN,zorder=100,color='snow')
      plt.gca().set_extent((lonWest,lonEast,latSouth,latNorth))
      plt.title(seasn[seas])

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
    #colorbar.set_label(' ')
    plt.suptitle(expt+' ACI '+'('+vari_list[0]+','+vari_list[1]+')')

    if save_plot:
     
       plt.savefig(starterpng+expt+plot_file, bbox_inches='tight',dpi=100)

    return None

###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor routine')
   
    green_list = create_greenlist(vari_list)
    green_list =obs_list+green_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list', green_list)

    for expt in green_list:   
        print(expt)
        for vari in vari_list:
            #print(vari)
            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+'_'+p_file, "wb" ))
            iris.io.save(cube_return, starternc+expt+'_'+vari+'_'+nc_file)
  
###############################
#Calculation control
###############################
if processor_calculations:
    print('entering calculation routine')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
 
      print(expt)

      vari1_cube = unpickle_cubes(starterp+expt+'_'+vari_list[0]+'_'+p_file)
      vari2_cube = unpickle_cubes(starterp+expt+'_'+vari_list[1]+'_'+p_file)

      vari1_seas = season_all_ts(vari1_cube)
      vari2_seas = season_all_ts(vari2_cube)

      for seas in seasons:
        aci = calc_ACI(vari1_seas,vari2_seas,seas)

        pickle.dump(aci, open(starterp+expt+'_aci_'+fmod+'_'+seas+p_file, "wb" ))
        iris.io.save(aci, starternc+expt+'_aci_'+fmod+'_'+seas+nc_file)
     
###############################
#plot control
###############################
if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      plot_ACI(expt,seasons)
      plt.show()
      plt.clf()

    print('plotting complete')
 
###############################
#End of file
###############################

