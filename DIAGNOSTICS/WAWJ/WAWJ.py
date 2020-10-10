# -*- coding: utf-8 -*-
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
from config.find_files import *
from config.config import *
from config.config_functions import *
from WAWJ_config import *
from iris.cube import Cube
from matplotlib import patches
import math
from matplotlib.transforms import Bbox
import xarray as xa

###############################
# Unpickle files
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

    #Step by step: 1.1
    cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(0, 20) & pressure_level(expt, 92500) & year_bounds(1980, 2014))         
    cube = cube_concatenator(cube_list)    
    cube = cube.intersection(longitude=(-40, 10), ignore_bounds=True)
    return cube 

#####################################################################
#Calculation function(s)
#####################################################################

def WAWJ_Analysis(expt):
  
    ua = unpickle_cubes(starterp+expt+'_'+'ua'+'_'+p_file)
    va = unpickle_cubes(starterp+expt+'_'+'va'+'_'+p_file)

    #Step by step:1.2
    ua_clim = climatology(ua)
    va_clim = climatology(va)
    
    return ua_clim, va_clim
    
#####################################################################
#Plotting function(s)
#####################################################################
def calc_windspeed(ua_clim, va_clim):
    
    #ua_clim = unpickle_cubes(starterp+expt+'_'+'ua_clim'+'_'+p_file)
    #va_clim = unpickle_cubes(starterp+expt+'_'+'va_clim'+'_'+p_file)
    windspeed = (ua_clim ** 2 + va_clim ** 2) ** 0.5
    
        
    return windspeed
    
def bestfit_colrow(total=1):
    
    if (total/3.0) > 2:
        cols = 3
        rows = math.ceil(total/3.0)
    elif (total/2.0) > 1:
        cols = 2
        rows = math.ceil(total/2.0)
    else:
        cols =1
        rows =1
            
    return cols, rows
    
def get_max_zorder(ax):
    zder = 0
    
    if not(ax is None):
        axobjs = ax.get_children()
        zder = max((obj.zorder for obj in axobjs))
    
    return zder
    
def plot_WAWJ(green_list):

    total_plots = mon_list[mon2] - mon_list[mon1] + 1
    cols, rows = bestfit_colrow(total_plots)

    for expt in green_list:
        ua = unpickle_cubes(starterp+expt+'_'+'ua_clim'+'_'+p_file)
        col_no = 0
        row_no = 0
	
        if expt in obs_list: #keep 6 obs to 1 model ratio
            xskip = 12
            yskip = 12
        else:
            xskip = 2
            yskip = 2

        fig, axs = plt.subplots(cols, rows, subplot_kw={'projection': ccrs.PlateCarree()})
        fig.suptitle(mon1+' to '+mon2+' ' +expt+' '+'wind vector')

        for mon in ua.coord('month').points:
           mon_number=mon_list[mon]
            
           #Step by step 1.4
           if mon_number >= mon_list[mon1] and mon_number <= mon_list[mon2]: 

              ua_clim = unpickle_cubes(starterp+expt+'_'+'ua_clim'+'_'+p_file)
              va_clim = unpickle_cubes(starterp+expt+'_'+'va_clim'+'_'+p_file)

              Ctim_0 = iris.Constraint(month=mon)
              ua_clim=ua_clim.extract(Ctim_0)
              va_clim=va_clim.extract(Ctim_0)

              x = ua_clim.coord('longitude').points
              y = ua_clim.coord('latitude').points

              xm, ym = np.meshgrid(x, y)
              u = ua_clim.data
              v = va_clim.data
              current_ax=axs[col_no, row_no] # in makinde's code this is row_no, col_no L227 WAWJ_plot_helper

              extent = [-40, 10, 0, 20]
              windspeed = calc_windspeed(ua_clim, va_clim)
             # iplt.contourf(windspeed)
              zder = 1
              #pf.plot_contour(m_ucube, ax=current_ax, fill=True, overlay=True, shw_labels=False, shw_key=True, shw_title=False, shw_plt=False)
              current_ax.contourf(xm, ym, windspeed.data, antialiased=True,zorder= zder)                   
              #iplt.contour(windspeed, row=row_no, col=col_no)
              #cp = axs[col_no, row_no].contourf(windspeed)

             # if expt in obs_list:
               #   arrow_scale = 2*scale_fact* max([xskip, yskip])
             # else:
                #  arrow_scale = scale_fact* max([xskip, yskip])

              #Step by step 1.5
              
              qv = axs[col_no, row_no].quiver(xm[::xskip, ::xskip], ym[::yskip, ::yskip], u[::xskip, ::xskip], v[::yskip, ::yskip], pivot='middle', units='inches', minlength=0, zorder=2)#scale=arrow_scale, minlength=0)
              axs[col_no, row_no].quiverkey(qv, 0.95, 1.05, scale_fact, r'$2 \frac{m}{s}$', labelpos='E', coordinates='axes')
              axs[col_no, row_no].set_xlabel('Longitude (°)', labelpad=20)
              axs[col_no, row_no].set_ylabel('Latitude (°)', labelpad=20)

              meridians = np.arange(extent[0], extent[1] + lon_step, lon_step)
              parallels = np.arange(extent[2], extent[3] + lat_step, lat_step)
              axs[col_no, row_no].grid()
              axs[col_no, row_no].set_xlim([extent[0], extent[1]])
              axs[col_no, row_no].set_ylim([extent[2], extent[3]])

              #axs[col_no, row_no].set_yticks(parallels)
              #axs[col_no, row_no].set_yticklabels(parallels)
              #axs[col_no, row_no].set_xticks(meridians)
              #axs[col_no, row_no].set_xticklabels(meridians)
              axs[col_no, row_no].add_feature(cfeature.BORDERS)
              axs[col_no, row_no].add_feature(cfeature.COASTLINE)

              title = mon
              axs[col_no, row_no].title.set_text(title)

              change_row = True
     
           else:
               change_row = False

           if change_row:
               row_no = row_no + 1              
               if row_no == rows:
                  row_no = 0
                  col_no = col_no + 1 
            
        if save_plot:
            plt.savefig(starterpng+'_vector_plot_'+expt+plot_file, bbox_inches='tight',dpi=400)
        else:
            plt.show() 
 
###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor routine')
   
    #green_list = create_greenlist(vari_list)
    green_list =obs_list#+green_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list', green_list)

    for expt in green_list:   
        for vari in vari_list:

            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+'_'+p_file, "wb" ))

if processor_calculations:
    print('entering calculation routine')

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        ua_clim, va_clim = WAWJ_Analysis(expt)
        pickle.dump(ua_clim, open(starterp+expt+'_ua_clim_'+p_file, "wb" ))
        pickle.dump(va_clim, open(starterp+expt+'_va_clim_'+p_file, "wb" ))
       

if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)

    plot_WAWJ(green_list)
    print('Plotting complete')
    
