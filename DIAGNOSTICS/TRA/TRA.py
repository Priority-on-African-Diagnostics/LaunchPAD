# -*- coding: utf-8 -*-

##############################
###-----Import Modules-----###
##############################

import numpy as np
import cf
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

    cube_list = iris.load(monthly_file_location(expt, 'ta'))[1]# &  
    #print(cube_list)
    #cube=cube_list[1]        
    #cube = cube_concatenator(cube_list) 
    cube = cube_list.extract(year_bounds(1990, 1991))
    cube = unit_converter_k_to_C(cube)
    result250 = cube.extract(pressure_level(expt,25000))
    result500 = cube.extract(pressure_level(expt,50000))
    
    return result250, result500
    
def load_expt_slp(expt):

    cube_list = iris.load(monthly_file_location(expt, 'psl'))[0] 
  
    cube = cube_list.extract(year_bounds(1990, 1991))
    
    return cube
    
def load_expt_wd(expt):
    cube1 = iris.load(monthly_file_location(expt, 'ua'), year_bounds(1990, 1991)) 
    #cube1 = cube_concatenator(cube_list1)
    cube2 = iris.load(monthly_file_location(expt, 'va'), year_bounds(1990, 1991)) 
    cube1=cube1[0]
    cube2=cube2[0]
    #cube2 = cube_concatenator(cube_list2)
   
    result250 = calc_windspeed(cube1.extract(pressure_level(expt,25000)), cube2.extract(pressure_level(expt,25000)))
    result1000 = calc_windspeed(cube1.extract(pressure_level(expt,100000)), cube2.extract(pressure_level(expt,100000)))
    result850 = calc_windspeed(cube1.extract(pressure_level(expt,85000)), cube2.extract(pressure_level(expt,85000)))
   
    u850 = cube1.extract(pressure_level(expt,85000))
    v850 = cube2.extract(pressure_level(expt,85000)) 
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
  #res = (abs(lon[2]-lon[1])) * 111

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
  
def calc_mslp(counter, value, expt, tc_id): 

  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)

  ni = slp.coord('longitude').points #  list of lon coords
  nj = slp.coord('latitude').points #  list of lat coords

  mslp=1013.25
  
  if(counter == 0) or (tc_id == 0): #ith-1 tc_id
    for j in nj:
      latConstraint = iris.Constraint(latitude=j)
      
      for i in ni:     
        lonContraint = iris.Constraint(longitude=i) 
       
        if(slp.extract(lonContraint & latConstraint)[counter].data < mslp):
          mslp = slp.extract(lonContraint & latConstraint)[counter].data
	  	  
          mslp_lon = i #longitude
          mslp_lat = j #latitude

  elif(tc_id == 1): #ith-1 tc_id
    
    track_radius=4
    
    dif_lat=abs(slp.coord('latitude').points[2]-cube.coord('latitude').points[1])
    dif_lon=abs(slp.coord('longitude').points[2]-cube.coord('longitude').points[1])    

    for j in range(mslp_lat - track_radius, int_mslp_lat + track_radius, diff_lat):
        latConstraint = iris.Constraint(latitude=j)
	
        for i in range(mslp_lon - track_radius, mslp_lon + track_radius, diff_lon):
            lonContraint = iris.Constraint(longitude=i)    

            if(slp.extract(lonContraint & latConstraint)[counter].data < mslp):
                mslp = slp.extract(lonContraint & latConstraint)[counter].data
                mslp_lon = i
                mslp_lat = j
	  
  else:
      print('none of criteria met')
    
  return mslp, mslp_lon, mslp_lat 
 
def calc_windregion(counter, mslp_lon, mslp_lat):

  avg_radius=3
  
  ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)
  ws850 = unpickle_cubes(starterp+expt+'_ws850_'+p_file)

  int_lat_lower = mslp_lat - avg_radius
  int_lat_upper = mslp_lat + avg_radius
  int_lon_lower = mslp_lon - avg_radius
  int_lon_upper = mslp_lon + avg_radius
  
  avg_wspd_250 = ws250.extract(lat_bounds(int_lat_lower, int_lat_upper) & lon_bounds(int_lon_lower, int_lon_upper))[counter]
  avg_wspd_850 = ws850.extract(lat_bounds(int_lat_lower, int_lat_upper) & lon_bounds(int_lon_lower, int_lon_upper))[counter]

  return avg_wspd_250,avg_wspd_850
  
