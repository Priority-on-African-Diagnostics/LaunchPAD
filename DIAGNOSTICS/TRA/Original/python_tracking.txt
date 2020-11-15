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

#######################################
###-----Open NetCDF & Read Data-----###
#######################################

#Open File------------------------------------------------------------------------------------------------------------------------------

ncfile= Dataset('../ERA5_Jan1990.nc','r')

#Select variables-----------------------------------------------------------------------------------------------------------------------

lon = ncfile.variables['longitude'][:]
lat = ncfile.variables['latitude'][:]

#select temp at 500 and 250 hPa
temp500 = ncfile.variables['t'][:,2,:,:] - 273.15
temp250 = ncfile.variables['t'][:,0,:,:] - 273.15

#select winds & compute wind speed at 850 hPa
u850 = ncfile.variables['u'][:,4,:,:]
#u850 = u850 * units.meter / units.second
v850 = ncfile.variables['v'][:,4,:,:]
#v850 = v850 * units.meter / units.second
wspd850 = np.sqrt(u850**2+v850**2)
wspd850=np.asarray(wspd850)

#select winds & compute wind speed at 250 hPa
u250 = ncfile.variables['u'][:,0,:,:]
#u250 = u250 * units.meter / units.second
v250 = ncfile.variables['v'][:,0,:,:]
#v250 = v250 * units.meter / units.second
wspd250 = np.sqrt(u250**2+v250**2)
wspd250=np.asarray(wspd250)

#select winds & compute wind speed at surface (10m)
u10m = ncfile.variables['u10'][:,:,:]
v10m = ncfile.variables['v10'][:,:,:]
wspd10m=np.sqrt(u10m**2+v10m**2)

slp = ncfile.variables['msl'][:,:,:] / 100
time = ncfile.variables['time'][:]
date=time
levels=ncfile.variables['level'][:]

ni=len(lon) #lon points
nj=len(lat) #lat points
nk=len(levels) #no of vertical levels
nl=len(time) #no of timesteps

#Create empty arrays---------------------------------------------------------------------------------------------------------------------

mslp=np.zeros((nl))
mslp_lon=np.zeros((nl))
mslp_lat=np.zeros((nl))
mslp_lon_ind=np.zeros((nl))
mslp_lat_ind=np.zeros((nl))
max_wspd=np.zeros((nl))
vort=np.zeros((nl,nj,ni))
vort_min=np.zeros((nl))
wc_temp=np.zeros((nl))
avg_temp_500_250=np.zeros((nl))
tc_id=np.zeros((nl))
tc_event=np.empty(nl,dtype='<U4')
tc_number=np.zeros((nl))
avg_wspd_250=np.zeros((nl))
avg_wspd_850=np.zeros((nl))
tc_number=np.zeros((nl))

#------------Convert time to actual times-----------------------------------------------------------------------------------------------

date=num2date(time[:],units='hours since 1900-1-1 00:00:00',calendar='standard') 

#---------------------------------------------------------------------------------------------------------------------------------------

#############################
###------Subroutines------###
#############################

#------------Calculate MSLP--------------------------------------------------------------

def calc_mslp(l):

