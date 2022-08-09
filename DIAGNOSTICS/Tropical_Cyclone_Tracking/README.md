# Tropical Cyclone Tracking Algorithm
Paige Donkin<sup>**</sup>***

Babatunde Abiodun, Thomas Webb, Ellen Dyer

<sup>*</sup> University of Cape Town
 
ldnkpai001@myuct.ac.za

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**



# Introduction: Why is this feature/process important?
This diagnostic identifies and tracks tropical cyclones (TCs) over the South West Indian Ocean (SWIO). TCs in the SWIO strike developing nations with fragile infrastructures and agriculture dominated economies. As a result, these countries often suffer massive environmental, economic and sanitary impacts (Leroux et al., 2018). This overwhelming potential for damage and loss of life makes future projections of TC activity, as well as our current ability to model these systems, an important research question in modelling the African region. Compounding this is the fact that relatively little work has been done on TCs in the SWIO (Reason and Keibel, 2004), despite having tropical system activity comparable to that of the North Atlantic Ocean. Improving our understanding of how TCs are modelled in the SWIO region will contribute to lowering projection uncertainty (Zarzycki and Jablonowski, 2014).

# Diagnostic Overview: what does the diagnostic do?
This is a detailed diagnostic which aims to identify and track TCs. The tracking domain covers the South Indian Ocean (0°-40°S,30°E-120°E). The tracking algorithm requires that 6-hourly instantaneous (6hrPlevPt) data is used for all variables other than sea level pressure, for which 6-hourly averaged (6hrPlev) data is used.
The algorithm used to identify and track TCs in this study was informed by the works of Camargo & Zebiak (2002), Maoyi et al., (2018), Murakami et al., (2012), Vitart et al., (1997), and Zhao et al., (2009). The algorithm makes use of resolution-dependent wind speed thresholds as outlined by Walsh et al. (2007).
At each time iteration, the code searches for a system that meets the criteria of a TC. In total, there are 4 criteria that must be met, these are outlined below.

**Starting point - Identifying the minimum sea level pressure (MSLP) – centre of the storm**
* The minimum sea level pressure (MSLP) is identified. This is defined as the centre of the storm.
 
**Criterion 1 – Surface Wind Speed**
* The maximum value of the surface wind speed within 5° of the MSLP is obtained.
* This is then compared to a resolution-dependent threshold value, if the maximum surface wind speed exceeds this threshold value, the criterion is met.

