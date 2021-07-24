# -*- coding: utf-8 -*-
###############################
from config import * #note relative paths from execution 
from find_files import * #remove config. here and above for mass
import os
import iris
import iris.coords
from iris.experimental.equalise_cubes import equalise_attributes
from iris.util import unify_time_units
import iris.coord_categorisation

def lon_bounds(lon1, lon2):

     if lon1 < lon2:
         Clon_0 = iris.Constraint(longitude=lambda cell: lon1 <= cell <= lon2)
     else:
         Clon_0 = iris.Constraint(longitude=lambda cell: lon1 <= cell <= lonC1 or lonC2 <= cell <= lon2)

     return Clon_0

def lat_bounds(lat1, lat2):

     Clat_0 = iris.Constraint(latitude=lambda cell: lat1 <= cell <= lat2)

     return Clat_0

def year_bounds(year1, year2):

     Ctim_0 = iris.Constraint(time=lambda cell: year1 <= cell.point.year <= year2)

     return Ctim_0

def spatial_collapse(cube):
     for coord in cube.coords():
         if coord.var_name=='lat' and len(coord.points)>1:
             cube = cube.collapsed('latitude', iris.analysis.MEAN)
         elif coord.var_name=='lon' and len(coord.points)>1:
             cube = cube.collapsed('longitude', iris.analysis.MEAN)
         elif coord.var_name=='latitude' and len(coord.points)>1:
             cube = cube.collapsed('latitude', iris.analysis.MEAN)
         elif coord.var_name=='longitude' and len(coord.points)>1:
             cube = cube.collapsed('longitude', iris.analysis.MEAN)

     return cube

def create_greenlist(vari_list):
    red_list=[]

    for mod in mod_list:
        for vari in vari_list:
            if not os.path.exists(level1_mon(mod,vari)):
                print(level1_mon(mod,vari))
                print('cannot find files for '+mod)
                red_list.append(mod)

    green_list = [x for x in mod_list if x not in red_list]

    return green_list

def create_greenlist6hr(vari_list):
    red_list=[]

    for mod in mod_list:
        for vari in vari_list:
            if not os.path.exists(level1_mon(mod,vari)):
                print(level1_mon(mod,vari))
                print('cannot find files for '+mod)
                red_list.append(mod)

    green_list = [x for x in mod_list if x not in red_list]

    return green_list


def time_bound_six(name):

    Ctim_1 = iris.Constraint(time=lambda cell: cell.point.hour == 6)

    return Ctim_1

def create_greenlist6hr(vari_list):
    red_list=[]

    for mod in mod_list:
        for vari in vari_list:
            if not os.path.exists(level1_6hr(mod,vari)):
                print('cannot find files for '+mod)
                red_list.append(mod)

    green_list = [x for x in mod_list if x not in red_list]

    return green_list

def pressure_min_mass_collapse(name, cube):

     if name=='ERA-Interim' or name =='ERA5' or name =='ERA-Interim':

         cube = cube.collapsed('pressure_level', iris.analysis.MIN)

     if name=='MERRA2':
         cube = cube.collapsed('air_pressure', iris.analysis.MIN)

     else:

         cube = cube.collapsed('pressure', iris.analysis.MIN)

     return cube

def pressure_min_collapse(name, cube):

     if name=='ERA-Interim' or name =='ERA5' or name =='ERA-Interim':

         cube = cube.collapsed('pressure_level', iris.analysis.MIN)

     else:

         cube = cube.collapsed('air_pressure', iris.analysis.MIN)

     return cube

def select_son(cube):

     iris.coord_categorisation.add_month_number(cube, 'time', name='month_number')

     cube = cube.extract(iris.Constraint(month_number=9) and iris.Constraint(month_number=10) and iris.Constraint(month_number=11))

     return cube

def season_all(cube):

     iris.coord_categorisation.add_season(cube, 'time', name='clim_season')
     cube = cube.aggregated_by(['clim_season'],iris.analysis.MEAN)

     return cube

def month_all(cube):

     iris.coord_categorisation.add_month(cube, 'time', name='month')
     cube = cube.aggregated_by(['month'],iris.analysis.MEAN)

     return cube

def season_all_ts(cube):
     #print(cube)

     iris.coord_categorisation.add_season(cube, 'time', name='clim_season')
     iris.coord_categorisation.add_season_year(cube, 'time', name='season_year')
    # print(cube)

     return cube

def pressure_bounds(name, pressure1, pressure2):

     if name=='ERA-Interim' or name =='ERA5' or name =='ERA-Interim':

         Caip_0 = iris.Constraint(pressure_level=lambda cell: pressure1/100 <= cell <= pressure2/100)

     else:

         Caip_0 = iris.Constraint(air_pressure=lambda cell: pressure1 <= cell <= pressure2)

     return Caip_0

def pressure_bounds_mass(name, pressure1, pressure2):

     if name=='ERA-Interim' or name =='ERA5' or name =='ERA-Interim':

         Caip_0 = iris.Constraint(pressure_level=lambda cell: pressure1/100 <= cell <= pressure2/100)

     elif name=='MERRA2':
         Caip_0 = iris.Constraint(air_pressure=lambda cell: pressure1 <= cell <= pressure2)

     else:

         Caip_0 = iris.Constraint(pressure=lambda cell: pressure1 <= cell <= pressure2)

     return Caip_0