#######################################################SECTION COMPLETE#########################################################
"**NOTE this subroutine has already been converted by Tom"

  mslp[l]=1013.25
  
  if(l == 0) or (tc_id[l-1] == 0):
    for j in range(0,nj):
      for i in range(0,ni):

        if(slp[l][j][i] < mslp[l]):
          mslp[l]  = slp[l][j][i] 
          mslp_lon[l] = lon[i]
          mslp_lon_ind[l] = i
          mslp_lat[l] = lat[j]
          mslp_lat_ind[l] = j

  elif(tc_id[l-1] == 1):
    
    track_radius=4
    dif_lat=abs(lat[2]-lat[1])
    dif_lon=abs(lon[2]-lon[1])

    lat_lower=mslp_lat_ind[l-1]-(track_radius/dif_lat)
    lat_upper=mslp_lat_ind[l-1]+(track_radius/dif_lat)+1
    lon_lower=mslp_lon_ind[l-1]-(track_radius/dif_lon)
    lon_upper=mslp_lon_ind[l-1]+(track_radius/dif_lon)+1
    int_lat_lower=lat_lower.astype(int)
    int_lat_upper=lat_upper.astype(int)
    int_lon_lower=lon_lower.astype(int)
    int_lon_upper=lon_upper.astype(int)

    if(int_lat_lower <= 0):int_lat_lower=0
    if(int_lat_upper >= nj):int_lat_upper=nj
    if(int_lon_lower <= 0):int_lon_lower=0
    if(int_lon_upper >= ni):int_lon_upper=ni

    for j in range(int_lat_lower,int_lat_upper):
      for i in range(int_lon_lower,int_lon_upper):

        if(slp[l][j][i] < mslp[l]):
          mslp[l]  = slp[l][j][i]
          mslp_lon[l] = lon[i]
          mslp_lon_ind[l] = i
          mslp_lat[l] = lat[j]
          mslp_lat_ind[l] = j
    
  return mslp[l], mslp_lon[l], mslp_lat[l], mslp_lon_ind[l], mslp_lat_ind[l]

#---------------Calc windregion---------------------------------------------------------------------

def calc_windregion(l):

#######################################################SECTION COMPLETE#########################################################
"**NOTE this subroutine has already been converted by Tom"

  #Calculates the number of indices needed for 5 degrees
  avg_radius=3

  dif_lat=abs(lat[2]-lat[1])
  dif_lon=abs(lon[2]-lon[1])
  
  #Creates range bounds for avg temp
  lat_lower_avg=mslp_lat_ind[l]-(avg_radius/dif_lat)
  lat_upper_avg=mslp_lat_ind[l]+(avg_radius/dif_lat)+1
  lon_lower_avg=mslp_lon_ind[l]-(avg_radius/dif_lon)
  lon_upper_avg=mslp_lon_ind[l]+(avg_radius/dif_lon)+1
  int_lat_lower_avg=lat_lower_avg.astype(int)
  int_lat_upper_avg=lat_upper_avg.astype(int)
  int_lon_lower_avg=lon_lower_avg.astype(int)
  int_lon_upper_avg=lon_upper_avg.astype(int)

  if(int_lat_lower_avg <= 0):int_lat_lower_avg=0
  if(int_lat_upper_avg >= nj):int_lat_upper_avg=nj
  if(int_lon_lower_avg <= 0):int_lon_lower_avg=0
  if(int_lon_upper_avg >= ni):int_lon_upper_avg=ni

  avg_wspd_250[l] = np.mean(wspd250[l,int_lat_lower_avg:int_lat_upper_avg,int_lon_lower_avg:int_lon_upper_avg])
  avg_wspd_850[l] = np.mean(wspd850[l,int_lat_lower_avg:int_lat_upper_avg,int_lon_lower_avg:int_lon_upper_avg])

  return avg_wspd_250[l],avg_wspd_850[l]

#---------------Calc max wspd---------------------------------------------------------------------

def calc_maxwind(l):

#######################################################SECTION COMPLETE#########################################################
"**NOTE this subroutine has already been converted by Tom"


  wind_radius=5
  dif_lat=abs(lat[2]-lat[1])
  dif_lon=abs(lon[2]-lon[1])

  lat_lower=mslp_lat_ind[l]-(wind_radius/dif_lat)
  lat_upper=mslp_lat_ind[l]+(wind_radius/dif_lat)+1
  lon_lower=mslp_lon_ind[l]-(wind_radius/dif_lon)
  lon_upper=mslp_lon_ind[l]+(wind_radius/dif_lon)+1
  int_lat_lower=lat_lower.astype(int)
  int_lat_upper=lat_upper.astype(int)
  int_lon_lower=lon_lower.astype(int)
  int_lon_upper=lon_upper.astype(int)

  if(int_lat_lower <= 0):int_lat_lower=0
  if(int_lat_upper >= nj):int_lat_upper=nj
  if(int_lon_lower <= 0):int_lon_lower=0
  if(int_lon_upper >= ni):int_lon_upper=ni

  max_wspd[l] = 0

  for j in range(int_lat_lower,int_lat_upper):
    for i in range(int_lon_lower,int_lon_upper):

      if(
        wspd10m[l][j][i] > max_wspd[l]
        ):
          max_wspd[l] = wspd10m[l][j][i]


  return max_wspd[l]

