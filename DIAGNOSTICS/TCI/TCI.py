# -*- coding: utf-8 -*-
###############################

###############################
# Start of file:
#
# Terrestrial Coupling Index (TCI)
# 
# Author(s): 
# Anthony Mwanthi (University of Nairobi) : mmwanthi@gmail.com
# Ellen Dyer (University of Oxford) : ellen.dyer@ouce.ox.ac.uk
# Thomas Webb (University of Oxford) : thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Anthony Mwanthi
###############################

###############################
#import required libraries
###############################

import os
import iris
import iris.coords
import iris.analysis
import iris.util
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
from config.find_files import *
from config.config import *
from config.config_functions import *
from TCI_config import *

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

    cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-41, 46) & year_bounds(1985, 2014))
    cube = cube_concatenator(cube_list)
    cube = cube.intersection(longitude=(-20, 54),ignore_bounds=True)
       
    if expt == 'FIO-ESM-2-0':
      iris.util.promote_aux_coord_to_dim_coord(cube,'latitude')
 
    return cube

###############################
#Calculation function(s)
###############################

def conv_volumetric(expt,var2):
  
    # convert from kg/m^2 to m^3/m^3
    # 10 cm layer depth -> 100mm
    if expt in mod_list:  
      vm = (var2/100.0)
    else: 
      vm = var2
    return vm

def calc_TCI(expt,var1,var2,seas):

    #regrid var2 to var1 grid (only due to small lat lon grid differences)
    var2 = var2.regrid(var1, iris.analysis.Linear())

    #season select
    var1_seas = var1.extract(iris.Constraint(clim_season=seas))
    var2_seas = var2.extract(iris.Constraint(clim_season=seas))
    var1_seas = var1_seas.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)
    var2_seas = var2_seas.aggregated_by(['clim_season', 'season_year'],iris.analysis.MEAN)
   
    #calculate standard deviation of hfls
    #CHANGE
    stdd = var2_seas.collapsed('time', iris.analysis.STD_DEV)
    if expt == 'E3SM-1-1':
        print(var1_seas)
        print(var2_seas)

    ccr = iris.analysis.stats.pearsonr(var1_seas, var2_seas,corr_coords='time')

    tci = ccr*stdd
     
    return tci

###############################
#Plotting function(s)
###############################

def plot_TCI(green_list):

    for expt in green_list:
        plt.figure(figsize=(7, 7))
    #CHANGE
        clevs = np.arange(-0.04,0.05,.01)
    #CHANGE
        cmap = plt.cm.Spectral

        for seas in seasons:
            tci = unpickle_cubes(starterp+expt+'_tci_'+fmod+'_'+seas+p_file)

            plt.subplot(2,2,seasons.index(seas)+1)
            cf = iplt.contourf(tci,clevs,cmap=cmap,extend='both')
            plt.gca().coastlines()
            plt.gca().add_feature(cfeature.BORDERS,linewidth=0.2)
            plt.gca().add_feature(cfeature.OCEAN,zorder=100,color='snow')
            plt.gca().set_extent((-20,54,-36,41))
            plt.title(seasn[seas])

        colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
        colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
        plt.suptitle(expt+' TCI '+'('+vari_list[0]+','+vari_list[1]+')')

        if save_plot:

            plt.savefig(starterpng+expt+plot_file, bbox_inches='tight',dpi=100)
       
        else:
            plt.show()
       
        plt.clf()

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
            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+'_'+p_file, "wb" ))
            #iris.io.save(cube_return, starternc+expt+'_'+vari+'_'+nc_file)
  
###############################
#Calculation control
###############################
if processor_calculations:
    print('entering calculation routine')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:

      vari1_cube = unpickle_cubes(starterp+expt+'_'+vari_list[0]+'_'+p_file)
      vari2_cube = unpickle_cubes(starterp+expt+'_'+vari_list[1]+'_'+p_file)

      vari2_cube_vm = conv_volumetric(expt, vari2_cube)

      vari1_seas = season_all_ts(vari1_cube)
      vari2_seas = season_all_ts(vari2_cube_vm)

      for seas in seasons:
        tci = calc_TCI(expt,vari1_seas,vari2_seas,seas)

        pickle.dump(tci, open(starterp+expt+'_tci_'+fmod+'_'+seas+p_file, "wb" ))
        #iris.io.save(tci, starternc+expt+'_tci_'+fmod+'_'+seas+nc_file)
     
###############################
#plot control
###############################
if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    plot_TCI(green_list)
      #plt.show()
      

    print('plotting complete')
 
###############################
#End of file
###############################

