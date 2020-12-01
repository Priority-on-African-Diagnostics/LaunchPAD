# West African Heat Low
Thompson Annor<sup>**</sup>***

Thomas Webb, Ellen Dyer, Rachel James and Richard Washington

<sup>*</sup> Kwame Nkrumah University of Science and Technology
 
tommykak@yahoo.com 
OR
tannor.cos@knust.edu.gh

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**

# Introduction: Why is this feature/process important?
The West African Heat Low (WAHL) is an area located in the western part of the African continent where high temperature and low pressure exist in the lower part of the troposphere. The WAHL is highly influenced by moisture and the temperature of the lower part of the troposphere of the region and therefore, it is determined as the anomaly in the Low Level Atmospheric Thickness (LLAT). The LLAT is simply the geopotential thickness between the 925 and 700 hPa pressure levels. Since the WAHL is highly modulated by the moisture amount and the temperature, it therefore forms a key component of the West African monsoon system (Lavaysse et al, 2009; Lavaysse et al, 2016; Biasutti, 2019). Hence, it is important to track this feature/process in climate models.


# Diagnostic Overview: what does the diagnostic do?
The WAHL version 1.0 first defines the LLAT as the difference in the geopotential height between 925 and 700 hPa pressure levels. Then, the WAHL is defined as the grid points with the highest 10% values of LLAT. This diagnostic has been found to reliably place areas with high surface temperatures and low surface pressure (Lavaysse et al, 2009). The domain covers longitudes 25°W, 30°E  and latitudes 10°S, 40°N. The temporal resolution of the data is daily exclusively taken at 06 hours for the whole year. The 06 hourly dataset is used to ensure that the calculation of WAHL is not affected by heating due to insulation.

The diagnostic output is a map showing the WAHL location and intensity for each month. 

# Step-by-step method: how is it calculated? 	
Step 1: The LLAT is calculated as the difference between geopotential heights at 925 and 700 hPa from 0600 UTC fields.

Step 2: Create monthly means of the LLAT.

Step 3: A cumulative probability distribution function of the LLATs is computed over all grid points of the domain for each month.

Step 4: The WAHL is defined as the area where the LLAT exceeds a threshold defined as 90% of the LLAT cumulative probability distribution function (i.e. the highest 10% values of LLAT).

Step 5: Plot a map of WAHL (all LLAT values in the highest 10% of values). 

# Diagnostic Summary: what is output?
The figure shows the climatological migration and the intensification of the heat low over the West African region on  a monthly time scale for the annual cycle.

This has been plotted for 06:00 hours for the 1983-2012 period.

Using ERA Interim, the WAHL migrates from south-eastern part of the region with a low intensity in January, with an increase in intensity, it moves to the north-western part of the region (the Sahelian region) where the maximum intensity is observed in the month of July. It then transverses from this location with a reduction in intensity from month to month until it reaches the south-eastern part of the region in December.

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/png/WAHL.png)

# Acknowledgements
The figure for this diagnostic was developed by Thompson Annor by adopting the calculation of the heat low in Lavaysse et al, 2009. With help from Thomas Webb, Ellen Dyer and Rachel James the code for the diagnostic was developed from ncl to python and integrated into the LaunchPAD framework in thisGitHub repository. Credit also goes to Richard Washington, who played a role as a supervisor. Finally, acknowledgement is also given to the ECMWF for the provision of the ERA-Interim dataset, and the providers of the other reanalyses and CMIP6 datasets.  

# References
Lavaysse, C, Flamant,C., Janicot ,S., Parker, D. J., Lafore, J.-P., Sultan, B. and Pelon, J. (2009). Seasonal evolution of the West African heat low: a climatological Perspective. Clim Dyn (2009) 33:313–330. DOI 10.1007/s00382-009-0553-4
Lavaysse, C., Flamant, C., Evan, A.,  Janicot, S.and Gaetani, M. (2016). Recent climatological trend of the Saharan heat low and its impact on the West African climate. Clim Dyn (2016) 47:3479–3498. DOI 10.1007/s00382-015-2847-z
Biasutti, M. (2019). Rainfall trends in the African Sahel: Characteristics, processes, and causes. WIREs Clim Change. 2019;10:e591. https://doi.org/10.1002/wcc.591
