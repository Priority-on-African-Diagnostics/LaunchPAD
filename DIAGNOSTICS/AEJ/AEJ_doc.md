# Introduction: Why is this feature/process important?
 The African Easterly Jet is a prominent feature of the mid tropospheric zonal wind that forms over central Africa. The jet is considered to play a crucial role in rainfall development over the central Africa region during September to November (Nicholson and Grist 2003). The jet presents two components. A northern component known as the African Easterly Jet North (AEJ-N) of the northern hemisphere, and a southern component known as the African Easterly Jet South (AEJ-S) of the southern hemisphere. Nicholson and Grist (2003) were the first authors to use this appellation for these two mid-level jets to distinguish them. The climatological AEJ-N is identifiable throughout the year from January when it lies at its southernmost location (3N) and move northward to its most northern location in August (13N) with maximum wind speeds attending 13 m_s in September, as it begins shifting southward towards the equator (Nicholson and Grist 2003). Characteristics of the southern component was also described by these authors, they state that AEJ-S is well defined from September to November and its core location lies between 5S and 10S with mean core speed reaching 8 m_s . While some studies have used reanalysis data to understand the dominant processes of climate variability in Central Africa by highlighting the important role of AEJ-N (Pokam et al. 2012; Dezfuli and Nicholson 2013; Nicholson and Dezfuli 2013) and AEJ-S (Jackson et al. 2009; Kuete et al. 2019), some studies on model process-based evaluation have shown that model rainfall biases are mainly related to bias in terms of location and intensity of AEJs in models (Creese and Washington 2018; Tamoffo et al. 2019).


# Diagnostic Overview: what does the diagnostic do?
Note that the AEJs are defined as monthly-mean easterly winds with values exceeding 6 m.s-1. And it has been shown that the AEJs are thermal winds, located slightly equator-ward of the lower tropospheric meridional temperature gradient (Nicholson and Grist 2003; Adebiyi and Zuidema 2016).  The northern component of the African Easterly Jet (AEJ-N) is present all year and results from the positive meridional surface temperature gradient while southern component (AEJ-S) is only present from September to November and results from the negative meridional surface temperature gradient. 

Locations and intensities of the jet cores (U ≤ -6 m/s) are calculated using 600hPa easterly winds. And averaged in the longitude range of [12E-24E]. 

Two figures are generated: (1) the climatological temperature gradient and jet core across latitudes and months, and (2) the annual cycle of the jets’ latitudinal location and intensity.


# Step by step method: how is it calculated?


### Figure 1: How to calculate and plot surface temperature gradient


Step 1: load temperature data over central Africa domain (20S-20N, 10-30E) and select 925 hPa pressure level

Step 2: calculate temperature monthly mean climatology and average over the longitude range (14-24E) 

Step 3: calculate the meridional temperature gradient using gradient formula which divides the change in temperature over the entire domain by the change in latitude values between (20S-20N). 

Step 4 plot temperature gradient values calculated in step 3

Step 5 plot AEJ core latitude (see Figure 2 for how to calculate)


### Figure 2: How to calculate and plot African Easterly jets components core mean location and intensity


Step 1: load model or reanalysis monthly zonal winds over central Africa domain (20S-20N, 10-30E) 
and select 700 and 600 hPa pressure levels

As the two jets (northern and southern) components are located in different domains, to represent locations and intensities of the two components, we have to extract AEJ-N (northern component) and AEJ-S (southern component) from the monthly zonal winds of our domain 

Step 2: 
create variable In which represent AEJ-N in the latitudinal range (3N-20N)
create variable Us which represent  AEJ-S in the latitudinal range (5S-20S) 

Step 3 
now calculate Un monthly mean climatology and average over the longitude range (12-24E) 
between 700 and 600 hPa levels (AEJ-N is located at 700 hPa from January to August and at 600 hPa from September to December)

also calculate Us  monthly mean climatology and average over the longitude range (12-24E) 
and select 600 hPa pressure level (AEJ-S is only present at 600hPa)

Step 4:  
calculate for all months and for all latitude points minimum value for Un and Us

As noted in the diagnostic overview, African Easterly Jets are defined as monthly-mean easterly winds with values exceeding -6 m.s-1. The Minus sign stands here for winds that are easterlies since the jets are easterly winds.

 Step 5: extraction of core mean locations and intensities of each component 

 - location and intensity of AEJ-N

 if for each latitude point and for each month and for the two levels 700 and 600 hPa,  the value of Un is equal to minimum value and minimum value of Un is lower or equals to -6 (-6 is threshold) then retain the latitude and intensity corresponding 

 - location and intensity of AEJ-S

if for each latitude point and for each month and for level 600 hPa level,  the value of Us is equal to minimum value of Us and minimum value of Us is lower or equals to -6 (-6 is threshold) then retain the latitude point and intensity corresponding

