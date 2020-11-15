##############################
###-----Import Modules-----###
##############################

from netCDF4 import Dataset
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from netCDF4 import num2date, date2num
import datetime
from scipy.stats import kde

#############################
###------Subroutines------###
#############################

def read_data(file):
#Reads data

  data=np.loadtxt(file,
           dtype={'names': ('date','time','mslp', 'lon','lat','max_wind','vort','tc_event','tc_number'),
                  'formats': ('U10', 'U10', np.float, np.float, np.float, np.float, np.float, 'U4', np.float)})

  mslp=data['mslp']
  lon=data['lon']
  lat=data['lat']
  max_wind=data['max_wind']
  tc_event=data['tc_event']
  tc_number=data['tc_number']

  return lon,lat,tc_event,max_wind,mslp,tc_number

def reanalysis():
#This reads in reanalysis data.

  data=np.loadtxt('ERA5_filtered_output.txt',
                  dtype={'names': ('date','time','mslp','lon','lat','max_wind','vort','tc_event','tc_number'),
                        'formats': ('U10','U10',np.float,np.float, np.float, np.float, np.float, 'U4', np.float)})


  era_lon=data['lon']
  era_lat=data['lat']
  era_event=data['tc_event']

  return era_lon,era_lat,era_event

def genesis_locations(lon,lat,tc_event):
#Returns lon&lat points for all genesis events

  lon_gen=lon[tc_event == "New"]
  lat_gen=lat[tc_event == "New"]

  return lon_gen,lat_gen

def max_lifetime_wspd():
#Calculates the lifetime maximum windspeed for each TC event

  df = pd.DataFrame({'NUM':tc_number[:],'MAXWSPD':max_wind[:]})
  group=df.groupby(['NUM']).max()
  ml_wspd=group['MAXWSPD']

  return ml_wspd

def basemap():
#Creates basemap for plots

  m = Basemap(projection='cyl',resolution='i',llcrnrlat=-40,urcrnrlat=0.1,llcrnrlon=30,urcrnrlon=90,ax=cax)
  m.drawcoastlines(linewidth=0.5)
  m.drawcountries(linewidth=0.5)
  m.drawmapboundary()
  # manually add ticks
  cax.set_xticks([30,40,50,60,70,80,90])
  cax.set_yticks([-40,-30,-20,-10,0])
  cax.tick_params(axis='both',which='major',direction='in',zorder=11)
  # add ticks to the opposite side as well
  cax.xaxis.set_ticks_position('both')
  cax.yaxis.set_ticks_position('both')
  # remove the tick labels
  cax.xaxis.set_ticklabels([])
  cax.yaxis.set_ticklabels([])
  # only add lon&lat labels on outer axes
  if((cax == axes[0]) or (cax == axes[2])):
    m.drawparallels(np.arange(-40,10,10), labels=[1,0,0,1], linewidth=0, fontsize=6, xoffset=2)
  if((cax == axes[2]) or (cax == axes[3])):
    m.drawmeridians(np.arange(30,100,10), labels=[1,0,0,1], linewidth=0, fontsize=6, yoffset=2)

  return m

def gen_plot():
#Creates genesis plot

  #Categorizes each genesis event based on the maximum lifetime intensity of the TC
  ts=np.where(ml_wspd <= 32)
  c1=np.where((ml_wspd > 32) & (ml_wspd <= 42))
  c2=np.where((ml_wspd > 42) & (ml_wspd <= 49))
  c3=np.where((ml_wspd > 49) & (ml_wspd <= 58))
  c45=np.where(ml_wspd > 58) 

  xts, yts = m(lon_gen[ts],lat_gen[ts])
  xc1, yc1 = m(lon_gen[c1],lat_gen[c1])
  xc2, yc2 = m(lon_gen[c2],lat_gen[c2])
  xc3, yc3 = m(lon_gen[c3],lat_gen[c3])
  xc45, yc45 = m(lon_gen[c45],lat_gen[c45])

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

