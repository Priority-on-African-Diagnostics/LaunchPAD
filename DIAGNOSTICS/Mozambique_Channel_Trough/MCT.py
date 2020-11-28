# -*- coding: utf-8 -*-

###############################
# Start of file:
#
# Mozambique Channel Trough (MCT)
# MCT index defined as the area averaged of the relative vorticity
# in the south Mozambique Channel
# 
# Author(s): 
# Rondro Barimalala (University of Cape Town) : rondrotiana.barimalala@uct.ac.za
# Thomas Webb (University of Oxford): thomas.webb@ouce.ox.ac.uk
# 
# Based on diagnostic scripts from Rondro Barimalala
# calculation of MCT
###############################

#################################
# Import required libraries
#################################

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
from MCT_config import *
from windspharm.iris import VectorWind

from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from pylab import *

################################

###############################
#unpickle files
###############################
    
def unpickle_cubes(path):
    """Load cube list from path."""
    with open(path, 'rb') as fh:
        cubes = pickle.load(fh)
    return cubes
    
################################

###############################
#Extraction function(s)
###############################

def load_expt(expt, vari):
     CL = iris.load(monthly_file_location(expt, vari), pressure_level(expt, 85000) & year_bounds(1980, 2006))
     CU = cube_concatenator(CL)
     
     return CU

################################

###############################
#Calculation function(s)
###############################

def calc_MCT(expt):

     #assign ua and va stored cubes
 
     ua = unpickle_cubes(starterp+expt+'_'+'ua'+p_file)
     va = unpickle_cubes(starterp+expt+'_'+'va'+p_file) 
     
     ua.data[ua.data > 2000] = 0.0
     va.data[va.data > 2000] = 0.0
     
     ua=climatology(ua)
     va=climatology(va) 
     
     delta_latitude = 180/180.0
     sample_points = [('longitude', ua.coord('longitude').points),('latitude',  np.linspace(90 - 0.5 * delta_latitude,-90 + 0.5 * delta_latitude,180))]
     ua_r = ua.interpolate(sample_points, iris.analysis.Linear())
     va_r = va.interpolate(sample_points, iris.analysis.Linear())
       
     wa = VectorWind(ua_r,va_r)

     xi = wa.vorticity()
     
     xi=xi.extract(lat_bounds(-26, -16) & lon_bounds(35, 44))
          
     xi = xi.collapsed(['longitude', 'latitude'],iris.analysis.MEAN)

     return xi

################################

###############################
#Plotting function(s)
###############################

def plot_MCT(green_list):

     CEDA_green = True

     fig, ax = plt.subplots()
     NUM_COLORS = len(green_list)
     
     plt.rc('font', family='serif')
     plt.rc('xtick', labelsize='x-small')
     plt.rc('ytick', labelsize='x-small')

     clist = len(green_list)
     len_clist = int(ceil(len(green_list) /3.0))   
     cm = plt.get_cmap('gist_rainbow', len_clist)
        
     colourWheel=[]
     for i in range(len_clist):
         rgb = cm(i)[:3] # will return rgba, we take only first 3 so we get rgb
         colourWheel.append(str(matplotlib.colors.rgb2hex(rgb)))
     
     dashesStyles = [[3,1],
            [1000,1],
            [2,1,10,1],
            [4, 1, 1, 1, 1, 1]]
     
     for j, expt in enumerate(green_list):
         

         xi = unpickle_cubes(starterp+expt+'_'+'_'+p_file)
         xi2=iris.analysis.maths.multiply(xi,1e6)

         if CEDA_green:
             if expt not in obs_list:
                 alphaVal = 1.0
                 linethick = 1.5
                 if j >= len_clist and j < 2*len_clist:
                     k = j - len_clist
                     dashesSty = dashesStyles[0]
                 elif j >= 2*len_clist:
                     k = j - 2*len_clist
                     dashesSty = dashesStyles[2]
                 else:
                     k=j
                     dashesSty = dashesStyles[1]
                 c_o = colourWheel[k%len(colourWheel)]
                 c_zorder=j

     
         if expt in obs_list:
             alphaVal = 1.0
             dashesSty = ''
             linethick = 2.5
             c_o = '#000000'
             c_zorder = clist + 1

         lines = plt.plot(mon_names, xi2.data,
                linestyle = '-',
                color= c_o,
                dashes=dashesSty,
                lw=linethick,
                label=expt,
                alpha=alphaVal, zorder = c_zorder)    
     
     ax.set_xlabel('')
     plt.xlim('Jan', 'Dec')
     ax.yaxis.set_major_formatter(ScalarFormatter())
     ax.yaxis.major.formatter._useMathText = True
     ax.yaxis.set_minor_locator(  AutoMinorLocator(5))
     #ax.xaxis.set_minor_locator(  AutoMinorLocator(5))
     ax.yaxis.set_label_coords(0.63,1.01)
     ax.yaxis.tick_left()

     nameOfPlot = 'Mozambique Channel Trough (Rondrotiana Barimalala)'
     plt.title(nameOfPlot)
     plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
     plt.legend(title='Dataset', bbox_to_anchor=(1.05, 1), loc='upper left')
  
     if save_plot:
         plt.savefig(starterpng+'MCT_plot_'+plot_file, bbox_inches='tight',dpi=100)
     else:
         plt.show()
     plt.clf() 
    	 
     return None

######################################

###############################
#main execution
###############################

if pre_processor_experiments:
    print('entering PRE-PROCESSOR models routine')
   
###############################
#extraction control
###############################
    green_list = create_greenlist(vari_list)
    green_list = green_list + obs_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" )) 
    for expt in green_list:
        for vari in vari_list:
             pickle.dump(load_expt(expt,vari), open(starterp+expt+'_'+vari+p_file, "wb" ))
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
            print(expt)        

            cube_return = calc_MCT(expt)
            pickle.dump(cube_return, open(starterp+expt+'_'+'_'+p_file, "wb"))

        print('data from '+expt+' calculated sucessfully')              
     
###############################
#plot control
###############################
if create_plot:
    print('entering PLOTTING routine')
    green_list =  unpickle_cubes(starterp+'green_list'+p_file)
    
    plot_MCT(green_list)

    print('data plotted sucessfully')
	 
###############################
#End of file
###############################
