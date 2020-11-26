# Atmospheric Coupling Index

**Anthony Mwanthi<sup>*</sup>**

Ellen Dyer, Thomas Webb

<sup>*</sup> Department of Meteorology, University of Nairobi
 
 mmwanthi@gmail.com 
or anthony.mwanthi@students.uonbi.ac.ke 

*This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.*


## Introduction: Why is this feature/process important?
Land-atmosphere interactions are inherent processes to represent in climate models. The land surface characteristics respond to atmospheric processes, such as rainfall events resulting in soil moisture anomalies which consequently modulate the budget of surface moisture and heat fluxes. The feedback pathway is depicted by surface fluxes exerting influence on the boundary layer meteorological variables, such as humidity and temperature (Dirmeyer, 2011). This is usually referred to the atmospheric leg of the land-atmosphere coupling process. These feedback characteristics are dependent on region, scale and model parameterizations (Koster et al., 2006). It thus points to a key diagnostic to consider in model evaluation. The diagnostic specifically brings out information on performance of model parameterizations related to moisture and energy balance. 

## Diagnostic Overview: what does the diagnostic do?
The Atmospheric Coupling Index (ACI) is a statistical computation to indicate the degree of sensitivity of lower atmospheric variables (temperature) to variability in the surface fluxes (latent heat flux). The computation is based on the product of their correlation with the standard deviation of the ‘driving’ variable (latent heat). Although correlation alone may be used to indicate association, the standard deviation serves to highlight regions whereby the coupling relationship is driven by large variability of latent heat flux (Halder _et al_., 2018). Negative (positive) values will show regions of negative (positive) feedback. 

Near surface temperature typically has a negative response to latent heat flux anomalies Seneviratne et al., (2010). This is related with partitioning of surface energy, whereby positive anomalies in latent heat limits sensible heat flux, thus resulting in negative temperature anomalies. 

## Step-by-step method: how is it calculated?
Step 1: Read in monthly data for surface latent heat flux (hfls) and near surface (2metre) temperature (tas)

Step 2: The year range is set as 1985-2014 for a 40 years period of the CMIP6 historical simulations or reanalysis data as the baseline

Step 3: Geographical domain for the analysis is selected to Africa, ranging from latitudes 26oS to 41oN and 20oW to 54oE longitudes 

Step 4: The monthly data is aggregated to get the seasonal means for the standard seasons, DJF, MAM, JJA and SON

Step 5: The correlation between hfls and tas is obtained as well as the standard deviation of hfls. The product of the correlation and standard deviation defines the ACI.

ACI = correlation (hfls,tas) x standard_devation (hfls) 

whereby _hfls_ is latent heat flux (+ve) in W/m<sup>2</sup> and tas is 2 metre temperature (oC) 

## Diagnostic Summary: what is output?
The spatial map presents the ACI patterns over Africa for ERA5 and CMIP6 models. 

For ERA5, the results indicate a negative feedback relationship between surface latent heat flux and temperature with varying intensities. In Southern Africa, East Africa and parts of the Sahel have quite a strong variability of latent heat flux, which yields a negative feedback with near surface temperature. Regions in the Sahara and parts of Central Africa, with weakest signal indicates a weak coupling. In regions with positive values, which also experience the least variability of latent heat variability, indicates that surface fluxes have no significant control over surface temperature. The coupling patterns indicate seasonal variability, with DJF and MAM presenting higher magnitudes over Southern and Eastern Africa, while JJA has the least signal over Africa JJA. 

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/Aerosol%20Coupling%20Index/plots/ERA5_ACI_plot.png)

Figure 1. Atmospheric Coupling Index over Africa based on ERA5 for the four seasons.

In Figure 2, the results are presented based on the HadGEM-G31-MM model. Similar to the ERA5, there is a strong signal in Southern Africa during DJF and MAM seasons and weak signals for JJA and SON. Coupling strengths over the Sahel and East Africa are much weaker. In the majority of the rest of the continent, the relationship is very weak due to the low variability of latent heat flux. This shows that the model does not capture the variability latent heat in most of Africa except the southern regions during DJF and MAM. 

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/Aerosol%20Coupling%20Index/plots/HadGEM3-GC31-MM_ACI_plot.png)

Figure 2. Atmospheric Coupling Index over Africa based on HadGEM-GC31-MM model for the four seasons.

## Acknowledgements
This diagnostic was designed by Anthony Mwanthi, adapted from Dirmeyer (2011), with support from Ellen Dyer. Thomas Webb developed the code framework for the LaunchPAD GitHub repository. The code was run using the UK’s JASMIN super-data-cluster. The reanalysis and model data were accessed courtesy of CEDA, and we acknowledge the data providers. The codes were originally written in NCL and transformed to Python.

## References

Dirmeyer, P. A. (2011). The terrestrial segment of soil moisture–climate coupling. Geophysical Research Letters, 38(16). 

Halder, S., Dirmeyer, P. A., Marx, L., & Kinter III, J. L. (2018). Impact of Land Surface Initialization and Land-Atmosphere Coupling on the Prediction of the Indian Summer Monsoon with the CFSv2. Frontiers in Environmental Science, 5, 92.

Koster, R. D., Sud, Y. C., Guo, Z., Dirmeyer, P. A., Bonan, G., Oleson, K. W., … & Kowalczyk, E. (2006). GLACE: the global land–atmosphere coupling experiment. Part I: overview. _Journal of Hydrometeorology_, _7_(4), 590-610.

Seneviratne, S. I., Corti, T., Davin, E. L., Hirschi, M., Jaeger, E. B., Lehner, I., … & Teuling, A. J. (2010). Investigating soil moisture–climate interactions in a changing climate: A review. _Earth-Science Reviews_, _99_(3-4), 125-161.
