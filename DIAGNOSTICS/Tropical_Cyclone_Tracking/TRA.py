# -*- coding: utf-8 -*-

##############################
###-----Import Modules-----###
##############################

from windspharm.iris import VectorWind
from numpy import *
from numpy import radians,cos,sin,sqrt,exp
from decimal import *
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from netCDF4 import num2date, Dataset

import os
import iris
import iris.cube
from iris.cube import Cube
import iris.coords
from iris.coords import DimCoord
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

from TRA_config import *
import pandas as pd
import xarray as xr
import operator
import warnings
from itertools import islice

sys.path.insert(1,home_add+'LaunchPAD/files/CONFIG')
from find_files import *
from config import *
from config_functions import *

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

def load_expt_t(expt):

    print(hr_sixhr_file_location(expt, 'ta'))
    cube_list_ta = xr.open_mfdataset(hr_sixhr_file_location(expt, 'ta'))
    if expt in ['ERA5']:
      cube_list_ta = cube_list_ta.rename({'latitude':'lat','longitude':'lon','level':'plev'})
      cube_list_ta = cube_list_ta.assign_coords(plev=cube_list_ta.plev*100.)
      cube_list_ta = cube_list_ta.reindex(lat=cube_list_ta.lat[::-1])['t']
    else:
      cube_list_ta = cube_list_ta['ta']
    cube_list_250 = cube_list_ta.sel(lat=slice(-40,0), lon=slice(30,90), plev=25000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube_list_500 = cube_list_ta.sel(lat=slice(-40,0), lon=slice(30,90), plev=50000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube_250 = xr.DataArray.to_iris(cube_list_250)
    cube_500 = xr.DataArray.to_iris(cube_list_500) 

    result250 = unit_converter_k_to_C(cube_250)
    result500 = unit_converter_k_to_C(cube_500)
    
    return result250, result500
    
def load_expt_slp(expt):

    cube_list_psl = xr.open_mfdataset(hr_sixhr_file_location(expt, 'psl'))
    if expt in ['ERA5']:
      cube_list_psl = cube_list_psl.rename({'latitude':'lat','longitude':'lon'})
      cube_list_psl = cube_list_psl.reindex(lat=cube_list_psl.lat[::-1])['msl']
    else:
      cube_list_psl = cube_list_psl['psl']
    cube_list_psl = cube_list_psl.sel(lat=slice(-40,0), lon=slice(30,90), time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube = xr.DataArray.to_iris(cube_list_psl)
    return cube
    
def load_expt_wd(expt):

    if expt in ['ERA5']:
      cubeL1 = xr.open_mfdataset(hr_sixhr_file_location(expt, 'ua'))['u']
      cubeL2 = xr.open_mfdataset(hr_sixhr_file_location(expt, 'va'))['v']
      cube10_uL = xr.open_mfdataset(hr_sixhr_file_location(expt, 'uas'))['u10']
      cube10_vL = xr.open_mfdataset(hr_sixhr_file_location(expt, 'vas'))['v10']

      cubeL1 = cubeL1.rename({'latitude':'lat','longitude':'lon','level':'plev'})
      cubeL1 = cubeL1.reindex(lat=cubeL1.lat[::-1])
      cubeL1 = cubeL1.assign_coords(plev=cubeL1.plev*100.)
      cubeL2 = cubeL2.rename({'latitude':'lat','longitude':'lon','level':'plev'})
      cubeL2 = cubeL2.reindex(lat=cubeL2.lat[::-1])
      cubeL2 = cubeL2.assign_coords(plev=cubeL2.plev*100.)
      cube10_uL = cube10_uL.rename({'latitude':'lat','longitude':'lon'})
      cube10_uL = cube10_uL.reindex(lat=cube10_uL.lat[::-1])
      cube10_vL = cube10_vL.rename({'latitude':'lat','longitude':'lon'})
      cube10_vL = cube10_vL.reindex(lat=cube10_vL.lat[::-1])
    else:
      cubeL1 = xr.open_mfdataset(hr_sixhr_file_location(expt, 'ua'))['ua']
      cubeL2 = xr.open_mfdataset(hr_sixhr_file_location(expt, 'va'))['va']
      cube10_uL = xr.open_mfdataset(hr_sixhr_file_location(expt, 'uas'))['uas']
      cube10_vL = xr.open_mfdataset(hr_sixhr_file_location(expt, 'vas'))['vas']
    cubeL3 = cubeL1
    cubeL4 = cubeL2 

    cubeL1 = cubeL1.sel(lat=slice(-40,0), lon=slice(30,90),plev=85000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cubeL2 = cubeL2.sel(lat=slice(-40,0), lon=slice(30,90),plev=85000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cubeL3 = cubeL3.sel(lat=slice(-40,0), lon=slice(30,90), plev=25000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cubeL4 = cubeL4.sel(lat=slice(-40,0), lon=slice(30,90), plev=25000, time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube10_uL = cube10_uL.sel(lat=slice(-40,0), lon=slice(30,90), time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube10_vL = cube10_vL.sel(lat=slice(-40,0), lon=slice(30,90), time=slice(str(years[0])+'-01',str(years[1])+'-12'))
    cube1 = xr.DataArray.to_iris(cubeL1)
    cube2 = xr.DataArray.to_iris(cubeL2)
    cube3 = xr.DataArray.to_iris(cubeL3)
    cube4 = xr.DataArray.to_iris(cubeL4)
    cube10_u = xr.DataArray.to_iris(cube10_uL)
    cube10_v = xr.DataArray.to_iris(cube10_vL)

    result250 = calc_windspeed(cube3,cube4)
    result1000 = calc_windspeed(cube10_u, cube10_v)
    result850 = calc_windspeed(cube1,cube2)
   
    u850 = cube1
    v850 = cube2 
    pickle.dump(u850, open(starterp+expt+'_u850_'+p_file, "wb" ))
    pickle.dump(v850, open(starterp+expt+'_v850_'+p_file, "wb" ))
                      
    return result250, result850, result1000
    
def calc_windspeed(ua, va):

    ws=ua
    ws.data = np.sqrt( ua.data**2 + va.data**2 )   
          
    return ws
 
###############################
#Calculation function(s)
###############################
   
def ws_thresh(res):

  if(res <= 10): wspd_threshold = 17.5
  if((res > 10) and (res <= 30)): 
    wspd_threshold = 17
  if((res > 30) and (res <= 50)): 
    wspd_threshold = 16.6
  if((res > 50) and (res <= 75)): 
    wspd_threshold = 15.8
  if((res > 75) and (res <= 100)): 
    wspd_threshold = 14.9
  if((res > 100) and (res <= 125)): 
    wspd_threshold = 14.3
  if((res > 125) and (res <= 150)): 
    wspd_threshold = 13.9
  if((res >150) and (res <= 175)): 
    wspd_threshold = 13.3
  if((res >175) and (res <= 200)): 
    wspd_threshold = 12.9
  if((res >200) and (res <= 225)): 
    wspd_threshold = 12
  if((res > 225) and (res <= 250)): 
    wspd_threshold = 11	 
  if(res > 250): 
    wspd_threshold = 10.5
	 
  return wspd_threshold 
  
def calc_mslp1(counter, value, expt, tc_id): 

  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)[counter]
  
  thresh=101325.00
           
  da = xr.DataArray.from_iris(slp)
  mslp = da.min().values
  coords = da.where(da==mslp, drop=True).squeeze()
  mslp_lat = coords.lat.values
  mslp_lon = coords.lon.values
  if size(mslp_lon) > 1:
      mslp_lon=mslp_lon[-1] #if 2+ identical minima take first value 
  if size(mslp_lat) > 1:
      mslp_lat=mslp_lat[-1] 

  return mslp, mslp_lon, mslp_lat
      
def calc_mslp2(counter, value, expt, tc_id, mslp, mslp_lon, mslp_lat):

  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)[counter]
  
  thresh=101325.00
    
  track_radius=4
  max_lat = mslp_lat + track_radius
  min_lat = mslp_lat - track_radius
  min_lon = mslp_lon - track_radius
  max_lon = mslp_lon + track_radius
      
  domain_slp = slp.extract(lon_bounds(min_lon, max_lon) & lat_bounds(min_lat, max_lat))
      
  da = xr.DataArray.from_iris(domain_slp)
  mslp = da.min().values
  coords = da.where(da==mslp, drop=True).squeeze()
  mslp_lat = coords.lat.values
  mslp_lon = coords.lon.values
  if size(mslp_lon) > 1:
      mslp_lon=mslp_lon[0] #if 2+ identical minima take first value 
  if size(mslp_lat) > 1:
      mslp_lat=mslp_lat[0]
    
  return mslp, mslp_lon, mslp_lat 
 
def calc_windregion(counter, mslp_lon, mslp_lat):

  avg_radius=3
  
  ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)[counter]
  ws850 = unpickle_cubes(starterp+expt+'_ws850_'+p_file)[counter]

  int_lat_lower = mslp_lat - avg_radius
  int_lat_upper = mslp_lat + avg_radius
  int_lon_lower = mslp_lon - avg_radius
  int_lon_upper = mslp_lon + avg_radius
  
  coords = ('longitude', 'latitude')
  avg_wspd_250 = ws250.extract(lat_bounds(int_lat_lower, int_lat_upper) & lon_bounds(int_lon_lower, int_lon_upper)).collapsed(coords, iris.analysis.MEAN).data
  avg_wspd_850 = ws850.extract(lat_bounds(int_lat_lower, int_lat_upper) & lon_bounds(int_lon_lower, int_lon_upper)).collapsed(coords, iris.analysis.MEAN).data

  return avg_wspd_250,avg_wspd_850
  
def calc_maxwind(counter, mslp_lon, mslp_lat):

  wind_radius=5
  
  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)
  
  lat_lower = mslp_lat - wind_radius
  lat_upper = mslp_lat + wind_radius
  lon_lower = mslp_lon - wind_radius
  lon_upper = mslp_lon + wind_radius

  max_wspd = 0
  
  wsp10m = unpickle_cubes(starterp+expt+'_ws1000_'+p_file)[counter]
  
  wsp10m.extract(lat_bounds(lat_lower, lat_upper) & lon_bounds(lon_lower, lon_upper))
  
  da = xr.DataArray.from_iris(wsp10m)
  max_wspd = da.max().values

  return max_wspd
  
def calc_vort(counter, mslp_lon, mslp_lat):
  R=6371000
  with warnings.catch_warnings():
      warnings.simplefilter('ignore', UserWarning)
      u850 = unpickle_cubes(starterp+expt+'_u850_'+p_file)
      v850 = unpickle_cubes(starterp+expt+'_v850_'+p_file)

      ua=u850[counter]
      va=v850[counter]

  uaxr=xr.DataArray.from_iris(ua)
  vaxr=xr.DataArray.from_iris(va)
  lats=uaxr.lat.values
  lons=uaxr.lon.values
   
  vort_min=0
  vort_radius=4
  ni=len(lons)
  nj=len(lats)
  vort=np.zeros((nj,ni))
    
  i1 = 1
  i2 = -2
  j1 = 2
  j2 = -1
  k1 = 0
  k2 = -3

  lon_mesh, lat_mesh = np.meshgrid(lons,lats)
  diff_lon = lon_mesh[i1:i2,j1:j2] - lon_mesh[i1:i2,k1:k2]
  diff_lat = lat_mesh[j1:j2,i1:i2] - lat_mesh[k1:k2,i1:i2]
  r_lat= R * cos(np.radians(lat_mesh[i1:i2,i1:i2]))    
  dx = (diff_lon/360)*(2*pi*r_lat)
  dy = (-diff_lat/360)*(2*pi*R)
    
  v_east=vaxr[i1:i2,j1:j2]
  v_west=vaxr[i1:i2,k1:k2]
  u_north=uaxr[k1:k2,i1:i2]
  u_south=uaxr[j1:j2,i1:i2]   
  
  vort[i1:i2,i1:i2]=((v_east.values-v_west.values)/dx)-((u_north.values-u_south.values)/dy) 

  lat= DimCoord(lats,standard_name='latitude',units='degrees')
  lon = DimCoord(lons,standard_name='longitude',units='degrees')
  vort_cube = Cube(vort, dim_coords_and_dims=[(lat, 0),(lon, 1)])
 
  lat_lower = mslp_lat - vort_radius
  lat_upper = mslp_lat + vort_radius
  lon_lower = mslp_lon - vort_radius
  lon_upper = mslp_lon + vort_radius

  vort=vort_cube.extract(lat_bounds(lat_lower, lat_upper) & lon_bounds(lon_lower, lon_upper))
  da = xr.DataArray.from_iris(vort)
  vort_min = da.min().values

  return vort_min
  
def calc_warm_core(counter, mslp_lon, mslp_lat):
  warm_core_radius=2
  avg_radius = 5
  
  #Creates range bounds for avg temp
  lat_lower = mslp_lat - warm_core_radius
  lat_upper = mslp_lat + warm_core_radius
  lon_lower = mslp_lon - warm_core_radius
  lon_upper = mslp_lon + warm_core_radius
  
  lat_lower_avg = mslp_lat - avg_radius
  lat_upper_avg = mslp_lat + avg_radius
  lon_lower_avg = mslp_lon - avg_radius
  lon_upper_avg = mslp_lon + avg_radius
  
  t250 = unpickle_cubes(starterp+expt+'_t250_'+p_file)[counter]
  t500 = unpickle_cubes(starterp+expt+'_t500_'+p_file)[counter]
  
  int_avg_temp_500_250 = iris.analysis.maths.multiply(iris.analysis.maths.add(t500, t250), 0.5)
  
  #wc_temp is max int_avg_temp_500_250
  coords = ('longitude', 'latitude')
  wc_temp = int_avg_temp_500_250.extract(lat_bounds(lat_lower, lat_upper) & lon_bounds(lon_lower, lon_upper)).collapsed(coords, iris.analysis.MAX).data
	  
  int_avg_temp_500_250 = int_avg_temp_500_250.extract(lat_bounds(lat_lower_avg, lat_upper_avg) & lon_bounds(lon_lower_avg, lon_upper_avg))
  int_avg_temp_500_250 = int_avg_temp_500_250.collapsed(coords, iris.analysis.MEAN).data
  
  return wc_temp, int_avg_temp_500_250
  
def tstep_fail_allowance(counter, df):
  
  radius=4.5
  if ((df.at[counter, 'tc_id'] == 0) and (df.at[counter-1, 'tc_id'] == 1) and (df.at[counter+1, 'tc_id'] == 1)):
    if (((df.at[counter,'mslp_lat'] <= (df.at[counter-1,'mslp_lat']+radius)) and (df.at[counter,'mslp_lat'] >= df.at[counter-1,'mslp_lat'])) or \
    ((df.at[counter,'mslp_lat'] >= (df.at[counter-1,'mslp_lat']-radius)) and (df.at[counter,'mslp_lat'] <= df.at[counter-1,'mslp_lat']))):
      if (((df.at[counter,'mslp_lon'] <= (df.at[counter-1,'mslp_lon']+radius)) and (df.at[counter,'mslp_lon'] >= df.at[counter-1,'mslp_lon'])) or \
      ((df.at[counter,'mslp_lon'] >= (df.at[counter-1,'mslp_lon']-radius)) and (df.at[counter,'mslp_lon'] <= df.at[counter-1,'mslp_lon']))):
        if (((df.at[counter,'mslp_lat'] <= (df.at[counter+1,'mslp_lat']+radius)) and (df.at[counter,'mslp_lat'] >= df.at[counter+1,'mslp_lat'])) or \
	((df.at[counter,'mslp_lat'] >= (df.at[counter+1,'mslp_lat']-radius)) and (df.at[counter,'mslp_lat'] <= df.at[counter+1,'mslp_lat']))):
          if (((df.at[counter,'mslp_lon'] <= (df.at[counter+1,'mslp_lon']+radius)) and (df.at[counter,'mslp_lon'] >= df.at[counter+1,'mslp_lon'])) or \
	  ((df.at[counter,'mslp_lon'] >= (df.at[counter+1,'mslp_lon']-radius)) and (df.at[counter,'mslp_lon'] <= df.at[counter+1,'mslp_lon']))):
            df.at[counter,'tc_id'] = 1

  return df
  
def assign_filter(counter, df):
  
  radius=4.5
  
  if ((df.at[counter, 'tc_id'] == 1.0) and ((df.at[counter-1, 'tc_id'] == 0.0) or (counter == 0))):
      df.at[counter,'tc_event'] = 'New'  
 
  if ((df.at[counter,'tc_id'] == 1) and (df.at[counter-1,'tc_id'] == 1)):
    if (((df.at[counter,'mslp_lat'] <= (df.at[counter-1,'mslp_lat']+radius)) and (df.at[counter,'mslp_lat'] >= df.at[counter-1,'mslp_lat'])) or \
    ((df.at[counter,'mslp_lat'] >= (df.at[counter-1,'mslp_lat']-radius)) and (df.at[counter,'mslp_lat'] <= df.at[counter-1,'mslp_lat']))):
      if (((df.at[counter,'mslp_lon'] <= (df.at[counter-1,'mslp_lon']+radius)) and (df.at[counter,'mslp_lon'] >= df.at[counter-1,'mslp_lon'])) or \
      ((df.at[counter,'mslp_lon'] >= (df.at[counter-1,'mslp_lon']-radius)) and (df.at[counter,'mslp_lon'] <= df.at[counter-1,'mslp_lon']))):
        df.at[counter,'tc_event']='Same'
  else:
    df.at[counter,'tc_event']='New'

  if (df.at[counter, 'tc_id'] == 0):
    df.at[counter,'tc_event'] = '-'
  
  return df
  
def time_threshold1(counter,df):

  #df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if (df.at[counter, 'tc_event'] == 'New'):
      if ((df.at[counter+1, 'tc_event'] != 'Same') or (df.at[counter+2, 'tc_event'] != 'Same') or (df.at[counter+3, 'tc_event'] != 'Same') or (df.at[counter+4, 'tc_event'] != 'Same') or (df.at[counter+5, 'tc_event'] != 'Same') or (df.at[counter+6, 'tc_event'] != 'Same') or (df.at[counter+7, 'tc_event'] != 'Same')):  
           df.at[counter,'tc_event'] = '-'
      
  return df 
  
def time_threshold2(counter,df): 

  if ((df.at[counter, 'tc_event'] == 'Same') and (df.at[counter-1, 'tc_event'] == '-')):  
       df.at[counter,'tc_event'] = '-'
    
  return df

def number_events1(counter,event_number,df):

  if df.at[counter, 'tc_event'] == 'New':
      event_number = event_number + 1
      df.at[counter,'tc_number'] = event_number
  else:
      df.at[counter,'tc_number'] = 999

  return df,event_number
  
def number_events2(counter,df): 

  if df.at[counter, 'tc_event'] == 'Same':
      df.at[counter,'tc_number'] = df.at[counter-1,'tc_number']
  
  return df	  

def remove_td(counter, df):
 
  group=df.groupby(['tc_number']).max()
  ml_wspd=group['max_wspd']

  rem_tcs=[]
  for x,i in zip(ml_wspd,range(0,len(ml_wspd))):
    if((x <= 17.5) or (math.isnan(x) == True)): rem_tcs.append(group.index[i])

  for x in rem_tcs:
    for index, row in df.iterrows():
      if df.loc[index, 'tc_number'] == x:
        df.drop(index, inplace=True)

  return df 

def number_events3(counter,event_number,df):

  if df.at[counter, 'tc_event'] == 'New':
      event_number = event_number + 1
      df.at[counter,'tc_number'] = event_number
  elif df.at[counter,'tc_event'] == 'Same':
      df.at[counter,'tc_number'] = event_number 

  return df,event_number

###############################
#Execution function(s)
###############################

if pre_processor_experiments:
    print('entering pre-processor routine')
    green_list =obs_list+tra_mod_list
    
    pickle.dump(green_list, open(starterp+'green_list'+p_file, "wb" ))
    print('new mod list', green_list)

    for expt in green_list: 
        t250,t500 = load_expt_t(expt)
        pickle.dump(t250, open(starterp+expt+'_t250_'+p_file, "wb" ))
        pickle.dump(t500, open(starterp+expt+'_t500_'+p_file, "wb" ))

        ws250,ws850,ws1000 = load_expt_wd(expt)
        
        pickle.dump(ws250, open(starterp+expt+'_ws250_'+p_file, "wb" ))
        pickle.dump(ws850, open(starterp+expt+'_ws850_'+p_file, "wb" ))
        pickle.dump(ws1000, open(starterp+expt+'_ws1000_'+p_file, "wb" ))
	
        slp = load_expt_slp(expt)
        pickle.dump(slp, open(starterp+expt+'_slp_'+p_file, "wb" ))
	
    print('Pre-processor complete')
	
if processor_calculations1:

    df = pd.DataFrame(columns=['date','mslp','mslp_lon','mslp_lat','max_wspd','vort_min','wc_temp','tc_id','tc_event','tc_number'])
    df = df.astype({"date": float, "mslp": float, "mslp_lon": float, "mslp_lat": float, "max_wspd": float, "vort_min": float, "wc_temp": float, "tc_id": int, "tc_event": str,"tc_number": int})

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)
       	
        nl=ws250.coord('time').points #time coords
        tc_id = 0
        for counter, value in enumerate(nl):
                        
            #units and calendar below will be model-dependent
            date=num2date(value,units='hours since 1980-01-01 00:00:00',calendar='gregorian') 

            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)

                if(counter == 0) or (tc_id == 0): #ith-1 tc_id
                    mslp, mslp_lon, mslp_lat = calc_mslp1(counter,value, expt, tc_id) 
                elif(tc_id == 1): 
                    mslp, mslp_lon, mslp_lat = calc_mslp2(counter,value, expt, tc_id, mslp, mslp_lon, mslp_lat) 
		    	 	    
                max_wspd = calc_maxwind(counter, mslp_lon, mslp_lat) 	    
                wspd_threshold = ws_thresh(abs(ws250.coord('longitude').points[2]-ws250.coord('longitude').points[1])*111) 	               
                wc_temp, avg_temp_500_250 = calc_warm_core(counter, mslp_lon, mslp_lat) 
                avg_wspd_250, avg_wspd_850 = calc_windregion(counter, mslp_lon, mslp_lat)

                if ((max_wspd >= wspd_threshold) and (wc_temp >= (avg_temp_500_250 + 1.)) and (avg_wspd_250 < avg_wspd_850)):
                    vort_min = calc_vort(counter, mslp_lon, mslp_lat)
                else:
                    vort_min=0
                     
                if ((max_wspd >= wspd_threshold) and (vort_min <= -0.000035) and (wc_temp >= (avg_temp_500_250 + 1.)) and (avg_wspd_250 < avg_wspd_850)):    
                    tc_id=1
                else:
                    tc_id=0
		
            df.at[counter,'tc_id'] = tc_id
            df.at[counter,'vort_min'] = vort_min
            df.at[counter,'mslp'] = mslp
            df.at[counter,'mslp_lon'] = mslp_lon
            df.at[counter,'mslp_lat'] = mslp_lat
            df.at[counter,'max_wspd'] = max_wspd
            df.at[counter,'wc_temp'] = wc_temp
            df.at[counter,'date'] = date
	    	    
            df.at[counter,'tc_event'] = "-"
            df.at[counter,'tc_number'] = 0
       
        pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" )) #dataframe of all variables
	
    print('calc stage 1 complete')

if processor_calculations2:	
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        print(expt)
    
        df = unpickle_cubes(starterp+expt+'_df_'+p_file)
        end_count = len(df.index)
 
        for index, row in islice(df.iterrows(), 1, end_count):
            tstep_fail_allowance(index, df)
	
        for index, row in islice(df.iterrows(), 1, None):
  
            assign_filter(index,df)		

        for index, row in islice(df.iterrows(), None, end_count-7):
       
            time_threshold1(index,df)
	
        for index, row in islice(df.iterrows(), 1, None):
      
            time_threshold2(index,df)
        
        event_number=0		
        for index, row in df.iterrows():
 
            df,event_number = number_events1(index,event_number,df)

        for index, row in islice(df.iterrows(), 1, None):

            number_events2(index,df)
	
        pickle.dump(df, open(starterp+expt+'_df_post-filter_'+p_file, "wb" ))

        for index, row in df.iterrows():

            if df.loc[index, 'tc_number'] == 999:
                df.drop(index, inplace=True)	
        
        remove_td(index,df)

        event_number=0

        for index, row in df.iterrows():

            df,event_number = number_events3(index,event_number,df)

        #Remove vorticity, warm core & tc_id columns as these need not be printed

        del df['vort_min']
        del df['wc_temp']
        del df['tc_id']

        #Write output to text file
        np.savetxt(starterp+expt+'_tracking_output.txt', df, fmt='%s')
	
    print('Tracking complete for '+expt)
