# Central African Easterlies
Ellen Dyer<sup>**</sup>***

Thomas Webb

<sup>*</sup> University of Oxford
 
ellen.dyer@ouce.ox.ac.uk 

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**


# Introduction
Rainfall in the long rains (March April May, MAM) season in Kenya has large biases in coupled historical CMIP simulations. A set of atmospheric diagnostics was created, using the ERA-Interim reanalysis and CHIRPSv2 rainfall, for the long rains (MAM) season in Kenya (Dyer and Washington, submitted 2020). This set of diagnostics was created using daily fields in the baseline and wet and dry extreme climatologies as the changing sub-seasonal drivers of rainfall were of interest. Local diagnostics such as mid-tropospheric moisture, moisture-flux convergence, and vertical velocity were found to be good indicators of rainfall in the wettest part of the season and during onset. However, a regional diagnostic which is well correlated with rainfall and is spatially correlated with moisture-flux convergence over Kenya is the strength of easterly zonal winds at 700 hPa over Central Africa (CAF). Stronger easterly winds are indicative of less rain over Kenya, and was shown to be a particularly good diagnostic during March and April. 
Diagnostic Overview
An anomaly plot is made for 700 hPa zonal winds to show the degree and regional extent of the easterly wind anomalies. This bias plot is created relative to ERA5 reanalysis zonal winds. A bias metric is also calculated using an area averaged anomaly over Central Africa, and rainfall over Kenya. The correlation between CAF winds and Kenyan rainfall were explored in a sub-seasonal analysis of Kenyan long-rains dynamics (Dyer and Washington, submitted 2020) and adjusted here for ERA5 and CMIP6. We compare this bias metric over the model ensemble as it is a measure of moisture export from Kenya, along with being well correlated with moisture-flux convergence, and rainfall in Kenya. This diagnostic has only been tested during the MAM season and is correlated with rainfall during March and April.

Monthly data is used, and an initial regional selection of (15S-10N, 0-45E) is made followed by sub-setting to (8S-2N, 15-34E) for a numeric metric which can then be compared to other models. 

# Step-by-step method

Step 1: Load model and reanalysis zonal winds over domain (15S-10N, 0-45E) and select 700 hPa level

Step 2: Loop over each month in MAM and calculate a time series mean. The remaining steps will all be done for each month in MAM.

Step 3: Regrid models to the ERA5 reanalysis grid and calculate model 700 hPa zonal wind anomaly from the reanalysis

Step 4: Select smaller region (8S-2N, 15-34E) from anomaly calculated in Step 3 and calculate an area mean for a CAF wind bias metric

Step 5: Select rainfall in the region (4S-4N, 33-42E) for a Kenyan rainfall bias metric

Step 6: Plot anomaly winds calculated in Step 3 for each model including an outline of the region used to calculate the bias metric in Step 4, and an outline of the region used to calculate the rainfall bias metric in Step 5.

Step 7: Calculate the Spearman correlation between model rainfall metric (Step 5) and model zonal wind bias metric (Step 4) using all available models in the ensemble. If the correlation between model rainfall and zonal wind is significant (p-value < 0.01) then output a scatter plot of the CAF 700 hPa zonal wind metric, vs Kenyan rainfall including all available models in the ensemble. 

# Diagnostic Summary

The diagnostics output are (1) a map of wind biases, and (2) a scatter plot of zonal winds over Central Africa and Kenyan rainfall.



Figure 1. HadGEM3-GC31-MM 700hPa easterly wind bias over Central Africa relative to ERA5 (m/s) for April. We have shown that an easterly wind bias (purple) is usually associated with a dry bias in Kenyan rainfall over the same period. Yellow outline shows the region used to calculate Central African winds, and blue outline shows the region used to calculate Kenyan rainfall (in Figure 2). 


Figure 2. CAF zonal wind metric (m/s) vs Kenyan rainfall metric (mm/day) for April in CMIP6. In this month there is a relationship between how strong easterly CAF winds are and how dry Kenyan rainfall is in models. April is also the month where most CMIP6 models have a dry bias in Kenyan rainfall.

# Acknowledgements
This work uses the CMIP6 ensemble, accessed using CEDA, and ERA5, ERA-Interim and MERRA2 reanalysis data. This diagnostic was created by Dr Ellen Dyer (ellen.dyer@ouce.ox.ac.uk) and integrated into AutoAssess by Dr Tom Webb (thomas.webb@ouce.ox.ac.uk). 

# References
Submitted and in review: Dyer, E., Washington, R. Kenyan long rains: a sub-seasonal approach to process-based diagnostics.