#------------Calc warm core------------------------------------------------------------------

def calc_warm_core(l):

#######################################################SECTION COMPLETE#########################################################
"**NOTE this subroutine has already been converted by Tom"

  #Calculates the number of indices needed for 5 degrees
  warm_core_radius=2
  avg_radius=5

  dif_lat=abs(lat[2]-lat[1])
  dif_lon=abs(lon[2]-lon[1])
  
  #Creates range bounds for avg temp
  lat_lower_avg=mslp_lat_ind[l]-(avg_radius/dif_lat)
  lat_upper_avg=mslp_lat_ind[l]+(avg_radius/dif_lat)+1
  lon_lower_avg=mslp_lon_ind[l]-(avg_radius/dif_lon)
  lon_upper_avg=mslp_lon_ind[l]+(avg_radius/dif_lon)+1
  int_lat_lower_avg=lat_lower_avg.astype(int)
  int_lat_upper_avg=lat_upper_avg.astype(int)
  int_lon_lower_avg=lon_lower_avg.astype(int)
  int_lon_upper_avg=lon_upper_avg.astype(int)

  if(int_lat_lower_avg <= 0):int_lat_lower_avg=0
  if(int_lat_upper_avg >= nj):int_lat_upper_avg=nj
  if(int_lon_lower_avg <= 0):int_lon_lower_avg=0
  if(int_lon_upper_avg >= ni):int_lon_upper_avg=ni

  #Creates range bounds for finding warm core
  lat_lower=mslp_lat_ind[l]-(warm_core_radius/dif_lat)
  lat_upper=mslp_lat_ind[l]+(warm_core_radius/dif_lat)+1
  lon_lower=mslp_lon_ind[l]-(warm_core_radius/dif_lon)
  lon_upper=mslp_lon_ind[l]+(warm_core_radius/dif_lon)+1
  int_lat_lower=lat_lower.astype(int)
  int_lat_upper=lat_upper.astype(int)
  int_lon_lower=lon_lower.astype(int)
  int_lon_upper=lon_upper.astype(int)

  if(int_lat_lower <= 0):int_lat_lower=0
  if(int_lat_upper >= nj):int_lat_upper=nj
  if(int_lon_lower <= 0):int_lon_lower=0
  if(int_lon_upper >= ni):int_lon_upper=ni

  int_avg_temp_500_250 = (temp500[l,:,:] + temp250[l,:,:]) / 2 
  
  wc_temp[l] = -100
  for j in range(int_lat_lower,int_lat_upper):
    for i in range(int_lon_lower,int_lon_upper):
      
      if(int_avg_temp_500_250[j][i] > wc_temp[l]): wc_temp[l] = int_avg_temp_500_250[j][i]
      
  avg_temp_500_250[l] = np.mean(int_avg_temp_500_250[int_lat_lower_avg:int_lat_upper_avg,int_lon_lower_avg:int_lon_upper_avg])

  return wc_temp[l],avg_temp_500_250[l]

#---------define windspeed threshold based on resolution-----------------------------------------------------------------------

def ws_thresh():

#######################################################SECTION COMPLETE#########################################################
"**NOTE this subroutine has already been converted by Tom"

  res = (abs(lon[2]-lon[1])) * 111

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

#--------------Calc relative vorticity over the grid and find the minimum value---------------------

def calc_vort(l):

"#######################----This section STILL needs to be converted by Tom----#######################"

