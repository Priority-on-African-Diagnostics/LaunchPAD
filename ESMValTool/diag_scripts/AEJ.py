"""
Diagnostic script for LaunchPAD AEJ.
"""

# to manipulate iris cubes
import iris
import matplotlib.pyplot as plt

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic
from esmvalcore.preprocessor import climate_statistics, zonal_statistics


def prep_for_plotting(cfg):
    """
    Arrange data to be ready for plotting routines.
    Return a dictionary of the prepped data

    Arguments:
        cfg - nested dictionary of metadata

    Returns:
        dictionary of cubes ready for plotting
    """
    # first organise data by dataset, then variable
    datasets = group_metadata(cfg["input_data"].values(), "dataset")
    prepped_data = {}

    # process
    for d in datasets:
        variables = group_metadata(datasets[d], "variable_group")
        prepped_data[d] = {}
        for v in variables:
            # load data
            data = iris.load_cube(variables[v][0]["filename"])

            # additional processing necessary for uN
            if v == "uN":
                # collapse pressure dimension by taking minimum
                data = data.collapsed("air_pressure", iris.analysis.MIN)
                # compute zonal mean
                data = zonal_statistics(data, "mean")
                # compute monthly means
                data = climate_statistics(data, "mean", "month")

            prepped_data[d][v] = data

    return prepped_data


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_for_plotting(config)