Step 6: plot latitude points and intensities for each month retain in step 5



# Diagnostic Summary: what is output?

![](AEJ_doc/H4T5dMSnKszJtnVqcSjAoR-UgcbC3Cfh0GMnTrbiEqRmEb-biSvDUgzCoMOjOsY8cltUrVIp-gft4vjw0_NoJMVLu6fLqwK2TiYTMK1iVtlo6u3yykVtq6OrsslGLg.png)


Figure 1. Latitude_time evolution of the 850 hPa surface temperature gradient (in K_m) with overlay mean locations of AEJ components core. Black solid line in the north represents AEJ-N and the red solid line in the south is the AEJ-S.


![](https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/master/DIAGNOSTICS/AEJ/plots/AEJ_plot_SAM0-UNICON_AEJ_plot.png)

Figure 2: African Easterly Jet components locations (Bottom row) and intensities (Top row).

## Acknowledgements
This work uses CMIP6 model data and reanalysis data of ERA-5 and MERRA-2. We acknowledge all of the data providers. The diagnostics were designed by Giresse Kuete.
We acknowledge Tom Webb (thomas.webb@ouce.ox.ac.uk) and Ellen Dyer ( ellen.dyer@ouce.ox.ac.uk ) for designing and coding in python based on diagnostic scripts from Giresse Kuete ( giresseturin@yahoo.fr ) also we thank the helpful inputs of Wilfried Pokam ( wpokam@yahoo.fr ), Rachel James (rachel.james@ouce.ox.ac.uk) and and Richard Washington (richard.washington@ouce.ox.ac.uk) for supervising.

## References
Cook, K. H. (1999). Generation of the African Easterly Jet and Its Role in Determining West African Precipitation. _Journal of Climate,_ _12_(5), 1165-1184. doi:10.1175/1520-0442(1999)0122.0.co;2

Creese, A., & Washington, R. (2018). A Process-Based Assessment of CMIP5 Rainfall in the Congo Basin: The September–November Rainy Season. _Journal of Climate,_ _31_(18), 7417-7439. doi:10.1175/jcli-d-17-0818.1

Creese, A., & Washington, R. (2016). Using qflux to constrain modeled Congo Basin rainfall in the CMIP5 ensemble. _Journal of Geophysical Research: Atmospheres,_ _121_(22). doi:10.1002/2016jd025596

Dezfuli, A. K., & Nicholson, S. E. (2013). The Relationship of Rainfall Variability in Western Equatorial Africa to the Tropical Oceans and Atmospheric Circulation. Part II: The Boreal Autumn. _Journal of Climate,_ _26_(1), 66-84. doi:10.1175/jcli-d-11-00686.1

Jackson, B., Nicholson, S. E., & Klotter, D. (2009). Mesoscale Convective Systems over Western Equatorial Africa and Their Relationship to Large-Scale Circulation. _Monthly Weather Review,_ _137_(4), 1272-1294. doi:10.1175/2008mwr2525.1

 Kuete, G., Mba, W. P., & Washington, R. (2019). African Easterly Jet South: Control, maintenance mechanisms and link with Southern subtropical waves. _Climate Dynamics,_ _54_(3-4), 1539-1552. doi:10.1007/s00382-019-05072-w

Nicholson, S. E., & Dezfuli, A. K. (2013). The Relationship of Rainfall Variability in Western Equatorial Africa to the Tropical Oceans and Atmospheric Circulation. Part I: The Boreal Spring. _Journal of Climate,_ _26_(1), 45-65. doi:10.1175/jcli-d-11-00653.1
Nicholson, S. E., & Grist, J. P. (2003). The Seasonal Evolution of the Atmospheric Circulation over West Africa and Equatorial Africa. _Journal of Climate,_ _16_(7), 1013-1030. doi:10.1175/1520-0442(2003)0162.0.co;2

Pokam, W. M., Djiotang, L. A., & Mkankam, F. K. (2011). Atmospheric water vapor transport and recycling in Equatorial Central Africa through NCEP_NCAR reanalysis data. /Climate Dynamics,_ _38_(9-10), 1715-1729. doi:10.1007/s00382-011-1242-7
Tamoffo, A. T., Moufouma-Okia, W., Dosio, A., James, R., Pokam, W. M., Vondou, D. A., . . . Nouayou, R. (2019). Process-oriented assessment of RCA4 regional climate model projections over the Congo Basin under $$1.5  ^{circ }{text {C}}$$ 1.5 ∘ C and $$2  ^{circ }{text {C}}$$ 2 ∘ C global warming levels: Influence of regional moisture fluxes. _Climate Dynamics,_ _53_(3-4), 1911-1935. doi:10.1007/s00382-019-04751-y
