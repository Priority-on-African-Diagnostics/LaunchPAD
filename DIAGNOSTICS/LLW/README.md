# Low-Level Westerlies (LLWs): Strength and Drivers

**Thierry Taguela<sup>*</sup>**

Wilfried POKAM

<sup>*</sup> Department of Physics, University of Yaounde I, Cameroon
 
thierrytaguela@gmail.com  

*This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.*



# Introduction: Why is this feature/process important?
Low-Level Westerlies (LLWs), known as recurvature of low-level southeasterlies into south-westerlies in the South Atlantic (Creese and Washington 2018), were identified as a key feature playing a crucial role for the Central Africa regional climate (Nicholson and Grist 2003; Pokam et al. 2014). By advecting moisture from the Atlantic ocean to the Central Africa region,  their strength is related to rainfall variability in the region where wet years exhibit a distinct westerly jet during both wet seasons (Dezfuli and Nicholson 2013; Nicholson and Dezfuli 2013). In the literature, different processes are suggested as drivers of LLWs. While Nicholson and Grist (2003) suggested that the formation of equatorial westerlies is associated with the sea surface pressure associated with the South Atlantic High (SAH), Pokam et al. (2014) suggest that when they recurve into south-westerlies, their strength is driven by the land-sea thermal contrast near the equator. It was also shown that the strength of the Congo Basin Walker circulation modulates the strength of LLWs (Cook and Vizy 2016; Neupane 2016). Therefore, the ability of climate models to well simulate the strength and drivers of LLWs is important for the study of Central Africa regional climate. 

# Diagnostic Overview: what does the diagnostic do?
 The region of interest (Central Africa) is located between 10°S-10°N and 10°E-30°E. The average amount of moisture inflow through the western boundary (10°S-10°N and 10-12.5°E) represents the strength of the LLWs in this diagnostic. 

Figure 1. shows how well the simulated strength of LLWs in CMIP6 models is related to the Ocean-Land temperature gradient and to the strength of Congo Basin Walker circulation. The Ocean-Land temperature gradient is calculated at 925hPa with Ocean temperature averaged between 5S-3N and 2W-8E while the continent temperature is averaged between 5S-3N and 15E-25E. 850hPa vertical wind average between 5S-3N and 2W-8E represents the strength of the Congo Basin Walker circulation.   

Figure 2. shows how the simulated strength of LLWs in CMIP6 models is related to the Mean South Atlantic High (SAH). SAH is calculated with sea level pressure average between 15S-40S and 40W-10E.
Both CMIP6 models and reanalysis data are at monthly time scale resolution covering the period 1980 to 2010 for the September-November season.

# Step-by-step method: how is it calculated? 	
### A) Calculate moisture flux across the coast

1. Load monthly u wind and q data
If need to reduce data size, could restrict it at this step:
		* Select the central Africa domain (-10°W to 40°E longitude and -25°S to 25°N latitude)
		* Select a time period (here 1980-2010), 925 hPa pressure level, and the September - November season
2. Sub-select coastal domain (10S-10N, 10E-12.5E)
3. Compute the moisture flux (q*u)
4. Average long term seasonal mean
5. Average over the spatial domain


### B) Calculate vertical velocity over the Gulf of Guinea

1. Load monthly vertical velocity data and select 850hPa pressure level, a time period (here 1980-2010), September - November season and the area covering 5S-3N and 2W-8E
2. Compute time average (long term seasonal mean) and area average

### C) Calculate temperature difference between eastern Atlantic and Central Africa

1. Load monthly temperature data and select 925hPa pressure level,  a time period (here 1980-2010) and the September - November season
2. Select Eastern Atlantic Ocean ( between 5S-3N and 2W-8E) and calculate area average
3. Select Central Africa landmass  ( between 5S-3N and 15E-25E) and calculate area average
4. Calculate long term seasonal mean
5. Compute the temperature difference between the Eastern Atlantic Ocean and Central Africa landmass.

### D) Calculate the strength of South Atlantic High (SAH)

1. Load monthly sea level pressure data and select a time period (here 1980-2010) and the September - November season
2. Select 15S-40S and 40W-10E and area average 
3. Calculate long term seasonal mean

### First Figure

Part a: moisture flux bar chart

	Plotting A (moisture flux) for each dataset

Part b: scatter plot vertical velocity and temperature difference

	Plotting B (vertical velocity) against C (temperature difference) for each dataset (scatter)

### Second Figure: Moisture flux and South Atlantic High 
	 	 	
Plot bar chart of A (moisture flux) on y-axis and D (SAH) on the z-axis


# Diagnostic Summary: what is output?

Figure 1: a) September-November 925hPa zonal moisture inflow at the western boundary (10S-10N and 10-12.5E) of Central Africa region representing the strength of Low-Level Westerlies (LLWs). b) Scatter plot representing the September-November 850hPa vertical wind average between 5S-3N and 2W-8E over the Gulf of Guinea and the 925hPa temperature gradient between Eastern Atlantic Ocean (average between 5S-3N and 2W-8E) and the continent (average between 5S-3N and 15E-25E).




Figure 2: (blue bars) September-November 925hPa zonal moisture inflow at the western boundary (10S-10N and 10-12.5E) of Central Africa region representing the strength of Low-Level Westerlies (LLWs) and (red bars) Mean South Atlantic High (SAH): sea-level pressure average between 15S-40S and 40W-10E

# Acknowledgements
This work uses the CMIP6 models and ERA5, ERAINT and MERRA2 reanalysis data. We thank all groups providing these data. The code used in this work to plot the figures was first written in NCL by Thierry Taguela and we thank Thomas Webb and Ellen Dyer for their help in translating the code in PYTHON. The helpful input of  Wilfried Pokam, Rachel James and Richard Washington in leading this work was also really appreciated.

 
# References
Creese A, Washington R (2018) A process-based assessment of CMIP5 rainfall in the Congo Basin: the September–November rainy season. J Clim 31(18):7417–7439. https://doi.org/10.1175/JCLI-D-17-0818.1 
 
Cook KH, Vizy EK (2016) The Congo Basin Walker circulation: dynamics and connections to precipitation. Clim Dyn 47(3):697–717. https://doi.org/10.1007/s00382-015-2864-y
 
Dezfuli, A. and S. E. Nicholson, 2013: The relationship of rainfall variability in western equatorial Africa to the tropical oceans and atmospheric circulation. Part II: The boreal autumn. J. Climate, 26, 66–84, https://doi.org/10.1175/JCLI-D-11-00686.1.
 
Neupane N (2016) The Congo Basin zonal overturning circulation. Adv Atmos Sci 33(6):767–782. https://doi.org/10.1007/s00376-015-5190-8
 
Nicholson SE, Grist JP (2003) The seasonal evolution of the atmospheric circulation over West Africa and equatorial Africa. J Clim 16(7):1013–1030. https :doi.org/10.1175/15200442(2003)016<1013:TSEOTA>2.0.CO;2
 
Nicholson S.E. and A. K. Dezfuli, 2013: The relationship of rainfall variability in western equatorial Africa to the tropical oceans and atmospheric circulation. Part I: The boreal spring. J. Climate, 26, 45–65, https://doi.org/10.1175/JCLI-D-11-00653.1.
 
Pokam, W. M., C. L. Bain, R. S. Chadwick, R. Graham, D. J. Sonwa, and F. M. Kamga, 2014: Identification of processes driving low-level westerlies in west equatorial Africa. J. Climate, 27, 4245-4262, https://doi.org/10.1175/JCLI-D-13-00490.1.
