# -*- coding: utf-8 -*-

##############################
###-----Import Modules-----###
##############################

import numpy as np
from windspharm.iris import VectorWind
#from scipy.io import netcdf
from numpy import *
from math import radians,cos,sin,sqrt,exp
from decimal import *
#import metpy.calc as mpcalc
#from metpy.units import units
import matplotlib.pyplot as plt
#from datetime import datetime, timedelta
from netCDF4 import num2date, Dataset

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
from TRA_config import *
import pandas as pd
import xarray as xr
import operator
import warnings
from itertools import islice
import datetime

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

    cube_list = iris.load(sixhr_file_location(expt, 'ta'))# & 
    cube=cube_concatenator(cube_list)
    cube = cube.extract(year_bounds(1990, 1991))
    
    #iris.coord_categorisation.add_month_number(cube, 'time', name='month_number') 
    #cube = cube.extract(iris.Constraint(month_number=3))
    
    cube = cube.extract(lat_bounds(-40, 0))
    cube = cube.extract(lon_bounds(30, 90))
    cube = unit_converter_k_to_C(cube)
    result250 = cube.extract(pressure_level(expt,25000))
    result500 = cube.extract(pressure_level(expt,50000))
    
    return result250, result500
    
def load_expt_slp(expt):

    cube_list = iris.load(sixhr_file_location(expt, 'psl'))#[0] 
    cube=cube_concatenator(cube_list) 
    cube = cube.extract(year_bounds(1990, 1991))
    #iris.coord_categorisation.add_month_number(cube, 'time', name='month_number') 
    #cube = cube.extract(iris.Constraint(month_number=3))
    
    cube = cube.extract(lat_bounds(-40, 0))
    cube = cube.extract(lon_bounds(30, 90))
    
    return cube
    
def load_expt_wd(expt):
    cubeL1 = iris.load(sixhr_file_location(expt, 'ua'), year_bounds(1990, 1991)) 
    cubeL2 = iris.load(sixhr_file_location(expt, 'va'), year_bounds(1990, 1991)) 

    cube1=cube_concatenator(cubeL1)
    cube2=cube_concatenator(cubeL2)
    
    #iris.coord_categorisation.add_month_number(cube1, 'time', name='month_number') 
    #cube1 = cube1.extract(iris.Constraint(month_number=3))
    #iris.coord_categorisation.add_month_number(cube2, 'time', name='month_number') 
    #cube2 = cube2.extract(iris.Constraint(month_number=3))
    
    cube10_uL = iris.load(sixhr_file_location(expt, 'uas'), year_bounds(1990, 1991))
    cube10_vL = iris.load(sixhr_file_location(expt, 'uas'), year_bounds(1990, 1991))
    cube10_u = cube_concatenator(cube10_uL)
    cube10_v = cube_concatenator(cube10_vL)
    
   # iris.coord_categorisation.add_month_number(cube10_u, 'time', name='month_number') 
   # cube10_u = cube10_u.extract(iris.Constraint(month_number=3))
   # iris.coord_categorisation.add_month_number(cube10_v, 'time', name='month_number') 
   # cube10_v = cube10_v.extract(iris.Constraint(month_number=3))
   
    result250 = calc_windspeed(cube1.extract(pressure_level(expt,25000)), cube2.extract(pressure_level(expt,25000)))
    result1000 = calc_windspeed(cube10_u, cube10_v)
    result850 = calc_windspeed(cube1.extract(pressure_level(expt,85000)), cube2.extract(pressure_level(expt,85000)))
   
    u850 = cube1.extract(pressure_level(expt,85000))
    v850 = cube2.extract(pressure_level(expt,85000)) 
    pickle.dump(u850, open(starterp+expt+'_u850_'+p_file, "wb" ))
    pickle.dump(v850, open(starterp+expt+'_v850_'+p_file, "wb" ))
    
    result250 = result250.extract(lat_bounds(-40, 0))
    result250 = result250.extract(lon_bounds(30, 90))
    result850 = result850.extract(lat_bounds(-40, 0))
    result850 = result850.extract(lon_bounds(30, 90))
    result1000 = result1000.extract(lat_bounds(-40, 0))
    result1000 = result1000.extract(lon_bounds(30, 90))
                  
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
  
  thresh = 1013.25
  
  if expt in ['ERA5']:
      thresh = thresh * 100
           
  da = xr.DataArray.from_iris(slp)
  mslp = da.min().values
  coords = da.where(da==mslp, drop=True).squeeze()
  mslp_lat = coords.latitude.values
  mslp_lon = coords.longitude.values
  if size(mslp_lon) > 1:
      mslp_lon=mslp_lon[0] #if 2+ identical minima take first value 
  if size(mslp_lat) > 1:
      mslp_lat=mslp_lat[0] 

  return mslp, mslp_lon, mslp_lat
      