"The goal of this subroutine is to:
"a) calculate the relative vorticity at 850hPa within an 8degree x 8degree block (4 degree radius) centered at the MSLP.
"b) Find the minimum vorticity within this block (within 4 degrees of the MSLP).

  u=u850[l,:,:]
  v=v850[l,:,:]
  vort[l]=cf.relative_vorticity(u,v)

  vort_radius=4
  dif_lat=abs(lat[2]-lat[1])
  dif_lon=abs(lon[2]-lon[1])

  lat_lower=mslp_lat_ind[l]-(vort_radius/dif_lat)
  lat_upper=mslp_lat_ind[l]+(vort_radius/dif_lat)+1
  lon_lower=mslp_lon_ind[l]-(vort_radius/dif_lon)
  lon_upper=mslp_lon_ind[l]+(vort_radius/dif_lon)+1
  int_lat_lower=lat_lower.astype(int)
  int_lat_upper=lat_upper.astype(int)
  int_lon_lower=lon_lower.astype(int)
  int_lon_upper=lon_upper.astype(int)

  if(int_lat_lower <= 0):int_lat_lower=0
  if(int_lat_upper >= nj):int_lat_upper=nj
  if(int_lon_lower <= 0):int_lon_lower=0
  if(int_lon_upper >= ni):int_lon_upper=ni

  vort_min[l]=0

  for j in range(int_lat_lower,int_lat_upper):
    for i in range(int_lon_lower,int_lon_upper):
      if(
      vort[l][j][i] < vort_min[l]
      ):
        vort_min[l]=vort[l][j][i]

  return vort_min[l]

#------------Filter------------------------------------------------------------------

"#######################----This section STILL needs to be converted by Tom----#######################"

def tstep_fail_allowance():

"Goal: Allowing for a single timestep failure
"a) Loops through all points and identifies points with a tracking ID of 0, but where the previous and following timesteps have a tracking ID of 1.
"b) If a point meets this criterion, the latitude and longitude of this point is then assessed to determine if it is within 4.5 degrees of the latitude and longitude of both the previous and following timesteps.
"c) If this point meets the above criterion, the tracking ID is changed from a 0 to a 1.
"This step is necessary to reduce broken tracks associated with the weakening of the system during intermittent 6-hourly intervals.

  radius=4.5
  for l in range(0,nl):

    if(tc_id[l] == 0) and (tc_id[l-1] == 1) and (tc_id[l+1] == 1):
      if((mslp_lat[l] <= (mslp_lat[l-1] + radius)) and (mslp_lat[l] >= mslp_lat[l-1])) or ((mslp_lat[l] >= (mslp_lat[l-1] - radius)) and (mslp_lat[l] <= mslp_lat[l-1])):
        if((mslp_lon[l] <= (mslp_lon[l-1] + radius)) and (mslp_lon[l] >= mslp_lon[l-1])) or ((mslp_lon[l] >= (mslp_lon[l-1] - radius)) and (mslp_lon[l] <= mslp_lon[l-1])):
          if((mslp_lat[l] <= (mslp_lat[l+1] + radius)) and (mslp_lat[l] >= mslp_lat[l+1])) or ((mslp_lat[l] >= (mslp_lat[l+1] - radius)) and (mslp_lat[l] <= mslp_lat[l+1])):
            if((mslp_lon[l] <= (mslp_lon[l+1] + radius)) and (mslp_lon[l] >= mslp_lon[l+1])) or ((mslp_lon[l] >= (mslp_lon[l-1] - radius)) and (mslp_lon[l] <= mslp_lon[l+1])):
              tc_id[l]=1

  return tc_id

#---------------------------------------------------------------------------------------------------------------------------------------

def assign_filter():

"Goal: Grouping events
"a) Each point is then assigned a character string - ‘New’, ‘Same’ or ‘-’ based on different criteria - this is necessary for further filtering and numbering of events.
"b) Loops through all timesteps and assigns these characters based on the following criteria:
"  i) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘0’, this indicates the start of a new event, and the timestep is assigned the string ‘New’.
"  ii) If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘1’, this indicates the continuation of an event, and the timestep is assigned the string ‘Same’.
"  iii) If the current timestep (it) has a tracking ID of ‘0’, it is not associated with a TC event and is assigned the string ‘-’.

  for l in range(0,nl):

    if(tc_id[l] == 1) and (tc_id[l-1] == 0):tc_event[l]='New'
    elif(tc_id[l] == 1) and (tc_id[l-1] == 1):tc_event[l]='Same'
    elif(tc_id[l] == 0):tc_event[l]='-'
  
  return tc_event

