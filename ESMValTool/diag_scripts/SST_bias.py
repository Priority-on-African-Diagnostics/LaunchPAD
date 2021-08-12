"""
Diagnostic script for LaunchPAD SST_bias.
"""

# to manipulate iris cubes
import iris
import iris.plot as iplt

import matplotlib.pyplot as plt

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic


seasons = {0: "DJF", 1: "MAM", 2: "JJA", 3: "SON"}


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
        # load data
        data = iris.load_cube(datasets[d][0]["filename"])
        # ensure no seam in the middle of our data
        data = data.intersection(longitude=(-180, 180))
        prepped_data[d] = data

    return prepped_data


def calc_bias(datasets):
    # calculate SST bias for all models
    # first get the obs data
    obs = datasets["HadISST"]

    biases = {}
    # now loop over the models
    for ds in datasets.keys():
        if ds == "HadISST":
            continue

        bias = datasets[ds] - obs

        biases[ds] = bias

    return biases


def plot_SST(data, expt):

    plt.figure(figsize=(5, 5))
    clevs = np.arange(-4.8, 5.2, 0.4)

    for seas in seasons.keys():
        bias = data.extract(iris.Constraint(season_number=seas))
        plt.subplot(2, 2, seas + 1)
        cf = iplt.contourf(bias, clevs, cmap="RdBu_r", extend="both")
        plt.gca().coastlines()
        plt.gca().set_extent((-25, 25, -40, 25))
        plt.title(seasons[seas])

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation="vertical")
    colorbar.set_label("K")
    plt.suptitle(expt + " SST biases")

    plt.savefig(
        config["plot_dir"] + "/" + expt + "_sst_bias.png", bbox_inches="tight", dpi=100
    )


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_data(config)
        data_for_plotting = calc_bias(data_for_plotting)
        for ds in data_for_plotting.keys():
            if ds == "HadISST":
                continue
            plot_SST(data_for_plotting[ds], ds)
