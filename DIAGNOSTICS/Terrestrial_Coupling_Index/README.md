# Terrestrial Coupling Index

**Anthony Mwanthi<sup>*</sup>**

Ellen Dyer, Thomas Webb

<sup>*</sup> Department of Meteorolgy, University of Nairobi, Kenya
 
mmwanthi@gmail.com 
or
anthony.mwanthi@students.uonbi.ac.ke

*This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.*



# Introduction: Why is this feature/process important?

Land-atmosphere interactions are key interactions that control the local and regional climate over several areas around the world. Although rainfall has a direct influence on soil moisture, the feedback loop is important for understanding the land-atmosphere coupling process (Koster et al., 2006). The feedback pathway between land and the atmosphere usually occurs in a two step process; impact of land characteristics (soil moisture) to surface fluxes, and the resulting control of boundary layer meteorology by the surface fluxes. These are referred to as the terrestrial and atmospheric segments of the land-atmosphere coupling process respectively (Dirmeyer, 2011). Since the coupling process is not explicitly represented in models, it is paramount for intercomparison studies in order to bring out information on resultant processes due to the parameterizations applied. Given the lack of sufficient observational data in Africa, coupled with model dependance of the processes, standardized frameworks such as Global Land–Atmosphere Coupling Experiment (GLACE) and Coupled Model Intercomparison Project (CMIP) offers opportunity platform for quantifying the land-atmosphere coupling processes (Guo et al., 2006)

# Diagnostic Overview: what does the diagnostic do?

The Terrestrial Coupling Index (TCI) is a statistical measure of the degree of sensitivity of surface fluxes (latent heat) to anomalies in the land surface characteristics, specifically soil moisture. The diagnostic is computed as a product of the correlation between soil moisture and latent heat and the standard deviation of soil moisture (Dimeyer, 2011). The correlation serves to highlight the strength and direction of the relationship, while the standard deviation highlights regions where large variability of soil moisture sustains the process (Halder et al., 2018). Positive (negative) TCI values indicate positive feedback; where soil moisture is a controlling factor in latent heat flux anomalies. Usually, this relationship exists in regions of abundant net radiation, with soil moisture being the limiting factor (Dimeyer, 2011; Koster el al., 2009). Consequently, the relationship does not hold in typically dry or saturated soils. 

# Step-by-step method: how is it calculated? 	
Step 1: Read in monthly data for soil moisture (mrsos) and latent heat flux (hlfs) 
Step 2: The year range is set as 1985-2014 for a 40 years period of the CMIP6 historical simulations or reanalysis data as the baseline
Step 3: Geographical domain for the analysis is selected to Africa, ranging from latitudes 26oS to 41oN and 20oW to 54oE longitudes 
Step 4: The monthly data is aggregated to get the seasonal means for the standard seasons, DJF, MAM, JJA and SON
Step 5: The correlation between mrsos and hfls is obtained as well as the standard deviation of mrsos. The product of the correlation and standard deviation defines the TCI.
TCI = correlation (mrsos,hfls) x standard_devation (mrsos) 

whereby mrsos  is soil moisture in m3/m3 and hfls is surface latent heat flux (+ve) in W/m2

Different datasets and models tend to have varied soil moisture depths as summarized in  Table 1. For all the analysis, the top layer was used. This is based on model results by Zhang et al., (2011) who noted that the uppermost layer of soil moisture (10cm) had dominant control over the evolution of surface fluxes. 




# Diagnostic Summary: what is output?

The TCI is a statistical representation of a complex process involving control of surface fluxes by soil moisture. The coupling patterns over Africa based on ERA5 indicates that characteristics are variable based on region and season. Positive feedbacks are pronounced over parts of eastern, southern and extreme northwestern Africa during DJF, wherelse the signal appears weaker through the other seasons. 

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/LLW/plots/llw_scatter_son_LLW_plot.png)


Figure 1: September-November 925hPa zonal moisture inflow at the western boundary (10S-10N and 10-12.5E) of Central Africa region representing the strength of Low-Level Westerlies (LLWs). b) Scatter plot representing the September-November 850hPa vertical wind average between 5S-3N and 2W-8E over the Gulf of Guinea and the 925hPa temperature gradient between Eastern Atlantic Ocean (average between 5S-3N and 2W-8E) and the continent (average between 5S-3N and 15E-25E).


# Acknowledgements
This diagnostic was designed by Anthony Mwanthi, adapted from Dirmeyer (2011), with support from Ellen Dyer. Thomas Webb developed the code framework for the LaunchPAD GitHub repository. The code was run using the UK’s JASMIN super-data-cluster. The reanalysis and model data were accessed courtesy of CEDA, and we acknowledge the data providers. The codes were originally written in NCL and transformed to Python.

 
# References
Dirmeyer, P. A. (2011). The terrestrial segment of soil moisture–climate coupling. Geophysical Research Letters, 38(16).

Koster, R. D., Sud, Y. C., Guo, Z., Dirmeyer, P. A., Bonan, G., Oleson, K. W., ... & Kowalczyk, E. (2006). GLACE: the global land–atmosphere coupling experiment. Part I: overview. Journal of Hydrometeorology, 7(4), 590-610.

Koster, R. D., Schubert, S. D., ... & Suarez, M. J. (2009). Analyzing the concurrence of meteorological droughts and warm periods, with implications for the determination of evaporative regime. Journal of Climate, 22(12), 3331-3341.

Zhang, L., Dirmeyer, P. A., Wei, J., Guo, Z., & Lu, C. H. (2011). Land–atmosphere coupling strength in the Global Forecast System. Journal of Hydrometeorology, 12(1), 147-156.

Guo, Z., Dirmeyer, P. A., Koster, R. D., Sud, Y. C., Bonan, G., Oleson, K. W., ... & McGregor, J. L. (2006). GLACE: the global land–atmosphere coupling experiment. Part II: analysis. Journal of Hydrometeorology, 7(4), 611-625.
