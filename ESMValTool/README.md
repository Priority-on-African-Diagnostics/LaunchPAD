# LaunchPAD: Priority on African Diagnostics

## ESMValTool versions of LaunchPAD diagnostics.

A number of the LaunchPAD diagnostics have been converted by Tom Crocker of the UK Met Office (thomas.crocker@metoffice.gov.uk) into recipes for use with ESMValTool.

ESMValTool https://www.esmvaltool.org/ is a piece of software designed for computing diagnositcs and performance metrics of Earth System Models (ESMs). Documentation is available at: https://docs.esmvaltool.org/en/latest/ The ESMValTool tutorial available at: https://esmvalgroup.github.io/ESMValTool_Tutorial/ is also useful for new users.

A central installation of ESMValTool is available on the JASMIN data analysis facility (https://www.jasmin.ac.uk). The recipes provided as part of this repository are designed to be run with this installation, and using the CEDA archive of CMIP6 model output (https://help.ceda.ac.uk/article/4801-cmip6-data). However, if you have a local installtion of ESMValTool and download the required data from the CEDA archive, you can modify the `config-user.yml` and `config-developer.yml` configuration files as appropriate to run the recipes elsewhere.

The recipes are located in the `recipes/` sub folder. The recipes describe the datasets (models and observations / reanalysis) that are used in each diagnostic, as well as various pre processing operations that are performed (e.g. time and region extraction, computing monthly means etc.). Most settings for a diagnostic that a user might want to change (for example the list of models to be used) can be modified in the recipe files. Recipes are written in a mark up language called YAML. YAML is relatively simple to learn, see for example https://learnxinyminutes.com/docs/yaml/).

The python scripts that compute the final diagnostic and plot them are stored in the `diag_scripts/` sub folder. These are called by ESMValTool after completing the pre-processing specified in each recipe.

## Running the ESMValTool diagnostics

The GitHub repository should be cloned as per the instructions at the top level of this repo.

The `config-user.yml` and `config-developer.yml` files from this folder should be copied to the `.esmvaltool/` folder in your home folder.

    cp config-*.yml ~/.esmvaltool/
To run the recipes on JASMIN, the ESMValTool module should first be activated.

    module load esmvaltool

Recipes should then be run using the command:

    esmvaltool run <recipe filename>

If the LaunchPAD repository has not been cloned into your home folder (i.e. `~/LaunchPAD/`), then the value of the `script:` key at the bottom of the recipe will need changing to point to the full path of the `LaunchPAD/ESMValTool/diag_scripts/` folder.

Output will appear under a folder `esmvaltool_output/` in whatever directory the `esmvaltool` command was run from. (This can be changed in the `config-user.yml` settings file if desired.) A subfolder `<recipe name>_<YYYYMMDD_HHMMSS>/`, with the time and datestamp corresponding to the time the recipe was run, will be created for each execution of `esmvaltool`. Plots will be contained in a `plots/` subfolder under this folder, with pre processed netCDF files from the recipe stored under `preproc/`. Log files produced while running the recipe and diagnostic are stored under the `run/` subfolder and are very useful for diagnosing any problems that may occur.

## Status of LaunchPad diagnostics

N.B. MERRA2 observations are not currently supported.

Diagnostic | Status
---------- | ------
African Easterly Jet | `recipe_African_Easterly_Jet.yml`
Atmospheric Coupling Index | `recipe_ACI.yml` CMIP6 models work fine. The ERA5 hfls data in the workspace needs it's units attribute setting to be used.
Central African Easterlies | `recipe_CAF.yml`
Low Level Westerlies | `recipe_LLW.yml`
Mozambique Channel Trough | Not supported as Windspharm module is not currently part of the ESMValTool conda environment on JASMIN.
Sea Surface Temperature Bias | `recipe_SST_bias.yml`
Storm Tracks | Not supported as Windspharm module is not currently part of the ESMValTool conda environment on JASMIN.
Terrestrial Coupling Index | `recipe_TCI.yml` Some CMIP6 models do not work due to unavailability of data.<br>The ERA5 hfls data in the workspace needs it's units attribute setting to be used.<br> FGOALS-g3 currently does not work, but a fix has been added to ESMValTool that will support it in the next release. (See https://github.com/ESMValGroup/ESMValCore/issues/1288).<br> CESM2 does not work due to a missing depth co-ordinate in the mrsos data.
Terrecstrial Coupling Index mrsol | `recipe_TCI.yml` The only model that works in this recipe is UKESM1-0-LL (due to availability of data). All other models should be commented out.<br>Line 248 in the recipe (`<<: *mrsos`) should be changed to (`<<: *mrsol`) to switch the recipe processing from mrsos to mrsol.
Tropical Cyclone Tracking | Not supported as Windspharm module is not currently part of the ESMValTool conda environment on JASMIN.
Turkana Jet | `recipe_Turkana_Jet.yml`
West African Heat Low, Rain Band and Heat Band | `recipe_WAHL.yml` - Requires ESMValCore issue 333 to be resolved. https://github.com/ESMValGroup/ESMValCore/issues/333.<br>`recipe_WARB.yml`<br>`recipe_WAHB.yml`
West African Westerly Jet | Requires ESMValCore issue 333 to be resolved. https://github.com/ESMValGroup/ESMValCore/issues/333