def calc_maxwind(counter, mslp_lon, mslp_lat):

  wind_radius=5
  
  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)
  
  dif_lat=abs(slp.coord('latitude').points[2]-cube.coord('latitude').points[1])
  dif_lon=abs(slp.coord('longitude').points[2]-cube.coord('longitude').points[1])
  
  int_lat_lower = mslp_lat - wind_radius
  int_lat_upper = mslp_lat + wind_radius
  int_lon_lower = mslp_lon - wind_radius
  int_lon_upper = mslp_lon + wind_radius

  max_wspd = 0
  
  wsp10m = unpickle_cubes(starterp+expt+'_ws1000_'+p_file)

  for j in range(int_lat_lower-wind_radius,int_lat_upper+wind_radius, diff_lat):
    latContraint = iris.Constraint(latitude=j)
    
    for i in range(int_lon_lower-wind_radius,int_lon_upper+wind_radius, diff_lon):
      lonContraint = iris.Constraint(longitude=i)
      
      if wspd10.extract(latContraint & lonContraint)[counter].data > max_wspd:
          max_wspd = wspd10.extract(latContraint & lonContraint)[counter].data

  return max_wspd
  
def calc_vort(counter, mslp_lon, mslp_lat):

  u850 = unpickle_cubes(starterp+expt+'_u850_'+p_file)
  v850 = unpickle_cubes(starterp+expt+'_wv850_'+p_file)

  u=u850[counter]
  v=v850[counter]
  
  vort=cf.relative_vorticity(u,v)
  
  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)
  
  dif_lat=abs(slp.coord('latitude').points[2]-cube.coord('latitude').points[1])
  dif_lon=abs(slp.coord('longitude').points[2]-cube.coord('longitude').points[1])

  vort_radius=4
  
  int_lat_lower = mslp_lat - vort_radius
  int_lat_upper = mslp_lat + vort_radius
  int_lon_lower = mslp_lon - vort_radius
  int_lon_upper = mslp_lon + vort_radius

  vort_min=0

  for j in range(int_lat_lower,int_lat_upper, diff_lat):
    for i in range(int_lon_lower,int_lon_upper, diff_lon):
        if vort[counter,j,i] <vort_min:
            vort_min = vort[counter,j,i]

  return vort_min
  
def calc_warm_core(counter, mslp_lon, mslp_lat):
  warm_core_radius=2
  
  slp = unpickle_cubes(starterp+expt+'_slp_'+p_file)

  dif_lat=abs(slp.coord('latitude').points[2]-cube.coord('latitude').points[1])
  dif_lon=abs(slp.coord('longitude').points[2]-cube.coord('longitude').points[1])
  
  #Creates range bounds for avg temp
  int_lat_lower = mslp_lat - warm_core_radius
  int_lat_upper = mslp_lat + warm_core_radius
  int_lon_lower = mslp_lon - warm_core_radius
  int_lon_upper = mslp_lon + warm_core_radius
  
  t250 = unpickle_cubes(starterp+expt+'_t250_'+p_file)[counter]
  t500 = unpickle_cubes(starterp+expt+'_t500_'+p_file)[counter]
  
  int_avg_temp_500_250 = iris.analysis.maths.multiply(iris.analysis.maths.add(t500, t250), 0.5)
  
  wc_temp = -100
  for j in range(int_lat_lower,int_lat_upper, diff_lat):
    latContraint = iris.Constraint(latitude=j)
    for i in range(int_lon_lower,int_lon_upper, diff_lon):
      lonContraint = iris.Constraint(longitude=i)
      if int_avg_temp_500_250.extract(latContraint & lonContraint).data > wc_temp:
          wc_temp = int_avg_temp_500_250.extract(latContraint & lonContraint).data
	  
  int_avg_temp_500_250 = int_avg_temp_500_250.extract(lat_bounds(int_lat_lower, int_lat_upper) & lon_bounds(int_lon_lower, int_lon_upper))

  return wc_temp, avg_temp_500_250
  
def tstep_fail_allowance(counter):