def calc_mslp2(counter, value, expt, tc_id, mslp, mslp_lon, mslp_lat):

  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)[counter]
  
  thresh = 1013.25
  
  if expt in ['ERA5']:
      thresh = thresh * 100
    
  track_radius=4
  max_lat = mslp_lat + track_radius
  min_lat = mslp_lat - track_radius
  min_lon = mslp_lon - track_radius
  max_lon = mslp_lon + track_radius
      
  domain_slp = slp.extract(lon_bounds(min_lon, max_lon) & lat_bounds(min_lat, max_lat))
      
  da = xr.DataArray.from_iris(domain_slp)
  mslp = da.min().values
  coords = da.where(da==mslp, drop=True).squeeze()
  mslp_lat = coords.latitude.values
  mslp_lon = coords.longitude.values
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

  with warnings.catch_warnings():
      warnings.simplefilter('ignore', UserWarning)
      u850 = unpickle_cubes(starterp+expt+'_u850_'+p_file)
      v850 = unpickle_cubes(starterp+expt+'_v850_'+p_file)

      ua=u850[counter]
      va=v850[counter]

      delta_latitude = 180/180.0
     
      sample_points = [('longitude', ua.coord('longitude').points),('latitude',  np.linspace(90 - 0.5 * delta_latitude,-90 + 0.5 * delta_latitude,180))]
      ua_r = ua.interpolate(sample_points, iris.analysis.Linear())
      va_r = va.interpolate(sample_points, iris.analysis.Linear())
  
  w = VectorWind(ua_r, va_r)
  
  vort = w.vorticity()
  

  vort_radius=4
  
  lat_lower = mslp_lat - vort_radius
  lat_upper = mslp_lat + vort_radius
  lon_lower = mslp_lon - vort_radius
  lon_upper = mslp_lon + vort_radius

  vort_min=0
  
  vort=vort.extract(lat_bounds(lat_lower, lat_upper) & lon_bounds(lon_lower, lon_upper))
  
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

#"Goal: Allowing for a single timestep failure
#"a) Loops through all points and identifies points with a tracking ID of 0, but where the previous and following timesteps have a tracking ID of 1.
#"b) If a point meets this criterion, the latitude and longitude of this point is then assessed to determine if it is within 4.5 degrees of the latitude and longitude of both the previous and following timesteps.
#"c) If this point meets the above criterion, the tracking ID is changed from a 0 to a 1.
#"This step is necessary to reduce broken tracks associated with the weakening of the system during intermittent 6-hourly intervals.

  
  radius=4.5
  
  if df.loc[counter, 'tc_id'] == 0 and df.loc[counter-1, 'tc_id'] == 1 and df.loc[counter+1, 'tc_id'] == 1:
      
      lon1_min = df.loc[counter, 'mslp_lon'] - radius
      lon1_max = df.loc[counter, 'mslp_lon'] + radius
      lat1_min = df.loc[counter, 'mslp_lat'] - radius
      lat1_max = df.loc[counter, 'mslp_lat'] + radius
      lon2 = df.loc[counter, 'mslp_lon'] 
      lat2 = df.loc[counter, 'mslp_lat'] 

      if lon1_min <= lon2 <= lon1_max and lat1_min <= lat2 <= lat1_max:
          df.loc[counter,'tc_id'] = 1
          #df.replace({'tc_id': counter}, 1)
         
  return df
  