#---------------------------------------------------------------------------------------------------------------------------------------

def time_threshold():

"Goal: Applying minimum lifetime criterion
"This step eliminates events that do not last for 2 days.
"a) First, we loop through all timesteps.
"  i) If the current timestep (it) has been assigned the string ‘New’, we consider the following 7 timesteps (it+1, it+2,....it+7).
"  ii) If any of the following 7 timesteps contain a ‘-’ character, this indicates that the event has not spanned 2 days (8 timesteps) and the character string of the current timestep (it) is changed from ‘New’ to ‘-’.
"b) Next, we loop through all timesteps a second time.
"  i) If the current timestep (it) has been assigned the string ‘Same’ and the previous timestep (it-1) has been assigned the ‘-’ string, the current timestep (it) is changed from ‘Same’ to ‘-’. 
"  i) Such cases will only arise from the previous step, in which ‘New’ has been changed to ‘-’ since the event did not meet the minimum lifetime criteria.

  for l in range(0,(nl-7)):

    if(tc_event[l] == 'New'):
      if((tc_event[l+1] == '-') or (tc_event[l+2] == '-') or (tc_event[l+3] == '-') or (tc_event[l+4] == '-') or (tc_event[l+5] == '-') or (tc_event[l+6] == '-') or (tc_event[l+7] == '-')):
        tc_event[l]='-'

  for l in range(0,nl):

    if((tc_event[l] == 'Same') and (tc_event[l-1] == '-')): tc_event[l]="-"

  return tc_event

#---------------------------------------------------------------------------------------------------------------------------------------

def number_events():

"Goal: Numbering events
"This is the final step which numbers all events.
"a) First, we set the event_tracker to 0.
"b) Next, we loop through all timesteps.
"  i) If the current timestep (it) has the character string ‘New’, the event tracker is updated (event_tracker = event_tracker+1), and this new value then becomes the event number (event_number=event_tracker).
"  ii) If the current timestep (it) does not have the character string ‘New’, the timestep is assigned an event number of 999.
"c) We then loop through all timesteps for a second time.
"  i) If the current timestep (it) has the character string ‘Same’, the event number is equal to the event number of the previous timestep (it-1). i.e. event_number(it) = event_number(it-1)

  event_number=0
  for l in range(0,nl):

    if (tc_event[l] == 'New'):
      event_number=event_number+1
      tc_number[l]=event_number
    else:
      tc_number[l]=999.

  for l in range(0,nl):

    if (tc_event[l] == 'Same'):
      tc_number[l]=tc_number[l-1]

  return tc_number

##############################
###----Main Executables----###
##############################

wspd_threshold = ws_thresh()
for l in range(0,nl):
  calc_mslp(l)
  calc_windregion(l)
  calc_maxwind(l)
  calc_vort(l)
  calc_warm_core(l)
  if(max_wspd[l] >= wspd_threshold):
    if(vort_min[l] <= -0.000035):
     if(wc_temp[l] >= (avg_temp_500_250[l] + 1)):
      if(avg_wspd_250[l] < avg_wspd_850[l]): 
        tc_id[l]=1
      else:
        tc_id[l]=0

tstep_fail_allowance()
assign_filter()
time_threshold()
number_events()

#Write output to text file
f = open("MODEL_output.txt","w")
for l in range(0,nl):
  if (tc_number[l] != 999):
    f.write("%s %7.2f %5.2f %5.2f %5.2f %.3e %4.2f %4.2f\n" % (date[l], mslp[l], mslp_lon[l], mslp_lat[l], max_wspd[l], vort_min[l], wc_temp[l], tc_event[l], tc_number[l]))
f.close()
