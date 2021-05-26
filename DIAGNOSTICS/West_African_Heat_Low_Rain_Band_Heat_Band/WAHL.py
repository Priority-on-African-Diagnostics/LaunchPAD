# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Tom Webb
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Thompson Annor
# panel_plot_bias_plot_WA.ncl, WAHL.sh and LLAT-1.sh
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

from config.find_files import *
from config.config import *
from WAHL_config import *
from config.config_functions import *
import cf_units as unit

from matplotlib import cm
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

     cube_list = iris.load(sixhr_file_location(expt, vari), lat_bounds(-10, 40) & year_bounds(1983, 2012) & time_bound_six(expt))
     print(cube_list)
     cube = cube_concatenator(cube_list)
     cube = cube.intersection(longitude=(-25, 30),ignore_bounds=True)
     cube1 = cube.extract(pressure_level(expt,70000))
     cube2 = cube.extract(pressure_level(expt,92500))
     
     return cube1, cube2

###############################
#Calculation function(s)
###############################

def calc_WAHL(expt, vari):

     Cube1 = unpickle_cubes(starterp+expt+'_high_'+vari+p_file)
     Cube2 = unpickle_cubes(starterp+expt+'_low_'+vari+p_file)

     #calculate difference in geopotential thickness
     #ERA5: Geopotential = geopotential height*9.80665 
     Cube3 = Cube1 - Cube2
     if expt=='ERA-Interim' and vari =='zg':
         Cube3 = Cube3 / 9.80665
     
     #create a new coordinate for month name
     iris.coord_categorisation.add_month(Cube3, 'time', name='month') 
     
     #average by month = LLAT
     Cube4 = Cube3.aggregated_by('month', iris.analysis.MEAN)

     result = Cube4
     
     return result
     
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

###############################
#Plotting function(s)
###############################

def plot_WAHL(expt, vari):

     Cube0 = unpickle_cubes(starterp+expt+'_'+vari+'_'+p_file)

     cmap_zg = cm.get_cmap('jet', 30) 
     cmap_hb = cm.get_cmap('jet', 8)
     cmap_pr = cm.get_cmap('Blues', 150)
     
     arr_zg=[]
     arr_hb=[]
     arr_pr=[]
     
     arr_zg.append('#ffffff')
     arr_zg.append('#ffffff')
     arr_hb.append('#ffffff')
     arr_pr.append('#ffffff')
   
     for i in range(cmap_zg.N):
         rgb = cmap_zg(i)[:3] 
         arr_zg.append(matplotlib.colors.rgb2hex(rgb))
	 
     for i in range(cmap_hb.N):
         rgb = cmap_hb(i)[:3] 
         arr_hb.append(matplotlib.colors.rgb2hex(rgb))
	 
     for i in range(cmap_pr.N):
         rgb = cmap_pr(i)[:3] 
         arr_pr.append(matplotlib.colors.rgb2hex(rgb))
	 
     plt.figure(figsize=(6, 6))
     clevs_zg = np.arange(0,30,1)
     clevs_pr = np.arange(0,150,1)
     clevs_hb = np.arange(0,9,1)
     
     cols, rows = bestfit_colrow(12)
     lon_step = 10
     lat_step = 10
     
     col_no = 0
     row_no = 0
 
     vari_line ='WAHL'
     si_line='m'
     
     fig, axs = plt.subplots(cols, rows, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(10, 10))
     fig.suptitle(vari_line+' @ 0600 for '+expt+' 1983-2012 '+si_line)

     for counter, Cube1 in enumerate(Cube0.slices(['latitude','longitude'])):
     
             #calculate 90th% over area (i.e. per month)
         Cube90 = Cube1.collapsed(['longitude','latitude'], iris.analysis.PERCENTILE, percent=[90]) 
	     #subtract from LLAT
         Cube1 = iris.analysis.maths.subtract(Cube1, Cube90[0])
	     #threshold of 2 m
         Cube1.data = np.ma.masked_where(Cube1.data <= 2, Cube1.data) 
	     
         month = Cube1.coord('month').points[0]
	
         x = Cube1.coord('longitude').points
         y = Cube1.coord('latitude').points

         xm, ym = np.meshgrid(x, y)
      
         #plt.subplot(3,4,counter+1)
         current_ax=axs[col_no, row_no] 
	
         cf = current_ax.contourf(xm, ym,np.array(Cube1.data),clevs_zg,colors=arr_zg,extend='both')
	 
         extent = [-25, 30, -10, 40]
	 
         if col_no == 2:
             axs[col_no, row_no].set_xlabel('Longitude (°)', labelpad=20)
         if row_no == 0:
             axs[col_no, row_no].set_ylabel('Latitude (°)', labelpad=20)

         meridians = np.arange(extent[0], extent[1] + lon_step, lon_step)
         parallels = np.arange(extent[2], extent[3] + lat_step, lat_step)
         axs[col_no, row_no].grid()
         axs[col_no, row_no].set_xlim([extent[0], extent[1]])
         axs[col_no, row_no].set_ylim([extent[2], extent[3]])

         axs[col_no, row_no].set_yticks(parallels)
         axs[col_no, row_no].set_yticklabels(parallels)
         axs[col_no, row_no].set_xticks(meridians)
         axs[col_no, row_no].set_xticklabels(meridians)
         axs[col_no, row_no].add_feature(cfeature.BORDERS)
         axs[col_no, row_no].add_feature(cfeature.COASTLINE)
        # axs[col_no, row_no].add_feature(cfeature.LAND, facecolor='#808080', zorder=1)
         axs[col_no, row_no].set_extent((-25, 30, -10, 40))
	      

         title = month
         axs[col_no, row_no].title.set_text(title)
	 
         row_no = row_no + 1              
         if row_no == rows:
             row_no = 0
             col_no = col_no + 1 

     colorbar_axes = plt.gcf().add_axes([0.25, 0.03, 0.5, 0.025])
     colorbar = plt.colorbar(cf, colorbar_axes, orientation='horizontal')
     #plt.suptitle() 

     if save_plot:
     
         plt.savefig(starterpng+expt+'_'+vari_line+'_'+plot_file, bbox_inches='tight',dpi=100)
     else:
         plt.show()
       
     plt.clf()	 
     
     return None
     
###############################
#main execution
###############################
if pre_processor_experiments:

    print('entering pre-processor models routine')
   
###############################
#extraction control
###############################
    green_list = create_greenlist6hr(vari_list)
    green_list = green_list + obs_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    
    for expt in green_list:   
      for vari in vari_list:
          cube1, cube2 = load_expt(expt, vari)
          pickle.dump(cube1, open(starterp+expt+'_high_'+vari+p_file, "wb" ))
          pickle.dump(cube2, open(starterp+expt+'_low_'+vari+p_file, "wb" ))
      print('data from '+expt+' pre-processed sucessfully')
   
###############################
#calculation control
###############################

if processor_calculations:
    print('entering CALCULATION models routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:  
        for vari in vari_list:        

            cube = calc_WAHL(expt, vari)
	    
            pickle.dump(cube, open(starterp+expt+'_'+vari+'_'+p_file, "wb"))

        print('data from '+expt+' calculated sucessfully')              
     
###############################
#plot control
###############################
if create_plot:
    print('entering PLOTTING routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list: 
        for vari in vari_list:  
            plot_WAHL(expt,vari)

    print('data plotted sucessfully')

###############################
#End of file
###############################

