# LaunchPAD: Priority on African Diagnostics

LaunchPAD is the first phase of the Climate Model Evaluation Hub for Africa. The aim of this project is to create diagnostics that can be used in model evaluations for Africa. 10 early career researchers and LaunchPAD fellows created the diagnostics shared in this repository. 

To learn more about LaunchPAD, the fellows, and their diagnositcs take a look at our project website: https://launchpad6.home.blog 

Each of the diagnostics have an folder within DIAGNOSTICS. Here you will also find a README for each diagnostic that details the rational for the diagnostic, a step by step method, and some sample plots. These also contain the contact information of the fellow responsible for each diagnostic and their contact information. __Not all of these diagnostic methods have been published and permission to cite requires permission from the authors of the diagnostic.__ 

This repository of diagnostics has been designed to run on the JASMIN data analysis facility (https://www.jasmin.ac.uk) and with the CEDA archive of CMIP6 model output (https://help.ceda.ac.uk/article/4801-cmip6-data). However, if you download the required data from the CEDA archive you can modify configuration files in the files/CONFIG directory to run diagnostics over a different system. 

All of the diagnostics use the same set of basic configuration files in files/CONFIG:
* *config.py* contains some hardcoded items like a list of models to search for, month names and file extensions
* *config_find_files.py* contains markers for model locations and specific information such as modelling group/institution
* *find_files.py* defines absolute paths for model and observational files on JASMIN and in the LaunchPAD group work space
* *config_functions.py* contains definitions that are used in diagnostic calculations

In each diagnostic directory there is a *diagnostic*.py file which is where the diagnostic is calculated and plotted. This is the only python file you need to execute. There is also a *diagnostic*\_config.py 
