# -*- coding: utf-8 -*-
###############################
# Start of file:
# Author(s): Ellen Dyer, Paige Donkin
# Contact: thomas.webb@ouce.ox.ac.uk
# Based on diagnostic scripts from Paige Donkin
# plotting of cyclone tracking
###############################

###############################
#import required libraries
###############################

import os
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import sys
import pandas as pd
from scipy.stats import kde
import cartopy
import cartopy.crs as ccrs
import collections
import cartopy.crs as crs
import cartopy.feature as cfeature
from cartopy.mpl.geoaxes import GeoAxes
from mpl_toolkits.axes_grid1 import AxesGrid
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cloudpickle as pickle

from TRA_plot_config import *
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
#Extraction function(s)
###############################

def read_data(expt):

  if pickle_or_txt == 1:
    #For pickle files:
    pd_in  = unpickle_cubes(starterp+expt+'_df__TRA.p') 
    mod_pd = pd_in[['mslp','mslp_lon','mslp_lat','max_wspd','tc_event','tc_number']]
    mod_pd = mod_pd.rename(columns={"mslp_lon": "lon", "mslp_lat": "lat","max_wspd": "max_wind"})

  if pickle_or_txt == 2:
    #For text files:
    data=np.loadtxt(starterp+expt+'_tracking_output.txt',
           #dtype={'names': ('date','time','mslp', 'lon','lat','max_wind','vort','tc_event','tc_number'),
           #       'formats': ('U10', 'U10', np.float, np.float, np.float, np.float, np.float, 'U4', np.float)})
           dtype={'names': ('date','time','mslp', 'lon','lat','max_wind','tc_event','tc_number'),
                  'formats': ('U10', 'U10', np.float, np.float, np.float, np.float, 'U4', np.float)})

    mod_pd = collections.OrderedDict()
    mod_pd['mslp'] = data['mslp']
    mod_pd['lon'] = data['lon']
    mod_pd['lat'] = data['lat']
    mod_pd['max_wind'] = data['max_wind']
    mod_pd['tc_event'] = data['tc_event']
    mod_pd['tc_number'] = data['tc_number']
    mod_pd = pd.DataFrame(data=mod_pd)

  print(mod_pd)
  return mod_pd


###############################
#Calculation function(s)
###############################

def genesis_locations(pd_any):
#Returns lon&lat points for all genesis events

  lon_gen=pd_any['lon'][pd_any['tc_event'] == "New"].to_numpy()
  lat_gen=pd_any['lat'][pd_any['tc_event'] == "New"].to_numpy()

  return lon_gen,lat_gen

def max_lifetime_wspd(pd_any):
#Calculates the lifetime maximum windspeed for each TC event

  group = pd_any.groupby(['tc_number']).max()
  ml_wspd=group['max_wind']

  return ml_wspd

def spatial_corr(mod_array,ra_array):
#Calculates spatial correlation with respect to reanalysis 

  p = ra_array #independent (reanalysis)
  q = mod_array #dependent (model)
  pq = p*q
  pqmask = pq-pq # 0 or "missing" so all variables share the same missing
  pmasked = p + pqmask
  qmasked = q + pqmask
  pp = pmasked*pmasked
  qq = qmasked*qmasked

  pxave = pmasked.mean(axis=1)
  qxave = qmasked.mean(axis=1)
  pave = pxave.mean(axis=0)
  qave = qxave.mean(axis=0)
  pqxave = pq.mean(axis=1)
  ppxave = pp.mean(axis=1)
  qqxave = qq.mean(axis=1)
  pqave = pqxave.mean(axis=0)
  ppave = ppxave.mean(axis=0)
  qqave = qqxave.mean(axis=0)
  pvar = ppave - pave*pave
  qvar = qqave - qave*qave
  pqvar = pqave - pave*qave
  corr = pqvar/(pvar*qvar)**0.5 #Spatial correlation 

  return corr


###############################
#Plotting function(s)
###############################

