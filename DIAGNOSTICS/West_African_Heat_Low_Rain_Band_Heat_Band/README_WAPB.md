# West African Rain Band
Thompson Annor<sup>**</sup>***

Thomas Webb, Ellen Dyer, Rachel James and Richard Washington

<sup>*</sup> Kwame Nkrumah University of Science and Technology
 
tommykak@yahoo.com 
OR
tannor.cos@knust.edu.gh

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**


# Introduction: Why is this feature/process important?
The Rain Band (RB) is an area located over the western region of African both over ocean and land where precipitation amount is higher than the surroundings. The RB is highly influenced by moisture and heat exchanges between the ocean in the south and the land in the north of the West African region (Biasutti, 2019). The RB can be used to portray the north-south movement of the tropical rainbelt, a key component of the West African monsoon system and also has linkages with the West African Heat Low and Heat Band. Hence, it is important to track this feature/process in climate models. 

# Diagnostic Overview: what does the diagnostic do?
The RB version 1.0 first determines the Monthly Total Rainfall Amount (MTRA) from the precipitation output. Then, the RB is defined as the grid points with the highest 50% values of MTRA which reliably demarcates areas with higher rainfall than the surroundings. The domain covers longitudes 25°W, 30°E  and latitudes 10°S, 40°N. The temporal resolution of the input data can be daily or monthly total precipitation. 

The diagnostic output shows a map of the rainband for each month.

# Step-by-step method: how is it calculated?     
Step 1: The MTRA is calculated as the monthly total precipitation from sub-monthly precipitation fields.

Step 2: A cumulative probability distribution function of the MTRA is computed on all grid points of the domain.

Step 3: The RB is defined as the area where the MTRA exceeds a threshold defined as 50% of the MTRA cumulative probability distribution function (i.e. the highest 50% values of MTRA).

Step 4: Then the RB calculated in the above steps is then plotted for each month for the climatological period in mm. 

# Diagnostic Summary: what is output?
This figure shows the climatological migration and the intensification of the Rain Band over the West African region on  a monthly time scale for the annual cycle for the GPCP precipitation dataset for the 1983-2012 period. The RB migrates from its south-most position with low intensity in January, with an increase in intensity, it moves to the north-most position in the month of August and the maximum widths are seen in August and September months. It then transverses from this location with a reduction in intensity from month to month until it reaches the south-most position in December.

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/West_African_Heat_Low_Rain_Band_Heat_Band/png/GPCC_WAPB__WAPB_plot.png)

# Acknowledgements
The figure for this diagnostic is developed by Thompson Annor. With help from Thomas Webb, Ellen Dyer and Rachel James the code for the diagnostic is developed into the LaunchPAD framework. Credit also goes to Richard Washington, who played a role as a supervisor. Finally, acknowledgement is also given to the providers of the GPCP and CMIP6 datasets.  

# References
Biasutti, M. (2019). Rainfall trends in the African Sahel: Characteristics, processes, and causes. WIREs Clim Change. 2019;10:e591. https://doi.org/10.1002/wcc.591