def mon_div(expt, cube, div_no, pressure1, pressure2):

     #print(cube)

     #for coord in cube.coords():
       #  print(coord.name)
     Cmon_num_0 = iris.Constraint(mon_num=lambda cell: div_no <= cell <= 12)
     Cmon_num_1 = iris.Constraint(mon_num=lambda cell: 1 <= cell < div_no)

     cube2 = cube.extract(Cmon_num_0 & pressure_level(expt, pressure1))
     cube3 = cube.extract(Cmon_num_1 & pressure_level(expt, pressure2))

     return cube2, cube3

def lon_level(lon1):

     Clon_0 = iris.Constraint(longitude=lon1)

     return Clon_0

def lat_level(lat1):

     Clat_0 = iris.Constraint(latitude=lat1)

     return Clat_0

def year_level(year1):

     Ctim_0 = iris.Constraint(time=year1)

     return Ctim_0

def unit_converter(cube):

     if cube.units == 'C':
         cube.data += 273.15
         cube.units = 'K'

     return cube

def unit_converter_k_to_C(cube):

     if cube.units == 'K':
         cube.data -= 273.15
         cube.units = 'C'

     return cube

def pressure_level(name, pressure1):


     if name =='ERA5' or name =='ERA-Interim':


         Caip_0 = iris.Constraint(pressure_level=pressure1/100)

     else:

         Caip_0 = iris.Constraint(air_pressure=pressure1)

     return Caip_0

def pressure_level_mass(name, pressure1):


     if name =='ERA5' or name =='ERA-Interim':


         Caip_0 = iris.Constraint(pressure_level=pressure1/100)
     elif name=='MERRA2':
         Caip_0 = iris.Constraint(air_pressure=pressure1)

     else:

         Caip_0 = iris.Constraint(pressure=pressure1/100)#required for TJ1 /100

     return Caip_0

def sixhr_file_location(expt, vari):
    CMIP6_extn = '*.nc'
    ERAI_extn = '/nc/'

    if expt=='GPCP':
        location = '/gws/nopw/j04/launchpad/observations/GPCP/precip.mon.mean.nc'
        print(location)

    elif expt =='ERA5' or expt =='MERRA2' or expt =='ERA-Interim':
        location = level1_obs_6hr(expt)+'/'+vari+'/'+CMIP6_extn
        print(location)

    else:
        location = level1_6hr(expt,vari)+CMIP6_extn

    return location

def monthly_file_location(expt, vari):

     CMIP6_extn = '*.nc'
     ERAI_extn = '/nc/'

     if expt=='ERA-Interim':
         if vari=='ta':
             location='/gws/nopw/j04/launchpad/observations/ERA-Interim/mon/ta/nc/erai_monthly_t_1979_2016_0'
         else:
             location = level1_obs_mon(expt)+vari+ERAI_extn+CMIP6_extn

     elif expt=='ERA5':
         location = level1_obs_mon(expt)+'era5_'+vari+CMIP6_extn

     elif expt=='GPCP':
         location = '/gws/nopw/j04/launchpad/observations/GPCP/precip.mon.mean.nc'

     elif expt=='MERRA2':

         location = level1_obs_mon(expt)+vari+'_'+CMIP6_extn

     elif expt=='HadISST':

         location = level1_obs_mon(expt)+'HadISST_'+vari+CMIP6_extn

     else:

         location = level1_mon(expt,vari)+'*'+expt+CMIP6_extn

     return location

def test_file_exists(location):
     if not os.path.exists(location):
         return False

     else:
         return True

def cube_concatenator(CL_0):

     equalise_attributes(CL_0)
     unify_time_units(CL_0)

     CU_0 = CL_0.concatenate_cube()

     CU_0.coord('longitude').circular = True

     return CU_0


def climatology(cube):

    #create a new coordinate for month name
    iris.coord_categorisation.add_month(cube, 'time', name='month')

    #average by month
    mean_cube = cube.aggregated_by('month', iris.analysis.MEAN)

    return mean_cube

def anomaly(cube, coord_str):

    # calculate global time average
    mean_cube = cube.collapsed(coord_str, iris.analysis.MEAN)

    # subtract mean from the actuall
    anom_cube = iris.analysis.maths.subtract(cube, mean_cube)

    return anom_cube

def time_anomaly(cube):

    # get the time anomaly
    # calculate averages over time by 
    # using climatology
    cube_mean = climatology(cube)
    anom_cube = iris.analysis.math.substract(cube, cube_mean)

    return anom_cube

def correlation(cube1, cube2):

    correl_cube = iris.analysis.stats.pearsonr(cube1, cube2, corr_coords=['time'])

    return correl_cube

def divergence(ua_cube, va_cube):

    # compute du/dx    
    dua_cube = iris.analysis.calculus.differentiate(ua_cube, 'longitude')

    # compute dv/dx
    dva_cube = iris.analysis.calculus.differentiate(va_cube, 'longitude')

    # div = -(du + dv)
    div_cube = -1 * (dua_cube + dva_cube)

    return div_cube

def vertical_velocity(ua_cube, va_cube):

    # compute the divergence
    div_cube = divergence(ua_cube, va_cube)

    # compute vertical velocity
    wa_cube = calc.integrate(div_cube, "pressure")


    return wa_cube
