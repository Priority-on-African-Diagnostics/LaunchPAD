# West African Westerly Jet
AI. MAKINDE<sup>**</sup>***

BJ Abiodun

<sup>*</sup> University of Cape Town
 
mckynde@gmail.com

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**


# Introduction: Why is this feature/process important?

The West African Westerly Jet (WAWJ) is a low-level westerly jet located at 8°–11°N over the eastern Atlantic and the West African coast. The WAWJ has been found to play a crucial role in the West African climate and is well known for transporting moisture from the eastern Atlantic onto the Sahel (subcontinent, especially at 8-11°N). It also modulates the atmosphere–ocean–land surface interactions, thereby playing an important role in the earth coupled system (Liu et al. 2019). The Sahel has been characterized by strong climatic variations and irregular rainfalls, which pose two of the biggest crises, food insecurity and poverty in the region according to the UN Environment Programme (UNEP  2012). There is, therefore, a strong need for monitoring and predicting rainfall changes throughout a large range of spatial and temporal scales, from local weather to continental climate change.
Reliable seasonal predictions and climate projections of rainfall in the Sahel require adequate simulation of WAWJ by Global Climate Models (GCMs). Therefore, representation of WAWJ in GCMs needs to be evaluated to determine how well the models simulate the characteristics of the jet. This diagnostic evaluates how well CMIP6 models simulate or represent West African Westerly Jet.
This document details the WAWJ code as released at version 1.0.

# Diagnostic Overview
This diagnostic emerges from research to find, calculate and visualize the WAWJ, its position, intensity, onset and cessation, correlation with precipitation and classifies possible patterns of the WAWJ. A threshold was defined for locating the WAWJ (zonal wind above 2.0 ms1 when the meridional component is greater zero, i.e. wind is southerly and not northerly) and the continent was masked out for all of the analysis except for the classification by SOMs method. The vertical location and the depth of the WAWJ was first examined with the profile of the WAWJ core (maximum zonal wind that fits the WAWJ threshold) at all pressure levels and was found at 925hPa and has a depth reaching 800hPa. Secondly, the strength of the WAWJ core was examined with a time series (monthly) plot of WAWJ core at 925hPa and was found to have a maximum of about 6ms-1 across all models and reanalysis. A wind vector map overlayed on the zonal wind (filled contours) that fits into the criteria for WAWJ and the zero meridional wind component at 925 hPa was made to show the location and intensity of WAWJ and the westward extent of the Jet. Also, a monthly plot of the WAWJ was made, to show the onset and the cessation of the Jet. Furthermore, possible patterns of the WAWJ were identified and classified and also the frequency contribution of each model was plotted. Finally, the correlation with precipitation over West Africa was calculated and plotted, to show the link and role of WAWJ in precipitation variation over the Sahel and West Africa at large.
We made and compared these diagnostics for reanalysis datasets and twenty six models in the CMIP6 ensemble,

Monthly data of zonal and meridional wind, geopotential height, specific humidity and precipitation from 1980 to 2014 was used to make 35 years climatology for both observation dataset (ERA5) and models in the CMIP6 ensemble.

Here we describe a diagnostic to summarise the location and intensity of the WAWJ as it relates to geopotential height and the location of the Inter-Tropical Convergence Zone (ITCZ): a map is shown for each month illustrating the winds alongside these features.

# Step-by-step method
Step 1: An initial regional selection of (0oN-20oN, 40oW-10oW) was made followed by regriding to 0.5o x 0.5o horizontal resolution for zonal (u) and meridional (v) winds, and geopotential height at 925hPa.

Step 2: Calculate the monthly long term mean (climatology) of the re-gridded datasets from step 1

Step 3: Locate the WAWJ by applying WAWJ thresholds (defined as zonal wind greater than 2.0ms-1 when the meridional is greater or equal to 0ms-1 - i.e. southerly and not notherly) to the zonal wind climatology from step 2.

Step 4: Make two copies of the result from step 3. Create a land mask from the grid.CDF file and use this mask to mask out the continent from the second copy. Name the first copy as wj_clim and the second as wj_mskd_clim.

Step 5: Plot maps with:
- filled contours to show the WAWJ from Step 4 ( the second copy - wj_maskd_clim)
- a line representing the  ITCZ (when meridional wind is 0ms-1) using meridional wind from Step 2
- wind vectors using zonal and meridional winds from Step 2
- contour lines of  geopotential height from step 2.

