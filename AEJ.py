	# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Tom Webb
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Giresse Turin
# AEJs_location_intensities.ncl
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
import cartopy
import cartopy.crs as crs
import cartopy.feature as cfeature
import cloudpickle as pickle

from config.find_files import *
from config.config import *
from config.config_functions import *
from AEJ_config import *

import operator
import xarray as xr

from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from pylab import *

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

     CLN = iris.load(monthly_file_location(expt, vari), lat_bounds(3, 20) & lon_bounds(14, 24) & pressure_bounds(expt, 60000, 70000) & year_bounds(1980, 2005))
     CUN = cube_concatenator(CLN)
     
    
     CLS = iris.load(monthly_file_location(expt, vari), lat_bounds(-20, -5) & lon_bounds(14, 24) & year_bounds(1980, 2005) & pressure_level(expt, 60000))
     CUS = cube_concatenator(CLS)
     
     CUS = climatology(CUS.collapsed('longitude', iris.analysis.MEAN)) #south 
     
     CUN = pressure_min_collapse(expt, CUN)
     CUN = climatology(CUN.collapsed('longitude', iris.analysis.MEAN)) #north
     
         
     return CUN, CUS
	
###############################
#calculation function(s)
###############################

def calc_AEJ(expt,vari):

    N_latitude, cubeN_intensity = find_lat_int(unpickle_cubes(starterp+expt+'_'+vari+'_'+'CUN'+p_file))      
    S_latitude, cubeS_intensity = find_lat_int(unpickle_cubes(starterp+expt+'_'+vari+'_'+'CUS'+p_file))  
      
    return cubeN_intensity, cubeS_intensity, N_latitude, S_latitude
    
def find_lat_int(cube):

    thresh=-6.0

    lat = []
    xr_cube = xr.DataArray.from_iris(cube)
    if expt in ['ERA5','ERA-Interim']:
      xr_min = xr_cube.min(dim='latitude')
    else:
      xr_min = xr_cube.min(dim='lat')
    xr_min = xr_min.where(xr_min<thresh)
    for m in xr_cube.time:
      try:
        if expt in ['ERA5','ERA-Interim']:
          lat.append(xr_cube.latitude.where(xr_cube.sel(time=m)==xr_min.sel(time=m),drop=True).item())
        else:
          lat.append(xr_cube.lat.where(xr_cube.sel(time=m)==xr_min.sel(time=m),drop=True).item())
      except:
        lat.append(np.nan)

    cube = xr.DataArray.to_iris(xr_min)

    return lat, cube
    
    	
###############################
#plot diagnostic
###############################