def assign_filter(counter, df):

#"Goal: Grouping events
#"a) Each point is then assigned a character string - ‘New’, ‘Same’ or ‘-’ based on different criteria - this is necessary for further filtering and numbering of events.
#"b) Loops through all timesteps and assigns these characters based on the following criteria:
#"  i) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘0’, this indicates the start of a new event, and the timestep is assigned the string ‘New’.
#"  ii) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘1’, this indicates the continuation of an event, and the timestep is assigned the string ‘Same’.
#"  iii) If the current timestep (it) has a tracking ID of ‘0’, it is not associated with a TC event and is assigned the string ‘-’.
  
  if df.at[counter, 'tc_id'] == 1 and df.at[counter-1, 'tc_id'] == 0:
      df.loc[counter,'tc_event'] = 'New'
      #df.replace({'tc_event': counter}, 'New')  
  elif df.at[counter, 'tc_id'] == 1 and df.at[counter-1, 'tc_id'] == 1:
      df.loc[counter,'tc_event'] = 'Same'
      #df.replace({'tc_event': counter}, 'Same')   
  elif df.at[counter, 'tc_id'] == 0:
      df.loc[counter,'tc_event'] = '-'
     # df.replace({'tc_event': counter}, '-')
      
  
  
  return df
  
def time_threshold1(counter,df):

#"Goal: Applying minimum lifetime criterion
#"This step eliminates events that do not last for 2 days.
#"a) First, we loop through all timesteps.
#"  i) If the current timestep (it) has been assigned the string ‘New’, we consider the following 7 timesteps (it+1, it+2,....it+7).#
#"  ii) If any of the following 7 timesteps contain a ‘-’ character, this indicates that the event has not spanned 2 days (8 timesteps) and the character string of the current timestep (it) is changed from ‘New’ to ‘-’.

  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if df.at[counter, 'tc_event'] == 'New':
      if df.at[counter+1, 'tc_event'] == '-' or df.at[counter+2, 'tc_event'] == '-' or df.at[counter+3, 'tc_event'] == '-' or df.at[counter+4, 'tc_event'] == '-' or df.at[counter+5, 'tc_event'] == '-' or df.at[counter+6, 'tc_event'] == '-' or df.at[counter+7, 'tc_event'] == '-':  
           df.loc[counter,'tc_event'] = '-'         
	  # df.replace({'tc_event': counter}, '-') 
	   
  
    
  return df 
  
def time_threshold2(counter,df): 
#"b) Next, we loop through all timesteps a second time.
#"  i) If the current timestep (it) has been assigned the string ‘Same’ and the previous timestep (it-1) has been assigned the ‘-’ string, the current timestep (it) is changed from ‘Same’ to ‘-’. 
#"  i) Such cases will only arise from the previous step, in which ‘New’ has been changed to ‘-’ since the event did not meet the minimum lifetime criteria.


  if df.at[counter, 'tc_event'] == 'Same' and df.at[counter-1, 'tc_event'] == '-': 
       df.loc[counter,'tc_event'] = '-'  
       #df.replace({'tc_event': counter}, '-') 

  
  
  return df
  
def number_events1(counter, event_number,df):

#"Goal: Numbering events
#"This is the final step which numbers all events.
#"a) First, we set the event_tracker to 0.
#"b) Next, we loop through all timesteps.
#"  i) If the current timestep (it) has the character string ‘New’, the event tracker is updated (event_tracker = event_tracker+1), and this new value then becomes the event number (event_number=event_tracker).
#"  ii) If the current timestep (it) does not have the character string ‘New’, the timestep is assigned an event number of 999.



  if df.at[counter, 'tc_event'] == 'New':
      event_number = event_number+1
      df.loc[counter,'tc_number'] = int(event_number)
     # df.replace({'tc_number': counter}, event_number)
  else:
      df.loc[counter,'tc_number'] = int(999)
      #df.replace({'tc_number': counter}, 999)
       
  
  
  return df, event_number
  
