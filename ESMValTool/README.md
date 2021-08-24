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

`esmvaltool run <recipe filename>`

If the LaunchPAD repository has not been cloned into your home folder (i.e. `~/LaunchPAD/`), then the value of the `script:` key at the bottom of the recipe will need changing to point to the full path of the `LaunchPAD/ESMValTool/diag_scripts/` folder.

Output will appear under a folder `esmvaltool_output/` in whatever directory the `esmvaltool` command was run from. (This can be changed in the `config-user.yml` settings file if desired.) A subfolder `<recipe name>_<YYYYMMDD_HHMMSS>/`, with the time and datestamp corresponding to the time the recipe was run, will be created for each execution of `esmvaltool`. Plots will be contained in a `plots/` subfolder under this folder, with pre processed netCDF files from the recipe stored under `preproc/`. Log files produced while running the recipe and diagnostic are stored under the `run/` subfolder and are very useful for diagnosing any problems that may occur.