def kde_plot(lon_data,lat_data,plot_axis):
#Creates kde plot (both tracks and genesis)

  k = kde.gaussian_kde([lon_data,lat_data])
  xi, yi = np.mgrid[30:90:240*1j, -40:0:160*1j] #0.25 degree bins
  zi = k(np.vstack([xi.flatten(), yi.flatten()]))
  im = plot_axis.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap='hot_r',vmin=0,vmax=0.002)
  corr_array=im.get_array().reshape(im._meshWidth, im._meshHeight) #2D array to calculate spatial correlation

  return corr_array, im

def track_plot():
#Creates track plot

  #Groups TCs into individual events based on the group number
  df = pd.DataFrame({'NUM':tc_number[:],'LON':lon[:],'LAT':lat[:],'WSPD':max_wind[:]})
  group=df.groupby(['NUM'])

  for group_number,group_data in group: #Here, the first item we mention (here: i) will always give us the group numbers / headings.
    group_data=group_data.to_numpy()
    x=group_data[:,1] #longitude
    y=group_data[:,2] #latitude
    wind=group_data[:,3] #windspeed
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

def spatial_corr():
#Calculates spatial correlation with respect to reanalysis 

  p = independent_corr #independent (reanalysis)
  q = corr_array #dependent (model)
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

##############################
###----Main Executables----###
##############################

#Read in data
lon,lat,tc_event,max_wind,mslp,tc_number=read_data('CNRM-CM6-1-HR_tracking_output.txt')
era_lon,era_lat,era_event,era_max_wind,era_mslp,era_tc_number=read_data('ERA5_tracking_output.txt')

#Create plot
fig, axes = plt.subplots(nrows=2,ncols=2)
axes=axes.flatten()

#Loop through axes and plot for each
for cax in axes:
  lon_gen,lat_gen=genesis_locations(lon,lat,tc_event)
  era5_lon_gen,era5_lat_gen=genesis_locations(era_lon,era_lat,era_event)
  ml_wspd=max_lifetime_wspd()
  m=basemap()
  
  #Genesis plot
  if (cax==axes[0]):
    handles=gen_plot()
    cax.annotate(('a'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
  
  #Genesis KDE
  if (cax==axes[1]):independent_corr,im=kde_plot(era5_lon_gen,era5_lat_gen,plt)
  if (cax==axes[1]):corr_array,im=kde_plot(lon_gen,lat_gen,cax)
  if (cax==axes[1]):
    corr=spatial_corr()
    cax.annotate(('r='+'%.2f' % corr), xy=(80, -37),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
    cax.annotate(('b'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
  
  #Track plot
  if (cax==axes[2]):
    track_plot()
    cax.annotate(('c'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
  
  #Track KDE
  if (cax==axes[3]):independent_corr,im=kde_plot(era_lon,era_lat,plt)
  if (cax==axes[3]):corr_array,im=kde_plot(lon,lat,cax)
  if (cax==axes[3]):
    corr=spatial_corr()
    cax.annotate(('r='+'%.2f' % corr), xy=(80, -37),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))
    cax.annotate(('d'), xy=(32, -4),zorder=10,fontsize=6,bbox=dict(facecolor='white', edgecolor='black',lw=0.8,boxstyle='square,pad=0.5'))

##############################
###-------Formatting-------###
############################## 

fig.subplots_adjust(wspace=0.1, hspace=-0.2)
plt.legend(handles=handles, labels=['Tropical Storm','Category 1','Category 2','Category 3', 'Category 4'],loc='upper center', bbox_to_anchor=(0, -0.15),fancybox=True, shadow=False, ncol=5,fontsize=6,frameon=False)
cbar = fig.colorbar(im, ax=axes.ravel().tolist(),orientation='vertical', fraction=0.031, pad=0.04,ticks=np.linspace(0, 0.002, 5))
cbar.ax.tick_params(labelsize=6)
fig.savefig('CompoundFigure.png', dpi=400, bbox_inches='tight')
