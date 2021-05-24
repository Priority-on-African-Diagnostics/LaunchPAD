# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Ellen Dyer
# Contact: thomas.webb@ouce.ox.ac.uk
# calculation of Central African zonal winds diagnostic
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
from CAF_config import *
from scipy.stats import spearmanr
from numpy.polynomial.polynomial import polyfit
from matplotlib.patches import Rectangle
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

    if vari == 'ua':
      cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(latS, latN) & \
                            lon_bounds(lonW, lonE) & \
                            pressure_level(expt, press) & year_bounds(yearStart, yearEnd))
    if vari == 'pr':
      cube_list = iris.load(monthly_file_location(expt, vari), lat_bounds(latS, latN) & \
                            lon_bounds(lonW, lonE) &  year_bounds(yearStart, yearEnd))
    cube = cube_concatenator(cube_list)

    return cube

###############################
#Calculation function(s)
###############################

def calc_bias(expt,obs,mon):

    #monon select
    obs_mon = obs.extract(iris.Constraint(month=mon))
    expt_mon = expt.extract(iris.Constraint(month=mon))

    #regrid observations to CMIP6 model data
    mod_regrid = expt_mon.regrid(obs_mon, iris.analysis.Linear())

    #calculate anomoly
    bias = mod_regrid - obs_mon

    return bias

def calc_caf_diag(cube,mon):

    #monon select
    cube_mon = cube.extract(iris.Constraint(month=mon))

    diag_constraint_lat = iris.Constraint(latitude=lambda cell: latSa < cell < latNa)
    diag_constraint_lon = iris.Constraint(longitude=lambda cell: lonWa < cell < lonEa)
    cube_mon = cube_mon.extract(diag_constraint_lat & diag_constraint_lon)    
    caf_diag = cube_mon.collapsed(['latitude','longitude'], iris.analysis.MEAN)#, weights=grid_areas)

    return caf_diag

def calc_pr_diag(cube,mon):

    #monon select
    cube_mon = cube.extract(iris.Constraint(month=mon))

    diag_constraint_lat = iris.Constraint(latitude=lambda cell: latSb < cell < latNb)
    diag_constraint_lon = iris.Constraint(longitude=lambda cell: lonWb < cell < lonEb)
    cube_mon = cube_mon.extract(diag_constraint_lat & diag_constraint_lon)    
    pr_diag = cube_mon.collapsed(['latitude','longitude'], iris.analysis.MEAN)#, weights=grid_areas)

    return pr_diag

###############################
#Plotting function(s)
###############################

