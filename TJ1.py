# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Ellen Dyer, Oscar Lino
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Oscar Lino
# calculation of Turkana Jet diagnotstic 1
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
from config.find_files import *
from config.config import *
from config.config_functions import *
from TJ1_config import *
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

    cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(-7, 8) & lon_bounds(30, 45) & pressure_level(expt, 85000) & year_bounds(1980, 2014))
    cube = cube_concatenator(cube_list)

    return cube

###############################
#Calculation function(s)
###############################

def scalar_mflx(expt,ua,va,hus):

    if expt is not 'ERA5': 
      #era5 cube
      era5 = unpickle_cubes(starterp+'ERA5_ua'+p_file)
  
      #regrid to era5 grid
      ua = ua.regrid(era5, iris.analysis.Linear())
      va = va.regrid(era5, iris.analysis.Linear())
      hus = hus.regrid(era5, iris.analysis.Linear())

    #calculate scalar wind
    windspeed = (ua ** 2 + va ** 2) ** 0.5

    #calculate mflux (conv hus to g/kg)
    mflx = windspeed*hus*1000

    return  ua, va, mflx

def vars_clim(ua,va,mflx):
   
    ua_clim = climatology(ua)
    va_clim = climatology(va)
    mflx_clim = climatology(mflx)

    return ua_clim, va_clim, mflx_clim

def mask_wind(ua,va):

    thresh = 5

    ua_masked = xr.DataArray.from_iris(ua)
    va_masked = xr.DataArray.from_iris(va)

    #calculate scalar wind
    windspeed = (ua_masked ** 2 + va_masked ** 2) ** 0.5

    ua_masked = ua_masked.where(windspeed>thresh)
    va_masked = va_masked.where(windspeed>thresh)

    ua_masked = ua_masked.to_iris()
    va_masked = va_masked.to_iris()

    return ua_masked, va_masked
    

###############################
#Plotting function(s)
###############################

def plot_TJ1(expt):


    ua = unpickle_cubes(starterp+expt+'_ua_clim'+p_file)
    va = unpickle_cubes(starterp+expt+'_va_clim'+p_file)
    mflx = unpickle_cubes(starterp+expt+'_mflx_clim'+p_file)

    plt.figure(figsize=(6, 6))
    clevs = np.arange(0,102,1)

    for mon in mon_names:

      ua_mon = ua.extract(iris.Constraint(month=mon))
      va_mon = va.extract(iris.Constraint(month=mon))
      mflx_mon = mflx.extract(iris.Constraint(month=mon))

      x = ua_mon.coord('longitude').points
      y = ua_mon.coord('latitude').points

      xm, ym = np.meshgrid(x, y)
      u = ua_mon.data
      v = va_mon.data
 
      xskip = 4
      yskip = 4
      scale_fact = 10
      arrow_scale = scale_fact*xskip*1.5
      
      plt.subplot(3,4,mon_names.index(mon)+1)
      cf = iplt.contourf(mflx_mon,clevs,cmap='coolwarm',extend='both')
      qv = plt.quiver(xm[::xskip, ::xskip], ym[::yskip, ::yskip], u[::xskip, ::xskip], \
                v[::yskip, ::yskip], pivot='middle', units='inches', minlength=0,scale=arrow_scale,width=0.0075)
      plt.quiverkey(qv, 0.9, 1.05, scale_fact, r'$10 \frac{m}{s}$', labelpos='E',fontproperties={'size': 7})
      plt.gca().coastlines()
      plt.gca().add_feature(cfeature.BORDERS,linewidth=0.2)
      plt.gca().set_extent((32,43,-5,6))
      plt.title(mon)

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
    colorbar.set_label('$\overline{qV} (g/Kg/ms^{-1}$)')
    plt.suptitle(expt+' TJ1 ')

    if save_plot:
     
       plt.savefig(starterpng+expt+plot_file, bbox_inches='tight',dpi=200)
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
        for vari in vari_list:
            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+p_file, "wb" ))
       
  
###############################
#Calculation control
###############################
if processor_calculations:
    print('entering calculation routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      print(expt)

      ua_cube = unpickle_cubes(starterp+expt+'_ua'+p_file)
      va_cube = unpickle_cubes(starterp+expt+'_va'+p_file)
      hus_cube = unpickle_cubes(starterp+expt+'_hus'+p_file)

      ua_cube, va_cube, mflx = scalar_mflx(expt,ua_cube,va_cube,hus_cube)

      ua_clim, va_clim, mflx_clim = vars_clim(ua_cube,va_cube,mflx)

      ua_clim, va_clim = mask_wind(ua_clim,va_clim)

      pickle.dump(mflx_clim, open(starterp+expt+'_mflx_clim'+p_file, "wb" ))
    
      pickle.dump(ua_clim, open(starterp+expt+'_ua_clim'+p_file, "wb" ))
   
      pickle.dump(va_clim, open(starterp+expt+'_va_clim'+p_file, "wb" ))
    
     
###############################
#plot control
###############################
if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      print(expt)
      plot_TJ1(expt)
      
      

    print('plotting complete')
 
###############################
#End of file
###############################