def gen_plot(ml_wspd,lon_gen,lat_gen,cax):
#Creates genesis plot

  #Categorizes each genesis event based on the maximum lifetime intensity of the TC
  ts=np.where(ml_wspd <= 32)
  c1=np.where((ml_wspd > 32) & (ml_wspd <= 42))
  c2=np.where((ml_wspd > 42) & (ml_wspd <= 49))
  c3=np.where((ml_wspd > 49) & (ml_wspd <= 58))
  c45=np.where(ml_wspd > 58)

  xts, yts = lon_gen[ts],lat_gen[ts]
  xc1, yc1 = lon_gen[c1],lat_gen[c1]
  xc2, yc2 = lon_gen[c2],lat_gen[c2]
  xc3, yc3 = lon_gen[c3],lat_gen[c3]
  xc45, yc45 = lon_gen[c45],lat_gen[c45]

  #Plots scatter points with colour based on the maximum lifetime intensity of the TC
  #Creates list of handles for legend
  handles = []
  han1=cax.scatter(xts, yts, color='#89fe05', s=15, marker='o', label='Tropical Storm', edgecolors='black',zorder=5,linewidth=0.6)
  han2=cax.scatter(xc1, yc1, color='#fffd01', s=15, marker='o', label='Category 1', edgecolors='black',zorder=5,linewidth=0.6)
  han3=cax.scatter(xc2, yc2, color='#ff9408', s=15, marker='o', label='Category 2', edgecolors='black',zorder=5,linewidth=0.6)
  han4=cax.scatter(xc3, yc3, color='#ff5b00', s=15, marker='o', label='Category 3', edgecolors='black',zorder=5,linewidth=0.6)
  han5=cax.scatter(xc45, yc45, color='#ec2d01', s=15, marker='o', label='Category 4', edgecolors='black',zorder=5,linewidth=0.6)
  if not handles:
    handles = [han1,han2,han3,han4,han5]

  return handles

def track_plot(pd_any,cax):
#Creates track plot

  #Groups TCs into individual events based on the group number
  group=pd_any.groupby(['tc_number'])

  for group_number,group_data in group: #Here, the first item we mention (here: i) will always give us the group numbers / headings.
    x=group_data['lon'].to_numpy() #longitude
    y=group_data['lat'].to_numpy() #latitude
    wind=group_data['max_wind'].to_numpy() #windspeed
    nk=len(x)
    for k in range(0,nk):
      kp1 = k+1
      if(kp1 >= nk): kp1 = nk-1
      #Plots lines based on intensity category (wrt windspeed - based on the Saffir Simpson scale)
      if(wind[k] <= 32): cax.plot((x[k],x[kp1]), (y[k],y[kp1]), linewidth=0.5, color='#89fe05', linestyle='-', label='Tropical Storm')
      if((wind[k] > 32) and (wind[k] <= 42)): cax.plot((x[k],x[kp1]), (y[k],y[kp1]), linewidth=0.5, color='#fffd01', linestyle='-', label='Category 1')
      if((wind[k] > 42) and (wind[k] <= 49)): cax.plot((x[k],x[kp1]), (y[k],y[kp1]), linewidth=0.5, color='#ff9408', linestyle='-', label='Category 2')
      if((wind[k] > 49) and (wind[k] <= 58)): cax.plot((x[k],x[kp1]), (y[k],y[kp1]), linewidth=0.5, color='#ff5b00', linestyle='-', label='Category 3')
      if(wind[k] > 58): cax.plot((x[k],x[kp1]), (y[k],y[kp1]), linewidth=0.5, color='#ec2d01', linestyle='-', label='Category 4')

def kde_plot(lon_data,lat_data,plt,cax=None):
#Creates kde plot (both tracks and genesis)

  k = kde.gaussian_kde([lon_data,lat_data])
  xi, yi = np.mgrid[30:90:240*1j, -40:0:160*1j] #0.25 degree bins
  zi = k(np.vstack([xi.flatten(), yi.flatten()]))
  corr_array=np.reshape(zi,(xi.shape))
  if plt == 'yes':
    im = cax.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap='hot_r',vmin=0,vmax=0.002)
    return corr_array,im
  else:
    return corr_array

