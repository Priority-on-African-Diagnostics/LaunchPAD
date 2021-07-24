# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Tom Webb
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Thierry Taguela
# SAH_LLWs_cmip5.ncl and walker_temp.grad_LLWs.ncl
###############################

###############################
#import required libraries
###############################
import os
import iris
import iris.coords
from pathlib import Path
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
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import xarray as xr

from LLWs_config import *
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

     if vari=='ua' or vari=='hus':
         cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-15, 15) \
                               & year_bounds(yearStart, yearEnd) & pressure_level(expt, pressLow))
         cube = cube_concatenator(cube_list)
         cube = cube.intersection(longitude=(-15, 15), ignore_bounds=True)
         cube = xr.DataArray.from_iris(cube)

     if vari=='wap':
         cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-10, 10) & \
                               year_bounds(yearStart, yearEnd) & pressure_level(expt, 85000)) 	          
         cube = cube_concatenator(cube_list)  
         cube = cube.intersection(longitude=(-10, 10), ignore_bounds=True) 
         cube = xr.DataArray.from_iris(cube)
 
     if vari=='ta':
         if expt=='ERA-Interim':
             cube_list=iris.load(monthly_file_location(expt, vari)+'925.nc', lat_bounds(-10, 10) \
                                 & year_bounds(yearStart, yearEnd))
         else:
             cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-10, 10) &\
                                   year_bounds(yearStart, yearEnd) & pressure_level(expt, 92500))       
         cube = cube_concatenator(cube_list) 
         cube = cube.intersection(longitude=(-10, 30), ignore_bounds=True) 
         cube = xr.DataArray.from_iris(cube)

     if vari=='psl':
         cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-50, -5) \
                               & year_bounds(yearStart, yearEnd))
         cube = cube_concatenator(cube_list)
         cube = cube.intersection(longitude=(-50, 20), ignore_bounds=True)
         cube = xr.DataArray.from_iris(cube)

     return cube

###############################
#Calculation function(s)
###############################

def sah_avg(expt):

     sah = unpickle_cubes(starterp+expt+'_'+'psl'+p_file)

     if expt in ['ERA5','ERA-Interim']:
       sah = sah.rename({'latitude':'lat'})
       sah = sah.rename({'longitude':'lon'})
       sah = sah.reindex(lat=sah.lat[::-1])

     sah = sah.sel(lat=slice(-40,-15),lon=slice(-40,10)).mean(dim=('lat','lon'))
     sah = sah.groupby('time.season').mean('time')
     sah = sah/100.0
   
     return sah

def ascent_avg(expt):

     ascent = unpickle_cubes(starterp+expt+'_'+'wap'+p_file)

     if expt in ['ERA5','ERA-Interim']:
       ascent = ascent.rename({'latitude':'lat'})
       ascent = ascent.rename({'longitude':'lon'})
       ascent = ascent.reindex(lat=ascent.lat[::-1])

     ascent = ascent.sel(lat=slice(-5,3),lon=slice(-2,8)).mean(dim=('lat','lon'))
     ascent = ascent.groupby('time.season').mean('time')
     ascent = ascent*100.0
   
     return ascent

def temp_gradient(expt):

     ta = unpickle_cubes(starterp+expt+'_'+'ta'+p_file)

     if expt in ['ERA5','ERA-Interim']:
       ta = ta.rename({'latitude':'lat'})
       ta = ta.rename({'longitude':'lon'})
       ta = ta.reindex(lat=ta.lat[::-1])
     
     EAO = ta.sel(lat=slice(-5,3),lon=slice(-2,8)).mean(dim=('lat','lon'))
     CA = ta.sel(lat=slice(-5,3),lon=slice(15,25)).mean(dim=('lat','lon'))

     EAO = EAO.groupby('time.season').mean('time')
     CA = CA.groupby('time.season').mean('time')

     grad = CA - EAO

     return grad

def moisture_flux(expt):

     ua = unpickle_cubes(starterp+expt+'_'+'ua'+p_file)
     hus = unpickle_cubes(starterp+expt+'_'+'hus'+p_file)

     if expt in ['ERA5','ERA-Interim']:
       ua = ua.rename({'latitude':'lat'})
       ua = ua.rename({'longitude':'lon'})
       ua = ua.reindex(lat=ua.lat[::-1])
       hus = hus.rename({'latitude':'lat'})
       hus = hus.rename({'longitude':'lon'})
       hus = hus.reindex(lat=hus.lat[::-1])

     #HadGEM3 had ua on a different grid than other variables
     #so this calculation is approached differently than other models
     #with values selected on each grid before calculating mflux
     if expt=='HadGEM3-GC31-LL':
       ua = ua.sel(lat=slice(-10,10),lon=slice(10,12.5)).mean(dim=('lat','lon'))
       hus = hus.sel(lat=slice(-10,10),lon=slice(10,12.5)).mean(dim=('lat','lon'))
       moisture_flux = ua*hus*1000.0
       moisture_flux = moisture_flux.groupby('time.season').mean('time')
     else:
       moisture_flux = ua*hus*1000.0
       moisture_flux = moisture_flux.sel(lat=slice(-10,10),lon=slice(10,12.5)).mean(dim=('lat','lon'))
       moisture_flux = moisture_flux.groupby('time.season').mean('time')

     return moisture_flux

    
###############################
#plot diagnostics
###############################
    
