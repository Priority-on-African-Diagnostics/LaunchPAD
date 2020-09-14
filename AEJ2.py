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
     CLN = iris.load(monthly_file_location(expt, vari), lat_bounds(3, 20) & lon_bounds(lonWest, lonEast) & \
                     pressure_bounds(expt, press1, press2) & year_bounds(yearStart, yearEnd))
     CUN = cube_concatenator(CLN)
    
     CLS = iris.load(monthly_file_location(expt, vari), lat_bounds(-20, -5) & lon_bounds(lonWest, lonEast) & \
                     year_bounds(yearStart, yearEnd) & pressure_level(expt, press1))
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

def plot_AEJ(expt):
      
    plt.figure(figsize=(8, 6))

    plt.subplot(2,2,1)
    plt.title('North')
    LN = unpickle_cubes(starterp+expt+'_'+'N_latitude'+'_'+p_file) 
    plt.plot(mon_names, LN)
    plt.ylim(0,14)
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Latitude') 
        
    plt.subplot(2,2,2)
    plt.title('South')
    LS = unpickle_cubes(starterp+expt+'_'+'S_latitude'+'_'+p_file) 
    plt.plot(mon_names, LS)
    plt.ylim(-12,0)
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Latitude')
    
    plt.subplot(2,2,3) 
    CU_N = unpickle_cubes(starterp+expt+'_'+'cubeN_intensity'+'_'+p_file)
    qplt.plot(CU_N.coord('month'), CU_N)
    plt.ylim(-6,-16)
    plt.title(' ')
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Intensity (m/s)')    
   
    plt.subplot(2,2,4)
    CU_S = unpickle_cubes(starterp+expt+'_'+'cubeS_intensity'+'_'+p_file)
    qplt.plot(CU_S.coord('month'), CU_S)
    plt.ylim(-6,-16)
    plt.title(' ')
    plt.xticks(np.arange(12), mon_names, rotation=45)
    plt.ylabel('Intensity (m/s)')

    plt.subplots_adjust(wspace=0.4,hspace=0.3)
        
###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor models routine')

    green_list = ['HadGEM3-GC31-MM']#create_greenlist(vari_list)
    green_list =obs_list+green_list
    #green_list.remove('FIO-ESM-2-0')
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
            iris.io.save(cubeN_intensity, starternc+expt+'_'+'cubeN_intensity'+'_'+nc_file) 
	    
            pickle.dump(cubeS_intensity, open(starterp+expt+'_'+'cubeS_intensity'+'_'+p_file, "wb"))
            iris.io.save(cubeS_intensity, starternc+expt+'_'+'cubeS_intensity'+'_'+nc_file) 
	    
            pickle.dump(N_latitude, open(starterp+expt+'_'+'N_latitude'+'_'+p_file, "wb"))	    
            pickle.dump(S_latitude, open(starterp+expt+'_'+'S_latitude'+'_'+p_file, "wb"))

	     
###############################
      
###############################
#Plotting control
###############################

if create_plot:

    print('entering PLOTTING routines')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        print('processing model '+expt)
	
        plot_AEJ(expt)
	
        if save_plot:
            plt.savefig(starterpng+'AEJ_plot_'+expt+plot_file, bbox_inches='tight',dpi=100)

        else:
            iplt.show()
            plt.clf()
	
    print('plotting complete')
         
###############################
#End of file
###############################		     


	