def number_events2(counter,df): 
#"c) We then loop through all timesteps for a second time.
#"  i) If the current timestep (it) has the character string ‘Same’, the event number is equal to the event number of the previous timestep (it-1). i.e. event_number(it) = event_number(it-1)


  if df.at[counter, 'tc_event'] == 'Same':
      df.loc[counter,'tc_number'] = df.at[counter-1, 'tc_number']
      #df.replace({'tc_number': counter}, df.at[counter-1, 'tc_number']) #inplace = True?
 
  return df	  

###############################
#Execution function(s)
###############################

if pre_processor_experiments:
    print('entering pre-processor routine')
   
    #green_list = create_greenlist(vari_list)
    green_list =obs_list#+green_list
    
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
    df = df.astype({"date":str, "mslp": float, "mslp_lon": float, "mslp_lat": float, "max_wspd": float, "vort_min": float, \
                     "wc_temp": float, "tc_id": int, "tc_event": str,"tc_number": int})

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)
        time = ws250.coord('time')
        #print(repr(time.units))
       	
        nl=ws250.coord('time').points #time coords
	
        tc_id = 0

        for counter, value in enumerate(nl):
            
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', UserWarning)

                if(counter == 0) or (tc_id == 0): #ith-1 tc_id
                    mslp, mslp_lon, mslp_lat = calc_mslp1(counter,value, expt, tc_id) 
                elif(tc_id == 1): 
                    mslp, mslp_lon, mslp_lat = calc_mslp2(counter,value, expt, tc_id, mslp, mslp_lon, mslp_lat) 
		    	 	    
                max_wspd = calc_maxwind(counter, mslp_lon, mslp_lat) 	    
                wspd_threshold = ws_thresh(abs(ws250.coord('longitude').points[2]-ws250.coord('longitude').points[1])*111) 	    
                vort_min = calc_vort(counter, mslp_lon, mslp_lat)     
                wc_temp, avg_temp_500_250 = calc_warm_core(counter, mslp_lon, mslp_lat) 
                avg_wspd_250, avg_wspd_850 = calc_windregion(counter, mslp_lon, mslp_lat)
           	                      
                if max_wspd >= wspd_threshold and vort_min <= -0.000035 and wc_temp >= (avg_temp_500_250 + 1.) and avg_wspd_250 < avg_wspd_850:    
                    tc_id=1
                else:
                    tc_id=0

            df.at[counter,'date'] = str(time.units.num2date(value))				
            df.at[counter,'tc_id'] = tc_id
            df.at[counter,'vort_min'] = vort_min
            df.at[counter,'mslp'] = mslp
            df.at[counter,'mslp_lon'] = mslp_lon
            df.at[counter,'mslp_lat'] = mslp_lat
            df.at[counter,'max_wspd'] = max_wspd
            df.at[counter,'wc_temp'] = wc_temp
	    
	    
            #df.at[counter,'tc_event'] = "-"
            #df.at[counter,'tc_number'] = 0
       
        pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" )) #dataframe of all variables
	
    print('calc stage 1 complete')

if processor_calculations2:	
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        print(expt)
    
        df = unpickle_cubes(starterp+expt+'_df_'+p_file)
        end_count = len(df.index)
 
        for index, row in islice(df.iterrows(), 1, end_count):
            #print(df.loc[index, 'tc_number'])
            #print('ts')
            df = tstep_fail_allowance(index, df)
		
        for index, row in islice(df.iterrows(), 1, None):
  
            df = assign_filter(index,df)
		
        for index, row in islice(df.iterrows(), None, end_count-7):
       
            df = time_threshold1(index,df)
		
        for index, row in islice(df.iterrows(), 1, None):
      
            df = time_threshold2(index,df)

        event_number = 0		
        for index, row in df.iterrows():
 
            df, event_number = number_events1(index, event_number,df)
	
        for index, row in islice(df.iterrows(), 1, None):

            df = number_events2(index,df)
	
        for index, row in df.iterrows():

            if df.loc[index, 'tc_number'] == int(999):
                df.drop(index)
		
        pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))	
  		            
        #Write output to text file
        np.savetxt(r'MODEL_output.txt', df, fmt='%s')
	
    print('Tracking complete for '+expt)