def plot_figure1(green_list):

     colour_list=['black','blue','orange','green','red','purple','brown',\
                  'pink','gold','gray','olive','cyan','navy','peru','rosybrown',\
                  'lime','teal','fuchsia','chartreuse','dodgerblue',\
                  'mediumseagreen','salmon','rebeccapurple']
     
     shape_list=["o","v","^","<",">","s","P","p","D","X","*","o","v","^",\
                 "<",">","s","P","p","D","X","*","o","v","^","<",">","s",\
                 "P","p","D","X","*"]

     moisture_flux = collections.OrderedDict()
     grad = collections.OrderedDict()
     wap = collections.OrderedDict()
     for expt in green_list:
         moisture_flux[expt] = unpickle_cubes(starterp+expt+'_mflux'+p_file)
         grad[expt] = unpickle_cubes(starterp+expt+'_'+'grad'+p_file)
         wap[expt] = unpickle_cubes(starterp+expt+'_'+'ascent'+p_file)

     for seas in seasons:
       fig, (ax1, ax2) = plt.subplots(2,figsize=(5,10))
       
       height=[] 
       y_pos = np.arange(len(green_list))
       for expt in green_list:
            mflux = moisture_flux[expt].sel(season=seasn[seas]).values.item()
            height.append(mflux)

       ax1.set(ylabel='Moisture Flux CA Western Boundary (g.Kg-1 m.s-1)')
       
       ax1.bar(y_pos, height,color=colour_list)
       ax1.set_xticks([])
       ax1.set_ylim(0.0, max(height)+5.0)
    
       
       box = ax1.get_position()
       ax1.set_position([box.x0, box.y0, box.width * 0.95, box.height])
       ax1.set_title(seasn[seas])
       
       gradl=[]
       wapl=[]
       for count, expt in enumerate(green_list):
         gradv = grad[expt].sel(season=seasn[seas]).values.item()
         wapv = wap[expt].sel(season=seasn[seas]).values.item()
         gradl.append(gradv)
         wapl.append(wapv)
  
         ax2.scatter(gradv, wapv, s=80, label=expt, \
                       marker=shape_list[count], color=colour_list[count])
        
       ax2.set(xlabel='Temperature gradient (K)', ylabel='Vertical velocity index (hPa s-1)')
       ax2.xaxis.set_minor_locator(MultipleLocator(0.1))
       ax2.yaxis.set_minor_locator(MultipleLocator(0.2))
       ax2.set_xlim(min(gradl)-0.2, max(gradl)+0.2)
       ax2.set_ylim(min(wapl)-0.2,max(wapl)+0.2)
       ax2.set_title(seasn[seas])
       
       box = ax2.get_position()
       ax2.set_position([box.x0, box.y0, box.width * 0.95, box.height])
    
       fig.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
       if save_plot:
           plt.savefig(starterpng+'llw_scatter'+'_'+seas+plot_file, bbox_inches='tight',dpi=200)
    
       else:
           iplt.show()
  
       plt.clf()
       plt.close()

     return None

def plot_figure2(green_list):


     moisture_flux = collections.OrderedDict()
     surface_pressure = collections.OrderedDict()
     for expt in green_list:
         moisture_flux[expt] = unpickle_cubes(starterp+expt+'_mflux'+p_file)
         surface_pressure[expt] = unpickle_cubes(starterp+expt+'_'+'sah'+p_file)

     for seas in seasons:

       height1=[]
       height2=[]
       y_pos = np.arange(len(green_list))
       width = 0.35

       fig, ax1 = plt.subplots()
  
       for expt in green_list:
         mflux = moisture_flux[expt].sel(season=seasn[seas]).values.item()
         sp = surface_pressure[expt].sel(season=seasn[seas]).values.item()
         height1.append(mflux)
         height2.append(sp)
    
       ax1.bar(y_pos - width/2, height1, width, color='blue')
       ax1.set_ylim(0,max(height1)+5.0)
       ax1.set_ylabel('Moisture Flux CA Western Boundary (g.Kg-1 m.s-1)', fontweight='bold', color = 'blue')
       ax1.set_title(seasn[seas])
    
       ax2 = ax1.twinx()
       ax2.bar(y_pos + width/2, height2, width, color='red')
       ax2.set_ylabel('Mean SAH (hPa)', fontweight='bold', color = 'red')
       ax2.set_ylim(1010, max(height2)+5.0)
    
       # Create names on the x-axis
       plt.xticks(y_pos)
       xticklabels = green_list
       ax1.set_xticklabels(xticklabels, rotation ='vertical')
    
  
       if save_plot:
           plt.savefig(starterpng+'sah_mflx'+'_'+seas+plot_file, bbox_inches='tight',dpi=100)
    
       else:
           iplt.show()
    
       plt.clf()
       plt.close()

     return None
  

###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor routine')
   
    green_list = create_greenlist(vari_list)
    green_list =  obs_list+green_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list',green_list)

    for expt in green_list:   
        for vari in vari_list:

            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+p_file, "wb" ))

if processor_calculations:
    print('entering calculation routine')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        print(expt)
        sah = sah_avg(expt)
        ascent = ascent_avg(expt)
        grad = temp_gradient(expt)
        mflux = moisture_flux(expt)
        pickle.dump(sah, open(starterp+expt+'_sah'+p_file, "wb" ))
        pickle.dump(ascent, open(starterp+expt+'_ascent'+p_file, "wb" ))
        pickle.dump(grad, open(starterp+expt+'_grad'+p_file, "wb" ))
        pickle.dump(mflux, open(starterp+expt+'_mflux'+p_file, "wb" ))

if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    plot_figure1(green_list)
    print('done Fig 1')
    plot_figure2(green_list)
    print('done Fig 2')

         
###############################
#End of file
###############################
