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
from config.find_files import level1_6hr
from config.config import *
from config.config_functions import *
from WAHL_config import *

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

     C_tim1 = iris.Constraint(time=lambda cell: cell.point.hour == 6)

     if expt in mod_list:
       cube_list = iris.load(sixhr_file_location(expt, vari), lat_bounds(-10, 40) & year_bounds(1983, 2012) & C_tim1)
       print(cube_list)
       print(expt)      
       cube = cube_concatenator(cube_list)
       cube = cube.intersection(longitude=(-25, 30))
       
     else:
       cube_list = iris.load(sixhr_file_location(expt, vari), lat_bounds(-10, 40) & lon_bounds(-25, 30) & year_bounds(1983, 2012) & C_tim1)
       print(cube_list)
       print(expt)
       cube = cube_concatenator(cube_list)
       
     Cube0 = cube.extract(pressure_level(expt, 70000))
     Cube1 = cube.extract(pressure_level(expt, 92500))  
     
     return Cube0, Cube1

###############################
#Calculation function(s)
###############################

def calc_WAHL(Cube1, Cube2):

     #calculate difference in geopotential thickness
     #ERA5: Geopotential = geopotential height*9.80665 but difference is still the same
     Cube3 = Cube1 - Cube2
     
     #create a new coordinate for month name
     iris.coord_categorisation.add_month(Cube3, 'time', name='month') 
     
     #average by month = LLAT
     Cube4 = Cube3.aggregated_by('month', iris.analysis.MEAN)

     #calculate 90th% over area (i.e. per month)
     Cube5 = Cube4.collapsed(['longitude','latitude'], iris.analysis.PERCENTILE, percent=[90])
     
     #monthly LLAT (Cube4) minus 90th% over area for each month (Cube5)
     result = iris.analysis.maths.subtract(Cube4, Cube5[0]) 
     
     #mask where cube data is not positive
     result.data = np.ma.masked_where(result.data <= 0, result.data)
     
     return result

###############################
#Plotting function(s)
###############################

def plot_WAHL(Cube0, mod):

     plt.figure(figsize=(12, 6), dpi=100)
			      
     #iterate over monthly lat-lon slices
     for Cube1 in Cube0.slices(['latitude','longitude']):
     
          #get month number (in year) from month
          month = Cube1.coord('month').points[0]
          mon_num = int(mon_list[month])
          plt.subplot(4,3,mon_num)
	  
          cf=iplt.contourf(Cube1, 20)
	  
          plt.title(month)
          plt.gca().coastlines()
          ax = plt.axes(projection=ccrs.PlateCarree())
          ax.add_feature(cfeature.BORDERS)
	  
	  #this ignores all data we have outside our domain of interest
          plt.gca().set_extent((-25,30,-10,40))
	  
     colorbar_axes = plt.gcf().add_axes([0.95, 0.2, 0.005, 0.7])	  
     colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
     colorbar.set_label('m')
     
     plt.suptitle('WAHL @ 0600 for '+mod+' 1983-2012 (m) ')
     
     if save_plot:
     
         # Save figure to png file
         plt.savefig(WAHL_starterpng+mod+WAHL_plot_file, bbox_inches='tight',dpi=100)
     
     else:
         iplt.show()

     # Clear the figure (for looping)
     plt.clf()

###############################
#main execution
###############################

if pre_processor_experiments:
    print('entering PRE-PROCESSOR models routine')
   
###############################
#extraction control
###############################
    #green_list = create_greenlist6hr(vari_list)
    green_list = obs_list#green_list + obs_list
    #green_list.remove('NorESM2-MM')
    pickle.dump(green_list, open(starterp+'white_list'+p_file, "wb" )) 
    for expt in green_list:
        for vari in vari_list:
             cube_return1, cube_return2 = load_expt(expt, vari)
             pickle.dump(cube_return1, open(starterp+expt+'_dom1_'+vari+p_file, "wb" ))
             pickle.dump(cube_return2, open(starterp+expt+'_dom2_'+vari+p_file, "wb" ))
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
            Cube1 =  unpickle_cubes(starterp+expt+'_dom1_'+vari+p_file)
            Cube2 =  unpickle_cubes(starterp+expt+'_dom2_'+vari+p_file)        

            #calculate WAHL
            result = calc_WAHL(Cube1, Cube2)
            pickle.dump(result, open(starterp+expt+'_WAHL_'+p_file, "wb"))

        print('data from '+expt+' calculated sucessfully')              
     
###############################
#plot control
###############################
if create_plot:
    print('entering PLOTTING routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
        result =  unpickle_cubes(starterp+expt+'_WAHL_'+p_file)
        plot_WAHL(result, expt)
        print('data from '+expt+' plotted sucessfully')
	 
###############################
#End of file
###############################

