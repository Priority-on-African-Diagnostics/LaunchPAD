# West African Heat Band
Thompson Annor<sup>**</sup>***

Thomas Webb, Ellen Dyer, Rachel James and Richard Washington

<sup>*</sup> Kwame Nkrumah University of Science and Technology
 
tommykak@yahoo.com 
OR
tannor.cos@knust.edu.gh

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**


# Introduction: Why is this feature/process important?
The Heat Band (TB) is an area located over the western region of African both over ocean and land where near surface air temperature is higher than the surroundings. The TB is highly influenced by moisture and heat exchanges between the ocean in the south and the land in the north of the West African region (Biasutti, 2019). The TB has linkages with the West African Heat Low and the Rain Band which forms part of the West African monsoon system. Hence, it is important to track this feature/process in climate models.

# Diagnostic Overview: what does the diagnostic do?
The TB version 1.0 first determines the Monthly Mean Temperature (MMT) from near surface temperature data. Then, the TB is defined as the grid points with the highest 50% values of MMT which reliably demarcates areas with higher temperature than the surroundings. The domain covers longitudes 25°W, 30°E  and latitudes 10°S, 40°N. The temporal resolution of the data can be daily or monthly mean.
The diagnostic output is a map of the heat band for each month.

# Step-by-step method: how is it calculated?     
Step 1: The MMT is calculated as the monthly mean temperature from sub-monthly temperature fields.

Step 2: A cumulative probability distribution function of the MMT is computed on all grid points of the domain.

Step 3: The TB is defined as the area where the MMT exceeds a threshold defined as 50% of the MMT cumulative probability distribution function (i.e. the highest 50% values of MMT).

Step 4: Then the TB calculated in the above steps is then plotted for each month for the climatological period in deg. C.

# Diagnostic Summary: what is output?
This figure shows the climatological migration and the intensification of the TB over the West African region on  a monthly time scale for the annual cycle for ERA-Interim. It migrates from southern part of the region with a low intensity in January, with an increase in intensity, it moves to the northern part of the region (where the maximum intensity is observed over the Sahelian region) in the month of July. It then transverses from this location with a reduction in intensity from month to month until it reaches the southern part of the region in December.

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/png/ERA-Interim_WAHB__WAHB_plot.png)

# Acknowledgements
The figure for this diagnostic is developed by Thompson Annor. With help from Thomas Webb, Ellen Dyer and Rachel James the code for the diagnostic is developed into the LaunchPAD framework on this GitHub repository. Credit also goes to Richard Washington, who played a role as a supervisor. Finally, acknowledgement is also given to the providers of the observational and CMIP6 datasets.  

# References
Biasutti, M. (2019). Rainfall trends in the African Sahel: Characteristics, processes, and causes. WIREs Clim Change. 2019;10:e591. https://doi.org/10.1002/wcc.591