The maps can be displayed as either:
- For each dataset, one map per month from March to November
- A map for August for each dataset


# Diagnostic Summary
The diagnostic illustrates on a map of West Africa the wind (vectors) the wind which makes up the WAWJ (shading), the location of the ITCZ, and the geopotential height. 

Figure 1 shows spatial plot of the WAWJ climatology from 1980 to 2014 at 925hPa from March to November in the reanalysis(ERA5). The figure shows the onset and cessation of WAWJ and the westward extension as it reaches maximum in August. The jet starts developing in June and gradually intensifies in July and reaches the maximum in August, retreats in September and dissipates in October. It has a maximum westward extension in August reaching about 35oW.

The majority of the models agree with the reanalysis having the jet maximum in August with the jet core at 925hPa. Figure 2 compares the WAWJ across all models with the reanalysis in the month of August at 925hPa. The majority of the models capture the location and the structure of the jet as in the reanalysis. However, most models overestimate the westward extension of the jet and some of the models overestimate the strength of the jet core. However, few of the models underestimate both the jet strength and the westward extension of the jet.

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/West_African_Westerly_Jet/plots/_WAWJ_ERA5_WAWJ_plot.png)

Figure 1: The climatology (1980 – 2014) of WAWJ (flled contours), the ITCZ (red line), the wind (vectors) and the geopotential height (contour lines) at 925-hPa in ERA5 reanalysis.

![](https://lh6.googleusercontent.com/RSDq_pU0-Oqeu36uJuQsBN0GXPuamzJ721Ic-NjEytpCNeEQERw5XLR15bWXgrThf2PhMdxTsblzekSKaPRDd_g4rjdmXqqXhYXqAtuixilLS8qkJHEFMj4RvL4elCNZ5LNFoqwK)

Figure 2: The climatology (1980 – 2014) of WAWJ (filled contours), the ITCZ (red line), the wind (vectors) and the geopotential height (contour lines) at 925-hPa in August for reanalysis (ERA5) and twenty six CMIP6 models.





# Acknowledgements
The figures for this diagnostic and the threshold for locating the WAWJ are based on the understanding of the jet’s dynamics from Pu and Cook, 2010, and were developed by Akintunde I. Makinde and Prof Babatunde J. Abiodun (as supervisor). With help and coordination from Rachel James, Thomas Webb, and Ellen Dyer the code for the diagnostic which was written in Ferret, Fortran and Python was developed into the LaunchPAD framework.
Finally, acknowledgement goes to the  European Centre for Medium-Range Weather Forecasts (ECMWF), Copernicus Data Service (CDS) (Copernicus Climate Change Service 2019) and the World Climate Research Programme (WCRP), which, through its Working Group on Coupled Modelling (WGCM), coordinated and promoted CMIP6 also the Earth System Grid Federation (ESGF) for archiving the data and providing access, and the multiple funding agencies who support CMIP6 and ESGF.



# References
Bing Pu, KERRY H. COOK, (2010). Dynamics of the West African Westerly Jet. Journal of Climate, DOI: 10.1175/2010JCLI3648.1

Bing Pu, KERRY H. COOK, (2011). Role of the West African Westerly Jet in Sahel Rainfall Variations, Journal of Climate, Vol. 25, DOI: 10.1175/JCLI-D-11-00394.1

Liu, W., Cook, K.H. & Vizy, E.K. Role of the West African westerly jet in the seasonal and diurnal cycles of precipitation over West Africa. Clim Dyn 54, 843–861 (2020). https://doi.org/10.1007/s00382-019-05035-1

Pu, B., & Cook, K. H. (2012). Role of the West African westerly jet in Sahel rainfall variations. Journal of Climate, 25(8), 2880-2896.

Semyon A. Grodsky, James A. Carton, and Sumant Nigam (2003). Near surface westerly wind jet in the Atlantic ITCZ, Geophysical Research Letters, vol. 30(19), doi:10.1029/2003GL017867.

Nicholson, S. E. (2009) A revised picture of the structure of the ‘monsoon’ and land ITCZ over West Africa. Climate Dynamics, Vol. 32.

Grist, J. E. & Nicholson, E. (2001). A study of the dynamic factors influencing the rainfall variability in the West African Sahel. Journal of Climate. Vol. 14
