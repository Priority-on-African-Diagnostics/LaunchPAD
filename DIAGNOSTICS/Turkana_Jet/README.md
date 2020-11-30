# Turkana Low-level Jet
Oscar Lino<sup>**</sup>***

Ellen Dyer, Thomas Webb

<sup>*</sup> University of Nairobi, Kenya
 
linowanjala@gmail.com

**This document has not been published. Permission to quote from it must be obtained from the author using the above contact details.**



# Introduction: Why is this feature/process important?
This diagnostic identifies the Turkana low-level jet, which flows through the Turkana channel in Northern Kenya. The Turkana Jet has great socio-economic importance due to its influence on wind and rainfall. Over Kenya, it has great potential to provide low-cost green energy to drive Kenya’s development activities. For countries to the north of Kenya, it is a transporter of moisture-laden air and therefore influences rainfall. The jet is considered a moisture transport channel, influencing the region’s climate by bringing aridity to most of the region (Trewartha 1981; Flohn, 1964; Griffiths, 1972; Nicholson, 1996; Indeje et al 2001) and redistributing rainy regimes to other places further North (Nicholson, 2015; Lino et al 2020). The purpose of this diagnostic is to improve our understanding of the Turkana Jet structure and variability in the models, because simulations of rainfall and winds by some climate models over parts of East Africa and Northern Kenya are poor due to inadequate representation of this feature. Some models exhibit a weaker jet, some no jet at all, depending on the representation of topography in the Turkana channel. Some models can have shallow, and unrealistic channels which can affect wind speed. In such models the Turkana and Somali jets can appear conflated when the Somali LLJ is active, underestimating or overestimating moisture transport and hence exhibit biases in timing of rainfall onsets and cessations, and locating regions of enhanced rainfall (over Northern Kenya and Ethiopia).

# Diagnostic Overview: what does the diagnostic do?
The method entails identification of the climatological strength and location of the Turkana low level jet by filtering the mean wind over Northern Kenya for speed of magnitudes less than 5 m/s. An analysis of mean states in humidity fields is also performed to show influx of moisture. 

# Step-by-step method: how is it calculated? 	
Step 1: Read in monthly data for horizontal vector wind components (U and V), and specific humidity (q) at 850mb

Step 2: The year range is set as 1985-2014 for a 40 years period of the CMIP6 historical simulations or reanalysis as the baseline

Step 3: Spatial extent is chosen for East Africa, bounded by latitudes 50S to 8oN and longitudes 32oE to 43oE

Step 4: The monthly data is aggregated to monthly climatological means, from January to December

Step 5: Two quantities are derived; 
    The scalar wind (ϑ) = sqrt(u*u + v*v)
And 
    The moisture flux (qϑ) = q* ϑ

Whereby the units for moisture flux are g/Kg/m/s, ϑ is in m/s, and q is in g/Kg.

Step 6: Filled contours for moisture flux (shading) are drawn and overlaid by the U and V vectors, and points of ϑ< 5m/s are masked out. 

# Diagnostic Summary: what is output?

The diagnostic generates a map showing wind shears as the jet intensifies as well as where the model places the jet on the spatial map and in which direction. Moisture flux is also drawn to show the effect of the jet on the humidity field. 


<img src="https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/54ff08ccd72c0184df2b2d82016566e2836cca0e/DIAGNOSTICS/Turkana%20Jet/plots/ERA5_TJ1_plot.png" width="350"/> <img src="https://github.com/Priority-on-African-Diagnostics/LaunchPAD/blob/54ff08ccd72c0184df2b2d82016566e2836cca0e/DIAGNOSTICS/Turkana%20Jet/plots/HadGEM3-GC31-MM_TJ1_plot.png" width="350"/> 

Figure: a) ERA5 and b) HadGEM3-GC31-MM mean monthly moisture flux at 850mb (g/Kg/m/s) (contour shading), overlaid with mean wind vector at 850mb (m/s). Wind vectors indicate winds of at least 5m/s.

# Acknowledgements
This diagnostic was developed by Oscar Lino (University of Nairobi). It  was formatted and programmed by Dr Ellen Dyer, to be embedded into this LaunchPAD GitHub framework designed by Dr Thomas Webb. Dr Thomas Webb also embedded  the diagnostic into the UK Met Office Auto-Assess system. The diagnostic was developed and run using the UK's JASMIN super-data-cluster. The reanalysis and CMIP 6 AMIP models were accessed courtesy of CEDA, and we acknowledge the data providers. 

# References
Flohn H. 1964. On the causes of aridity of northeastern Africa. Würzburger Geograph. Arb. 12: 1–17

Indeje M, Semazzi FHM, Xie L, Ogallo LJ. 2001. Mechanistic model simulations of the East African climate using NCAR regional climate model: influence of large-scale orography on the Turkana low-level jet. J. Clim. 14: 2710–2724

Nicholson, S. (2015). The Turkana low-level jet: mean climatology and association with regional aridity. International Journal of Climatology, 36(6), 2598–2614. doi:10.1002/joc.4515 

Nicholson SE. 1996. A review of climate dynamics and climate variability in eastern Africa. In The Limnology, Climatology and Paleoclimatology of the East African Lakes, Johnson TC, Odada EO (eds). Gordon and Breach: Toronto, Canada, 25–56
