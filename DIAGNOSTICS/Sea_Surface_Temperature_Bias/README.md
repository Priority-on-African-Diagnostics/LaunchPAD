# Sea Surface Temperature Biases in the Gulf of Guinea

**Apphia Tetteh Ackon<sup>*</sup>**

Thompson Annor, Rachel James, Ellen Dyer, Thomas Webb

<sup>*</sup> Kwame Nkrumah University of Science and Technology
 
giresseturin@yahoo.fr  

*This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.*


# Introduction: Why is this feature/process important?
Sea Surface temperature (SST) has been studied to be one of the major drivers of precipitation over West Africa (Biasutti, 2019) with most of its influence from the Gulf of Guinea (GoG) Sea Surface Temperature (GoG SST) since it serves as the southern boundary of this sub-continent (Odekunle and Eluyodin, 2007). Warm GoG SST brings enhanced rainfall over the Guinea Coast region of West Africa and dry conditions over the Sahel region. Conversely, cold GoG SST results in decrease in rainfall over the Guinea Coast region and increase in rainfall over the Sahel (Paeth and Hense, 2006; Vizy and Cook, 2001). This shows the importance of GoG SST in regulating precipitation over West Africa.  
GoG SSTs have been studied to be very warm in coupled models (Creese and Washington, 2008), therefore it is relevant to evaluate how they perform in CMIP6 models. To know how effectively climate models represent this feature, there is the need to assess how they perform relative to observations. In this case, absolute bias is employed to evaluate the performance of the models. These models are relied on for future climate projections hence the ability of climate models to simulate well GoG SST will help in reducing the errors in these models leading to better performance.

# Diagnostic Overview: what does the diagnostic do?
This diagnostic calculates the Absolute Bias (AB) (difference between the model data and observed data). The observed dataset used is Hadley Center Sea Ice and Sea Surface Temperature version 1.1 (HadISST v1.1) with 1° by 1° resolution. Coordinates of the domain are 25°N, 40°S, 25°E and 25°W which  has been previously used to investigate Atlantic SST biases in CMIP5 models (Creese and Washington, 2018). An absolute bias of 0 implies the model captures the SST of the observed, a positive SST bias means the model is warmer than observation while negative SST bias means the model is colder than the observation. A map is output to illustrate the SST bias in four seasons. The period 1982-2012 has been used to calculate the bias.

# Step-by-step method: how is it calculated?    
1. The study period and domain are selected for both observed and model data

2.  The model data is regridded to the HadISST v1.1 resolution

3. Absolute bias is calculated (Model – Observed)

4. The absolute bias is calculated and plotted for each seasonal mean (DJF, MAM, JJA, SON) over the study area.


# Diagnostic Summary: what is output?
Here is an example of the diagnostic applied to HadGEM3-GC31-MM.  Warmest GoG SST biases (positive values) are observed in the JJA season, while cold biases (negative values) are shown in the south Atlantic for all the seasons. Only a few areas had an AB of 0.

![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/Sea_Surface_Temperature_Bias/plots/HadGEM3-GC31-MM_SST_bias_plot.png)

Figure. 1: Seasonal mean absolute SST bias (model – observed) for HadGEM3-GC31-MM relative to HadISSTv1.1 (K)

# Acknowledgements
This figure was designed by Apphia Tetteh Ackon. Special thanks to Rachel James, Ellen Dyer, and Thompson Annor for their guidance and contributions to this work. I am grateful to Ellen Dyer and Thomas Webb who converted this code to GitHub and auto-assess framework. I acknowledge all providers of HadISSTv1.1 and CMIP6 datasets.

# References
Biasutti, M. (2019). Rainfall trends in the African Sahel: Characteristics, processes, and causes. Wiley Interdisciplinary Reviews: Climate Change, 10(4), e591.


Creese, A., & Washington, R. (2018). A process-based assessment of CMIP5 rainfall in the Congo Basin: the September–November rainy season. Journal of Climate, 31(18), 7417-743

Odekunle, T. O., & Eludoyin, A. O. (2008). Sea surface temperature patterns in the Gulf of Guinea: their implications for the spatio‐temporal variability of precipitation in West Africa. International Journal of Climatology: A Journal of the Royal Meteorological Society, 28(11), 1507-1517.

Paeth, H., Hense A. 2006. On the linear response of tropical African climate to SST changes deduced from regional climate model simulations. Theoretical and Applied Climatology 83: 1–19


Vizy, E. K., & Cook, K. H. (2001). Mechanisms by which Gulf of Guinea and eastern North Atlantic sea surface temperature anomalies can influence African rainfall. Journal of Climate, 14(5), 795-821.
