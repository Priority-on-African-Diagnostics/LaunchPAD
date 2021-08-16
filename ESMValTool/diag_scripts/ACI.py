"""
Diagnostic script for LaunchPAD ACI.
"""

# to manipulate iris cubes
import iris
import iris.plot as iplt
import iris.analysis.stats
import cartopy.feature as cfeature

import matplotlib.pyplot as plt

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic


seasons = ["DJF", "MAM", "JJA", "SON"]


def prep_data(cfg):
    """
    Arrange data to be ready for plotting.
    Return a dictionary of the prepped data

    Arguments:
        cfg - nested dictionary of metadata

    Returns:
        dictionary of cubes
    """
    # organise data by dataset
    datasets = group_metadata(cfg["input_data"].values(), "dataset")
    prepped_data = {}

    # process
    for d in datasets:
        variables = group_metadata(datasets[d], "variable_group")
        prepped_data[d] = {}
        for v in variables:
            # load data
            data = iris.load_cube(variables[v][0]["filename"])
            # ensure no seam in the middle of our data
            data = data.intersection(longitude=(-180, 180))

            # fix for minor rounding issue with coords in some models
            data.coord("latitude").points = data.coord("latitude").points.round(10)
            data.coord("latitude").bounds = None
            data.coord("longitude").points = data.coord("longitude").points.round(10)
            data.coord("longitude").bounds = None

            prepped_data[d][v] = data

    return prepped_data


def calc_ACI(dataset):
    # calculate ACI

    aci = {}
    for seas in seasons:
        sea_con = iris.Constraint(clim_season=seas)
        hfls = dataset["hfls"].extract(sea_con)
        tas = dataset["tas"].extract(sea_con)

        # calculate Pearson correlation
        ccr = iris.analysis.stats.pearsonr(hfls, tas, corr_coords="time")

        # calculate standard deviation of hfls
        stdd = hfls.collapsed("time", iris.analysis.STD_DEV)

        aci[seas] = ccr * stdd

    return aci


def plot_ACI(data, expt):
    # make the plot
    plt.figure(figsize=(7, 7))
    clevs = np.arange(-18, 20, 2)

    for seas in seasons:
        aci = data[seas]

        plt.subplot(2, 2, seasons.index(seas) + 1)
        cf = iplt.contourf(aci, clevs, cmap="RdBu_r", extend="both")
        plt.gca().coastlines()
        plt.gca().add_feature(cfeature.BORDERS, linewidth=0.2)
        plt.gca().add_feature(cfeature.OCEAN, zorder=100, color="snow")
        plt.gca().set_extent((-20, 54, -36, 41))
        plt.title(seas)

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation="vertical")
    # colorbar.set_label(' ')
    plt.suptitle(expt + " ACI (tas,hfls)")

    plt.savefig(
        config["plot_dir"] + "/" + expt + "_ACI_plot.png", bbox_inches="tight", dpi=100
    )

    plt.close()


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        input_data = prep_data(config)
        for ds in input_data.keys():
            # calc ACI
            aci = calc_ACI(input_data[ds])
            plot_ACI(aci, ds)