![unnamed](https://user-images.githubusercontent.com/64270734/183715954-86817246-1eba-4bfa-b47a-71c06137c290.png)

*Figure. Variation of threshold detection with resolution (Walsh et al., 2007)*

**Criterion 2 – Vertical Wind Shear**
* The mean wind speed at the levels 850 hPa and 250 hPa is calculated over a 6° X 6° block centred at the MSLP.
* To meet the criterion, the mean wind speed at 850 hPa > mean wind speed at 250 hPa.
 
**Criterion 3 – Warm Core**
* The maximum value of the 500-250 hPa integrated temperature within 2° of the MSLP is obtained. This is defined as the centre of the warm core.
* The mean value of the 500-250 hPa integrated temperature over a 10° X 10° block centred at the MSLP (this is within 5° of the MSLP) is obtained.
* To meet the warm core criterion, this maximum value >= mean value + 1
 
**Criterion 4 – Vorticity**
* The minimum value of relative vorticity within 4° of the MSLP is obtained
* To meet the criterion, the minimum vorticity <= -3.5E-5.

The results are then filtered to detect & number storms.

# Step-by-step method: how is it calculated? 	
Step 1: Find the minimum sea level pressure (MSLP). 
* If it is the first time iteration, or if the previous time iteration did not satisfy the TC criteria, this must be the minimum over the whole domain.
* However, if the previous time iteration did satisfy the TC criteria, this minimum must be within 4° of the location of the previous minimum.
 
Step 2: Find the maximum surface wind speed within 5° of the MSLP location.
 
Step 3: Calculate the mean wind speed at 850 hPa within a 6° X 6° block centred at the MSLP (3° radius).
 
Step 4: Calculate the mean wind speed at 250 hPa within a 6° X 6° block centred at the MSLP (3° radius).
 
Step 5: Calculate the average integrated temperature from 500 hPa – 250 hPa.
 
Step 6: Find the maximum of this average integrated temperature within 2° of the MSLP.
 
Step 7: Calculate the mean of this average integrated temperature over a 10° X 10° block centred at the MSLP (5° radius).
 
Step 8: Calculate the relative vorticity over the domain.
 
Step 9: Find the minimum relative vorticity within 4° of the MSLP.
 
Step 10: Determine if the values calculated in steps 1-9 meet the criteria of a TC.
* Maximum surface wind speed (step 2) >= wind speed threshold value (resolution dependent)
* Mean wind speed at 850 hPa (step 3) > Mean wind speed at 250 hPa (step 4)
* Warm core temp (step 6) >= Local mean temp (step 7) + 1
* Minimum relative vorticity <= -3.5E-5
 
Each timestep is then assigned a tracking ID.
If the timestep meets the criteria of a TC, it is assigned a 1.
If it does not meet the criteria, it is assigned a 0.

**All of the above values must be stored as they will be used to group & number events in the next step.**

Step 11: Filter results to identify & number events.
*Step 11.1: Allowing for a single timestep failure*
* Loops through all points and identifies points with a tracking ID of 0, but where the previous **and**following timesteps have a tracking ID of 1.
* If a point meets this criterion, the latitude and longitude of this point is then assessed to determine if it is within 4.5 degrees of the latitude and longitude of both the previous **and** following timesteps.
* If this point meets the above criterion, the tracking ID is changed from a 0 to a 1.
This step is necessary to reduce broken tracks associated with the weakening of the system during intermittent 6-hourly intervals. 

*Step 11.2: Grouping events*
* Each point is then assigned a character string - ‘New’, ‘Same’ or ‘-’ based on different criteria - this is necessary for further filtering and numbering of events.
* Loops through all timesteps and assigns these characters based on the following criteria:
	* If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘0’, this indicates the start of a new event, and the timestep is assigned the string ‘New’.
	* If the current timestep (it) has a tracking ID of ‘1’, and the previous timestep (it-1) has a tracking ID of ‘1’, this indicates the continuation of an event, and the timestep is assigned the string ‘Same’.
	* If the current timestep (it) has a tracking ID of ‘0’, it is not associated with a TC event and is assigned the string ‘-’.

*Step 11.3: Applying minimum lifetime criterion*
* This step eliminates events that do not last for 2 days.
* First, we loop through all timesteps. 
	* If the current timestep (it) has been assigned the string ‘New’, we consider the following **7** timesteps (it+1, it+2,….it+7).
	* If any of the following **7** timesteps contain a ‘-’ character, this indicates that the event has not spanned 2 days (8 timesteps) and the character string of the current timestep (it) is changed from ‘New’ to ‘-’.
* Next, we loop through all timesteps a second time.
	* If the current timestep (it) has been assigned the string ‘Same’ and the previous timestep (it-1) has been assigned the ‘-’ string, the current timestep (it) is changed from ‘Same’ to ‘-’. Such cases will **only** arise from the previous step, in which ‘New’ has been changed to ‘-’ since the event did not meet the minimum lifetime criteria.

*Step 11.4: Numbering events*
* This is the final step which numbers all events.
* First, we set the event_tracker to 0.
* Next, we loop through all timesteps.
	* If the current timestep (it) has the character string ‘New’, the event tracker is updated (event_tracker = event_tracker+1), and this new value then becomes the event number (event_number=event_tracker).
	* If the current timestep (it) does **not** have the character string ‘New’, the timestep is assigned an event number of 999.
* We then loop through all timesteps for a second time.
	* If the current timestep (it) has the character string ‘Same’, the event number is equal to the event number of the previous timestep (it-1). i.e. event_number(it) = event_number(it-1)

Step 12: All timesteps which do not have an event number of ‘999’ are written to a txt file.

# Diagnostic Summary: what is output?
Output is a text file with the following values given for each time iteration:
* MSLP
* Longitude (of the MSLP)
* Latitude (of the MSLP)
* Maximum surface wind speed
* Character string (‘New’, ‘Same’, ‘-’) - necessary for genesis plots
* Event number



<img src="https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/aa26b2305c1543accafadd3617bec760f438d265/DIAGNOSTICS/Tropical_Cyclone_Tracking/plots/CNRM-CM6-1-HR_tra_plot.png">

*Figure. Genesis locations of tropical systems in the SWIO from 1990-1991 in CNRM-CM6-1-HR. The panels on the left show 
the spatial distribution of genesis locations and the spatial distribution of the tracks, 
with the colour of the dot corresponding to the maximum lifetime intensity of the system. 
The panels on the right show a Kernel Density Estimation (KDE) of these genesis locations and 
tracks, with the spatial correlation with respect to observations (RSMC) given in the bottom right.* 


# Acknowledgements
The tracking algorithm was developed by Paige Donkin.

Supervisor: Babatunde Abiodun

Conversion to Python Libraries: Thomas Webb, Ellen Dyer

The criteria included in this tracking algorithm were informed by the works of Camargo & Zebiak, 2002; Maoyi et al., 2018; Murakami et al., 2012; Vitart et al., 1997; Walsh et al., 2007; Zhao et al., 2009.
The diagnostic was developed and run using the UK’s JASMIN super-data-cluster. The reanalysis and CMIP 6 AMIP models were accessed courtesy of CEDA, and we acknowledge the data providers. 

# References
Camargo, S. J., & Zebiak, S. E. (2002). Improving the detection and tracking of tropical cyclones in atmospheric general circulation models. Weather and Forecasting, 17(6), 1152–1162. https://doi.org/10.1175/1520-0434(2002)017<1152:ITDATO>2.0.CO;2

Horn, M., Walsh, K., Zhao, M., Camargo, S. J., Scoccimarro, E., Murakami, H., Wang, H., Ballinger, A., Kumar, A., Shaevitz, D. A., Jonas, J. A., & Oouchi, K. (2014). Tracking scheme dependence of simulated tropical cyclone response to idealized climate simulations. Journal of Climate, 27(24), 9197–9213. https://doi.org/10.1175/JCLI-D-14-00200.1

Maoyi, M. L., Abiodun, B. J., Prusa, J. M., & Veitch, J. J. (2018). Simulating the characteristics of tropical cyclones over the South West Indian Ocean using a Stretched-Grid Global Climate Model. Climate Dynamics, 50(5–6), 1581–1596. https://doi.org/10.1007/s00382-017-3706-x

Moon, Y., Kim, D., Camargo, S. J., Wing, A. A., Sobel, A. H., Murakami, H., Reed, K. A., Scoccimarro, E., Vecchi, G. A., Wehner, M. F., Zarzycki, C. M., & Zhao, M. (2020). Azimuthally Averaged Wind and Thermodynamic Structures of Tropical Cyclones in Global Climate Models and Their Sensitivity to Horizontal Resolution. Journal of Climate, 33(4), 1575–1595. https://doi.org/10.1175/jcli-d-19-0172.1

Murakami, H., Wang, Y., Yoshimura, H., Mizuta, R., Sugi, M., Shindo, E., Adachi, Y., Yukimoto, S., Hosaka, M., Kusunoki, S., Ose, T., & Kitoh, A. (2012). Future changes in tropical cyclone activity projected by the new high-resolution MRI-AGCM. Journal of Climate, 25(9), 3237–3260. https://doi.org/10.1175/JCLI-D-11-00415.1

Vitart, F., Anderson, J. L., & Stern, W. F. (1997). Simulation of interannual variability of tropical storm frequency in an ensemble of GCM integrations. Journal of Climate, 10(4), 745–760. https://doi.org/10.1175/1520-0442(1997)010<0745:SOIVOT>2.0.CO;2

Walsh, K. J. E., Fiorino, M., Landsea, C. W., & McInnes, K. L. (2007). Objectively determined resolution-dependent threshold criteria for the detection of tropical cyclones in climate models and reanalyses. Journal of Climate, 20(10), 2307–2314. https://doi.org/10.1175/JCLI4074.1

Zarzycki, C. M., & Jablonowski, C. (2014). A multidecadal simulation of Atlantic tropical cyclones using a variable-resolution global atmospheric general circulation model. Journal of Advances in Modeling Earth Systems, 6, 1065–1094. https://doi.org/10.1002/2014MS000363.Received

Zhao, M., Held, I. M., Lin, S. J., & Vecchi, G. A. (2009). Simulations of global hurricane climatology, interannual variability, and response to global warming using a 50-km resolution GCM. Journal of Climate, 22(24), 6653–6678. https://doi.org/10.1175/2009JCLI3049.1