#"Goal: Allowing for a single timestep failure
#"a) Loops through all points and identifies points with a tracking ID of 0, but where the previous and following timesteps have a tracking ID of 1.
#"b) If a point meets this criterion, the latitude and longitude of this point is then assessed to determine if it is within 4.5 degrees of the latitude and longitude of both the previous and following timesteps.
#"c) If this point meets the above criterion, the tracking ID is changed from a 0 to a 1.
#"This step is necessary to reduce broken tracks associated with the weakening of the system during intermittent 6-hourly intervals.

  radius=4.5
  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
   
  if df.loc[counter, 'tc_id'] == 0 and df.loc[counter-1, 'tc_id'] == 1 and df.loc[counter+1, 'tc_id'] ==1:
      lon1_min = df.loc[counter, 'mslp_lon'] - radius
      lon1_max = df.loc[counter, 'mslp_lon'] + radius
      lat1_min = df.loc[counter, 'mslp_lat'] - radius
      lat1_max = df.loc[counter, 'mslp_lat'] + radius
      lon2 = df.loc[counter, 'mslp_lon'] 
      lat2 = df.loc[counter, 'mslp_lat'] 

      if lon1_min <= lon2 <= lon1_max and lat1_min <= lat2 <= lat1_max:
          df.replace({'tc_id': counter}, 1)
      
  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
     
  return None
  
def assign_filter(counter):

#"Goal: Grouping events
#"a) Each point is then assigned a character string - ‘New’, ‘Same’ or ‘-’ based on different criteria - this is necessary for further filtering and numbering of events.
#"b) Loops through all timesteps and assigns these characters based on the following criteria:
#"  i) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘0’, this indicates the start of a new event, and the timestep is assigned the string ‘New’.
#"  ii) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘1’, this indicates the continuation of an event, and the timestep is assigned the string ‘Same’.
#"  iii) If the current timestep (it) has a tracking ID of ‘0’, it is not associated with a TC event and is assigned the string ‘-’.

  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  
  if df.loc[counter, 'tc_id'] == 1 and df.loc[counter-1, 'tc_id'] == 0:
      df.replace({'tc_event': counter}, 'New')  
  elif df.loc[counter, 'tc_id'] == 1 and df.loc[counter-1, 'tc_id'] == 1:
      df.replace({'tc_event': counter}, 'Same')   
  elif df.loc[counter, 'tc_id'] == 0:
      df.replace({'tc_event': counter}, '-')
      
  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
  
  return None
  
def time_threshold1(counter):

#"Goal: Applying minimum lifetime criterion
#"This step eliminates events that do not last for 2 days.
#"a) First, we loop through all timesteps.
#"  i) If the current timestep (it) has been assigned the string ‘New’, we consider the following 7 timesteps (it+1, it+2,....it+7).#
#"  ii) If any of the following 7 timesteps contain a ‘-’ character, this indicates that the event has not spanned 2 days (8 timesteps) and the character string of the current timestep (it) is changed from ‘New’ to ‘-’.

  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if df.loc[counter, 'tc_event'] == 'New':
      if df.loc[counter+1, 'tc_event'] == '-' or df.loc[counter+2, 'tc_event'] == '-' or df.loc[counter+3, 'tc_event'] == '-' or df.loc[counter+4, 'tc_event'] == '-' or df.loc[counter+5, 'tc_event'] == '-' or df.loc[counter+6, 'tc_event'] == '-' or df.loc[counter+7, 'tc_event'] == '-':  
           df.replace({'tc_event': counter}, '-') 
	   
  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
    
  return None 
  
def time_threshold2(counter): 
#"b) Next, we loop through all timesteps a second time.
#"  i) If the current timestep (it) has been assigned the string ‘Same’ and the previous timestep (it-1) has been assigned the ‘-’ string, the current timestep (it) is changed from ‘Same’ to ‘-’. 
#"  i) Such cases will only arise from the previous step, in which ‘New’ has been changed to ‘-’ since the event did not meet the minimum lifetime criteria.

  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if df.loc[counter, 'tc_event'] == 'Same' and df.loc[counter-1, 'tc_event'] == '-': 
       df.replace({'tc_event': counter}, '-') 

  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
  
  return None
  
def number_events1(counter, event_number):

#"Goal: Numbering events
#"This is the final step which numbers all events.
#"a) First, we set the event_tracker to 0.
#"b) Next, we loop through all timesteps.
#"  i) If the current timestep (it) has the character string ‘New’, the event tracker is updated (event_tracker = event_tracker+1), and this new value then becomes the event number (event_number=event_tracker).
#"  ii) If the current timestep (it) does not have the character string ‘New’, the timestep is assigned an event number of 999.


  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if df.loc[counter, 'tc_event'] == 'New':
      event_number = event_number+1
      df.replace({'tc_number': counter}, event_number)
  else:
      df.replace({'tc_number': counter}, 999)
       
  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
  
  return None
  