def plot_CAF(expt,months):

    if expt is not bias_obs:
      plt.figure(figsize=(5, 4))
      clevs = np.arange(-3,3.5,0.5)
  
      for mon in months:
        bias = unpickle_cubes(starterp+expt+'_caf_bias_'+mon+p_file)
  
        plt.subplot(2,2,months.index(mon)+1)
        ax = plt.axes(projection=crs.PlateCarree(0))
        cf = iplt.contourf(bias,clevs,cmap='PRGn',extend='both')
        plt.gca().coastlines()
        plt.gca().add_feature(cfeature.BORDERS,linewidth=0.2)
        plt.gca().set_extent((lonW,lonE,latS+1,latN-1))
        plt.gca().add_patch(Rectangle((lonWa,latSa),lonEa-lonWa,latNa-latSa,linewidth=1,
                            edgecolor='yellow',facecolor='none'))
        plt.gca().add_patch(Rectangle((lonWb,latSb),lonEb-lonWb,latNb-latSb,linewidth=1,
                            edgecolor='blue',facecolor='none'))
        gl = ax.gridlines(crs=crs.PlateCarree(), draw_labels=True,
                    linewidth=2, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False

        plt.title(mon)
  
        colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
        colorbar = plt.colorbar(cf, colorbar_axes, orientation='vertical')
        colorbar.set_label('m/s')
        plt.suptitle(expt+' 700 hPa CAF bias')
    
        if save_plot:
         
           plt.savefig(starterpng+expt+'_'+mon+plot_file, bbox_inches='tight',dpi=200)
           #plt.show()
           plt.clf()
           plt.close()

    return None

def plot_scatter(mon):

    shape=[".","o","v","^","<","8","s",">","p","P","*","h",
    "+","X","d","x","D","H","3","1","o","v","^","<",
    ".","o","v","^","<","8","s",">","p","P","*","h",
    "+","X","d","x","D","H","3","1","o","v","^","<"]
    colors = plt.matplotlib.cm.viridis(np.linspace(0,1,len(green_list)))


    pr_list = []
    caf_list = []
    for expt in green_list:

      caf_expt = unpickle_cubes(starterp+expt+'_caf_diag_'+mon+p_file)
      pr_expt = unpickle_cubes(starterp+expt+'_pr_diag_'+mon+p_file)
  
      if expt in obs_list:
        if expt == 'ERA5':
          pr_expt = pr_expt*1000.
        if expt == 'MERRA2':
          pr_expt = pr_expt*86400.
        plt.scatter(pr_expt.data,caf_expt.data,color=['coral'],s=[90],\
                    marker=shape[green_list.index(expt)],label=expt)
      else:
        pr_expt = pr_expt*86400.
        plt.scatter(pr_expt.data,caf_expt.data,color=colors[green_list.index(expt)],s=[50],\
                    marker=shape[green_list.index(expt)],label=expt)
        pr_list.append(pr_expt.data)
        caf_list.append(caf_expt.data)


    correl = spearmanr(pr_list,caf_list)
    print(correl)
    sc = correl[0]

    sy = caf_list
    sx = pr_list
    z = polyfit(sx,sy, 1)
    p = np.poly1d([z[1],z[0]])
    sx = np.arange(np.min(sx),np.max(sx)+(np.max(sx)-np.min(sx))/10,(np.max(sx)-np.min(sx))/10)
    plt.plot(sx, p(sx), '--',color='black',label='r='+"{:<.3f}".format(sc)+', p<0.01')

    plt.legend(bbox_to_anchor=(1.1, 1.05),ncol=2)
    #plt.ylim(-9,-1.8)
    #plt.xlim(0.5,8.5)
    plt.xlabel('pr (mm/day)')
    plt.ylabel('CAF zonal wind (m/s)')
    plt.title(mon)

    #if correl[1] <= 0.01:
    plt.savefig(starterpng+'ALL_SCATTER_'+mon+plot_file, bbox_inches='tight',dpi=200)
    #plt.show()
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
            print(vari)
            cube_return=load_expt(expt, vari)
            pickle.dump(cube_return, open(starterp+expt+'_'+vari+'_'+p_file, "wb" ))
            iris.io.save(cube_return, starternc+expt+'_'+vari+'_'+nc_file)
  
###############################
#Calculation control
###############################
if processor_calculations:
    print('entering calculation routine')

    obs_cube = unpickle_cubes(starterp+bias_obs+'_'+vari_list[0]+'_'+p_file)
    obs_cube = month_all(obs_cube)

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      print(expt)

      ua_cube = unpickle_cubes(starterp+expt+'_'+vari_list[0]+'_'+p_file)
      pr_cube = unpickle_cubes(starterp+expt+'_'+vari_list[1]+'_'+p_file)

      ua_cube = month_all(ua_cube)
      pr_cube = month_all(pr_cube)

      for mon in months:

        if expt is not bias_obs: 
          bias = calc_bias(ua_cube,obs_cube,mon)
         
        caf_diag = calc_caf_diag(ua_cube,mon)
  
        pr_diag = calc_pr_diag(pr_cube,mon)

        pickle.dump(bias, open(starterp+expt+'_caf_bias_'+mon+p_file, "wb" ))
        #iris.io.save(bias, starternc+expt+'_caf_bias_'+mon+nc_file)
        pickle.dump(caf_diag, open(starterp+expt+'_caf_diag_'+mon+p_file, "wb" ))
        #iris.io.save(caf_diag, starternc+expt+'_caf_diag_'+mon+nc_file)
        pickle.dump(pr_diag, open(starterp+expt+'_pr_diag_'+mon+p_file, "wb" ))
        #iris.io.save(pr_diag, starternc+expt+'_pr_diag_'+mon+nc_file)
     
###############################
#plot control
###############################
if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      plot_CAF(expt,months)
    
    for mon in months:
      plot_scatter(mon)

    print('plotting complete')
 
###############################
#End of file
###############################

