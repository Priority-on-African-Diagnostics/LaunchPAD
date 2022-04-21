"""
Diagnostic script for LaunchPAD TCI.
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
            data.coord("latitude").points = data.coord("latitude").points.round(2)
            data.coord("longitude").points = data.coord("longitude").points.round(2)

            # bounds aren't needed so just remove to avoid any potential issue.
            data.coord("latitude").bounds = None
            data.coord("longitude").bounds = None

            # convert units if needed
            if v == "mrsos":
                if data.units == "kg m-2":
                    data.units = "m^3 m-3"
                    data.data = data.data / 100.0
            elif v == "mrsol":
                # alternate conversion for TCI_mrsol
                if data.units == "kg m-2":
                    data = data[:, 0, :, :] / (1000.0 * data.coord("depth").points[0])
                    data.units = "m^3 m-3"

            prepped_data[d][v] = data

    return prepped_data


def calc_TCI(dataset):
    # calculate TCI

    tci = {}
    for seas in seasons:
        sea_con = iris.Constraint(clim_season=seas)
        if "mrsos" in dataset.keys():
            soilvar = dataset["mrsos"].extract(sea_con)
        else:
            soilvar = dataset["mrsol"].extract(sea_con)
        hfls = dataset["hfls"].extract(sea_con)

        # calculate Pearson correlation
        ccr = iris.analysis.stats.pearsonr(hfls, soilvar, corr_coords="time")

        # calculate standard deviation of mrsos
        stdd = soilvar.collapsed("time", iris.analysis.STD_DEV)

        tci[seas] = ccr * stdd

    return tci


def plot_TCI(data, ds, title):

    plt.figure(figsize=(7, 7))

    clevs = np.arange(-0.04, 0.05, 0.01)

    cmap = plt.cm.Spectral

    for i, seas in enumerate(seasons):
        tci = data[seas]

        plt.subplot(2, 2, i + 1)
        cf = iplt.contourf(tci, clevs, cmap=cmap, extend="both")
        plt.gca().coastlines()
        plt.gca().add_feature(cfeature.BORDERS, linewidth=0.2)
        plt.gca().add_feature(cfeature.OCEAN, zorder=100, color="snow")
        plt.gca().set_extent((-20, 54, -36, 41))
        plt.title(seas)

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation="vertical")
    plt.suptitle(title)

    plt.savefig(
        config["plot_dir"] + "/" + ds + "_TCI_plot.png", bbox_inches="tight", dpi=100
    )

    plt.close()


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        input_data = prep_data(config)
        for ds in input_data.keys():
            # calc TCI
            tci = calc_TCI(input_data[ds])
            if "mrsos" in input_data[ds].keys():
                title = f"{ds} TCI (hfls,mrsos)"
            else:
                title = f"{ds} TCI (hfls,mrsol)"
            plot_TCI(tci, ds, title)