def plot_panels(expt):

  ra_pd = unpickle_cubes(starterp+obs+'_'+p_file)
  ra_lon_gen = unpickle_cubes(starterp+'ra_lon'+p_file)
  ra_lat_gen = unpickle_cubes(starterp+'ra_lat'+p_file)
  mod_pd = unpickle_cubes(starterp+expt+'_'+p_file)
  mod_lon_gen = unpickle_cubes(starterp+expt+'_mod_lon'+p_file)
  mod_lat_gen = unpickle_cubes(starterp+expt+'_mod_lat'+p_file)
  ml_wspd = unpickle_cubes(starterp+expt+'_ml_wspd'+p_file)

  #Create plot
  projection = crs.PlateCarree()
  axes_class = (GeoAxes,
                dict(map_projection=projection))
  fig = plt.figure(figsize=(7, 5))
  axgr = AxesGrid(fig, 111, axes_class=axes_class,
                  nrows_ncols=(2, 2),
                  ngrids = 4,
                  axes_pad=0.3,
                  cbar_mode=None,
                  label_mode='')  # note the empty label_mode
  
  for i, ax in enumerate(axgr):

    ax.coastlines()
    ax.set_extent([30,90,-40,0],crs=projection)
    ax.set_yticks(np.linspace(-40, 0, 5), crs=projection)
    ax.set_xticks(np.linspace(30, 90, 7), crs=projection)

    #Genesis plot
    if i==0:
      handles=gen_plot(ml_wspd,mod_lon_gen,mod_lat_gen,ax)
      ax.annotate(('a'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.tick_params(direction='in', top=True, right=True,labelsize=6,labelbottom=False)
  
    #Genesis KDE
    if i==1:
      ra_array=kde_plot(ra_lon_gen,ra_lat_gen,plt='no')
      mod_array,im=kde_plot(mod_lon_gen,mod_lat_gen,plt='yes',cax=ax)
      corr=spatial_corr(mod_array,ra_array)
      ax.annotate(('r='+'%.2f' % corr), xy=(80, -37),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.annotate(('b'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.tick_params(direction='in', top=True, right=True,labelsize=6,labelbottom=False,labelleft=False)
  
    #Track plot
    if i==2:
      track_plot(mod_pd,ax)
      ax.annotate(('c'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.tick_params(direction='in', top=True, right=True,labelsize=6)

  
    #Track KDE
    if i==3:
      ra_array=kde_plot(ra_pd['lon'],ra_pd['lat'],plt='no')
      mod_array,im=kde_plot(mod_pd['lon'],mod_pd['lat'],plt='yes',cax=ax)
      corr=spatial_corr(mod_array,ra_array)
      ax.annotate(('r='+'%.2f' % corr), xy=(80, -37),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.annotate(('d'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
      ax.tick_params(direction='in', top=True, right=True,labelsize=6,labelleft=False)

    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

  cax = fig.add_axes([0.92, 0.13, 0.03, 0.73])
  cbar = fig.colorbar(im,cax=cax, orientation='vertical', fraction=0.028, pad=0.01,ticks=np.linspace(0, 0.002, 5))
  cbar.ax.tick_params(labelsize=6)
  legend = ax.legend(handles=handles, labels=['Tropical Storm','Category 1','Category 2','Category 3', 'Category 4'],loc='upper center', 
             bbox_to_anchor=(0, -0.15),fancybox=True, shadow=False, ncol=5,fontsize=6,frameon=False)

  if save_plot:
    fig.savefig(starterpng+expt+plot_file, dpi=400, bbox_inches='tight')

###############################
#main execution
###############################
if pre_processor_experiments:
    print('entering pre-processor routine')
   
    ra_pd = read_data(obs)
    pickle.dump(ra_pd, open(starterp+obs+'_'+p_file, "wb" ))

    #green_list = create_greenlist(mod_list)
    green_list = tra_mod_list
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list', green_list)

    for expt in green_list:   
      mod_pd = read_data(expt)
      pickle.dump(mod_pd, open(starterp+expt+'_'+p_file, "wb" ))
  
###############################
#Calculation control
###############################
if processor_calculations:
    print('entering calculation routine')

    ra_pd = unpickle_cubes(starterp+obs+'_'+p_file)
    ra_lon_gen,ra_lat_gen=genesis_locations(ra_pd)
    pickle.dump(ra_lon_gen, open(starterp+'ra_lon'+p_file, "wb" ))
    pickle.dump(ra_lat_gen, open(starterp+'ra_lat'+p_file, "wb" ))

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      mod_pd = unpickle_cubes(starterp+expt+'_'+p_file)
      mod_lon_gen,mod_lat_gen=genesis_locations(mod_pd)
      ml_wspd=max_lifetime_wspd(mod_pd)
      pickle.dump(mod_lon_gen, open(starterp+expt+'_mod_lon'+p_file, "wb" ))
      pickle.dump(mod_lat_gen, open(starterp+expt+'_mod_lat'+p_file, "wb" ))
      pickle.dump(ml_wspd, open(starterp+expt+'_ml_wspd'+p_file, "wb" ))
     
###############################
#plot control
###############################
if create_plot:
    print('entering plotting routine')
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
      plot_panels(expt)
      #plt.show()
      plt.clf()

    print('plotting complete')
 
###############################
#End of file
###############################