def plot_AEJ(green_list):
      
    len_clist = int(ceil(len(green_list) /3.0))   
    cm = plt.get_cmap('gist_rainbow', len_clist)

    colourWheel=[]
    for i in range(len_clist):
        rgb = cm(i)[:3] # will return rgba, we take only first 3 so we get rgb
        colourWheel.append(str(matplotlib.colors.rgb2hex(rgb)))
      
    fig, ax = plt.subplots()
    nameOfPlot = 'African Easterly Jet (Giresse Turin)'
    fig.suptitle(nameOfPlot, fontsize=14)
    plt.title(nameOfPlot)
    
    clist = len(green_list)
    
    dashesStyles = [[3,1],
            [1000,1],
            [2,1,10,1],
            [4, 1, 1, 1, 1, 1]]

    plt.subplot(2,2,1)
    plt.title('North')
    for j, expt in enumerate( green_list):
        LN = unpickle_cubes(starterp+expt+'_'+'N_latitude'+'_'+p_file) 
        if expt in obs_list:
            c_o = '#000000'
            linethick = 2.5
            c_zorder = clist + 1
            dashesSty = dashesStyles[obs_list.index(expt)]
        else:
            c_o = colourWheel[j%len(colourWheel)]
            linethick = 1.5
            c_zorder = j
            if j >= len_clist and j < 2*len_clist:
                dashesSty = dashesStyles[0]
            elif j >= 2*len_clist:
                dashesSty = dashesStyles[2]
            else:
                dashesSty = dashesStyles[1]
        plt.plot(mon_names, LN, linestyle = '-', color= c_o, dashes=dashesSty, lw=linethick, label=expt, zorder = c_zorder)   
    plt.ylim(0,14)
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Latitude', fontsize=12) 
        
    plt.subplot(2,2,2)
    plt.title('South')
    for j, expt in enumerate( green_list):
        LS = unpickle_cubes(starterp+expt+'_'+'S_latitude'+'_'+p_file) 
        if expt in obs_list:
            dashesSty = dashesStyles[obs_list.index(expt)]
            c_o = '#000000'
            linethick = 2.5
            c_zorder = clist + 1
        else:
            c_o = colourWheel[j%len(colourWheel)]
            linethick = 1.5
            c_zorder = j
            if j >= len_clist and j < 2*len_clist:
                dashesSty = dashesStyles[0]
            elif j >= 2*len_clist:
                dashesSty = dashesStyles[2]
            else:
                dashesSty = dashesStyles[1]
        plt.plot(mon_names, LS, linestyle = '-', color= c_o, dashes=dashesSty, lw=linethick, label=expt, zorder = c_zorder)
    plt.ylim(-12,0)
    plt.xticks(np.arange(12), mon_names, rotation=45)

    
    plt.subplot(2,2,3) 
    for j, expt in enumerate( green_list):
        CU_N = unpickle_cubes(starterp+expt+'_'+'cubeN_intensity'+'_'+p_file)
        if expt in obs_list:
            c_o = '#000000'
            linethick = 2.5
            c_zorder = clist + 1
            dashesSty = dashesStyles[obs_list.index(expt)]
        else:
            c_o = colourWheel[j%len(colourWheel)]
            linethick = 1.5
            c_zorder = j
            if j >= len_clist and j < 2*len_clist:
                dashesSty = dashesStyles[0]
            elif j >= 2*len_clist:
                dashesSty = dashesStyles[2]
            else:
                dashesSty = dashesStyles[1]
        qplt.plot(CU_N.coord('month'), CU_N, linestyle = '-', color= c_o, dashes=dashesSty, lw=linethick, label=expt, zorder = c_zorder)
    plt.ylim(-6,-16)
    plt.title(' ')
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Intensity (m/s)', fontsize=12)    
   
    plt.subplot(2,2,4)
    for j, expt in enumerate( green_list):
        CU_S = unpickle_cubes(starterp+expt+'_'+'cubeS_intensity'+'_'+p_file)
        if expt in obs_list:
            c_o = '#000000'
            linethick = 2.5
            c_zorder = clist + 1
            dashesSty = dashesStyles[obs_list.index(expt)]
        else:
            c_o = colourWheel[j%len(colourWheel)]
            linethick = 1.5
            c_zorder = j
            if j >= len_clist and j < 2*len_clist:
                dashesSty = dashesStyles[0]
            elif j >= 2*len_clist:
                dashesSty = dashesStyles[2]
            else:
                dashesSty = dashesStyles[1]
        qplt.plot(CU_S.coord('month'), CU_S, linestyle = '-', color= c_o, dashes=dashesSty, lw=linethick, label=expt, zorder = c_zorder)
    
    plt.ylim(-6,-16)
    plt.title(' ')
    plt.xticks(np.arange(12), mon_names, rotation=45)

    handles, labels = ax.get_legend_handles_labels()
    plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
    plt.legend(title='Dataset', bbox_to_anchor=(1.05, 2.3), loc='upper left')
    
    if save_plot:
        plt.savefig(starterpng+'AEJ_plot_'+expt+plot_file, bbox_inches='tight',dpi=100)

    else:
        iplt.show()
	
    return None
        
###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor models routine')

    green_list = create_greenlist(vari_list)
    green_list =obs_list+green_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list', green_list)

    for expt in green_list:
        print(expt)
        for vari in vari_list:

            CUN, CUS = load_expt(expt,vari)
	    
            pickle.dump(CUN, open(starterp+expt+'_'+vari+'_'+'CUN'+p_file, "wb" ))
            pickle.dump(CUS, open(starterp+expt+'_'+vari+'_'+'CUS'+p_file, "wb" ))
	    
        print('model data from '+expt+' pre-processed sucessfully')
             
###############################
#Calculation control
###############################

if processor_calculations:
    print('entering CALCULATION routines')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        for vari in vari_list:
	    
            cubeN_intensity, cubeS_intensity, N_latitude, S_latitude = calc_AEJ(expt, vari)
	    

            pickle.dump(cubeN_intensity, open(starterp+expt+'_'+'cubeN_intensity'+'_'+p_file, "wb"))
	    
            pickle.dump(cubeS_intensity, open(starterp+expt+'_'+'cubeS_intensity'+'_'+p_file, "wb"))
	    
            pickle.dump(N_latitude, open(starterp+expt+'_'+'N_latitude'+'_'+p_file, "wb"))	    
            pickle.dump(S_latitude, open(starterp+expt+'_'+'S_latitude'+'_'+p_file, "wb"))

	     
###############################
      
###############################
#Plotting control
###############################

if create_plot:

    print('entering PLOTTING routines')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    plot_AEJ(green_list)

    print('plotting complete')
         
###############################
#End of file
###############################		     


	