def number_events2(counter): 
#"c) We then loop through all timesteps for a second time.
#"  i) If the current timestep (it) has the character string ‘Same’, the event number is equal to the event number of the previous timestep (it-1). i.e. event_number(it) = event_number(it-1)

  df = unpickle_cubes(starterp+expt+'_df_'+p_file)
  if df.loc[counter, 'tc_event'] == 'Same':
      df.replace({'tc_number': counter}, df.loc[counter-1, 'tc_number'])

  pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
  
  return None	  

###############################
#Execution function(s)
###############################

if pre_processor_experiments:
    print('entering pre-processor routine')
   
    green_list = create_greenlist(vari_list)
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
	
if processor_calculations1:

    df = pd.DataFrame(columns=['mslp','mslp_lon','mslp_lat','max_wspd','vort_min','wc_temp','tc_id','tc_event','tc_number'])

    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        tc_id = 0 #to allow dictionary building
        vort_min = 0 #- dictionary with default to Nan otherwise: note: not set later so can delete these
        mslp = 0
        mslp_lat = 0
        mslp_lon = 0
        max_wspd = 0
        wc_temp = 0
        tc_event = '-'
        tc_number = 0
        tc_gate=True
    
        ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)
	
        threshold = ws_thresh(abs(ws250.coord('longitude').points[2]-ws250.coord('longitude').points[1])*111)
       	
        nl=ws250.coord('time').points #time coords

        for counter, value in enumerate(nl):
            mslp, mslp_lon, mslp_lat = calc_mslp(counter,value, expt, tc_id) #this will only take first mslp low it encounters
            max_wspd = calc_maxwind(counter, mslp_lon, mslp_lat)           
            if(max_wspd >= wspd_threshold): 
                vort_min = calc_vort(counter, mslp_lon, mslp_lat)
                if(vort_min <= -0.000035):    
                    wc_temp, avg_temp_500_250 = calc_warm_core(counter, mslp_lon, mslp_lat)		    
                    if(wc_temp >= (avg_temp_500_250.data + 1)):
                        avg_wspd_250, avg_wspd_850 = calc_windregion(counter, mslp_lon, mslp_lat)
                        if(avg_wspd_250.data < avg_wspd_850.data): 
                            tc_id=1
                            tc_gate = True
                        else:
                            tc_id=0
                            tc_gate = True
            if tc_gate:
                df.at[counter,'tc_id'] = tc_id
                df.at[counter,'vort_min'] = vort_min
                df.at[counter,'mslp'] = mslp
                df.at[counter,'mslp_lon'] = mslp_lon
                df.at[counter,'mslp_lat'] = mslp_lat
                df.at[counter,'max_wspd'] = max_wspd
                df.at[counter,'wc_temp'] = wc_temp
            tc_gate = False 

        pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" )) #dataframe of all variables

if processor_calculations2:	
    green_list = unpickle_cubes(starterp+'green_list'+p_file)
    for expt in green_list:
    
        ws250 = unpickle_cubes(starterp+expt+'_ws250_'+p_file)
        nl=ws250.coord('time').points

        end_count = len(nl)
	#must loop through all timesteps to update them before proceeding to next section
        for counter, value in enumerate(nl):
            if counter == 0 or counter == end_count: #no previous timestep or no forward timestep
                pass
            else:
                tstep_fail_allowance(counter)
		
        for counter, value in enumerate(nl):
            if counter ==0:
                pass
            else:
                assign_filter(counter)
		
        for counter, value in enumerate(nl):
            if counter >= nl-7:
                pass
            else:
                time_threshold1(counter)
		
        for counter, value in enumerate(nl):
            if counter ==0:
                pass
            else:
                time_threshold2(counter)

        event_number = 0		
        for counter, value in enumerate(nl):
            number_events1(counter, event_number)
	
        for counter, value in enumerate(nl):
            if counter ==0:
                pass
            else:
                number_events2(counter)

        df = unpickle_cubes(starterp+expt+'_df_'+p_file)
	
        for counter, value in enumerate(nl):
            if df.loc[counter, 'tc_number'] == 999:
                df.drop(counter)
        pickle.dump(df, open(starterp+expt+'_df_'+p_file, "wb" ))
		            
        #Write output to text file
        np.savetxt(r'MODEL_output.txt', df.values, fmt='%d')
	
    print('Tracking complete for '+expt)

