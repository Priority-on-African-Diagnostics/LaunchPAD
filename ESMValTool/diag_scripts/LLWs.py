"""
Diagnostic script for LaunchPAD LLWs.
"""

# to manipulate iris cubes
import iris
import xarray as xr

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic

obs_list = ["ERA5", "MERRA2"]
mon_names = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

seasons = {0: "DJF", 1: "MAM", 2: "JJA", 3: "SON"}


def prep_data(cfg):
    """
    Arrange data to be ready for further calculations plotting.
    Return a dictionary of the prepped data

    Arguments:
        cfg - nested dictionary of metadata

    Returns:
        dictionary of cubes
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

            # convert to xarray
            data = xr.DataArray.from_iris(data)

            # additional processing
            if v == "psl":
                data = data / 100.0
            elif v == "wap":
                data = data * 100.0

            prepped_data[d][v] = data

    return prepped_data


def calculations(ds_list):
    """Calculate temp gradients and moisture flux

    Args:
        ds_list (dict): Processed dictionary of data
    Returns:
        dictionary with added temp gradient info
    """
    # loop over datasets
    for d in ds_list.keys():
        t_grad = ds_list[d]["ta_CA"] - ds_list[d]["ta_EAO"]
        ds_list[d]["t_grad"] = t_grad

        mflux = ds_list[d]["ua"] * ds_list[d]["hus"] * 1000.0
        ds_list[d]["mflux"] = mflux

    return ds_list


def plot_figure1(ds_list):

    colour_list = [
        "black",
        "blue",
        "orange",
        "green",
        "red",
        "purple",
        "brown",
        "pink",
        "gold",
        "gray",
        "olive",
        "cyan",
        "navy",
        "peru",
        "rosybrown",
        "lime",
        "teal",
        "fuchsia",
        "chartreuse",
        "dodgerblue",
        "mediumseagreen",
        "salmon",
        "rebeccapurple",
    ]

    shape_list = [
        "o",
        "v",
        "^",
        "<",
        ">",
        "s",
        "P",
        "p",
        "D",
        "X",
        "*",
        "o",
        "v",
        "^",
        "<",
        ">",
        "s",
        "P",
        "p",
        "D",
        "X",
        "*",
        "o",
        "v",
        "^",
        "<",
        ">",
        "s",
        "P",
        "p",
        "D",
        "X",
        "*",
    ]

    for seas in seasons.keys():
        fig, (ax1, ax2) = plt.subplots(2, figsize=(5, 10))

        height = []
        y_pos = np.arange(len(ds_list.keys()))
        for expt in ds_list.keys():
            mflux = ds_list[expt]["mflux"].sel(season_number=seas).values.item()
            height.append(mflux)

        ax1.set(ylabel="Moisture Flux CA Western Boundary (g.Kg-1 m.s-1)")

        ax1.bar(y_pos, height, color=colour_list)
        ax1.set_xticks([])
        ax1.set_ylim(0.0, max(height) + 5.0)

        box = ax1.get_position()
        ax1.set_position([box.x0, box.y0, box.width * 0.95, box.height])
        ax1.set_title(seasons[seas])

        gradl = []
        wapl = []
        for count, expt in enumerate(ds_list.keys()):
            gradv = ds_list[expt]["t_grad"].sel(season_number=seas).values.item()
            wapv = ds_list[expt]["wap"].sel(season_number=seas).values.item()
            gradl.append(gradv)
            wapl.append(wapv)

            ax2.scatter(
                gradv,
                wapv,
                s=80,
                label=expt,
                marker=shape_list[count],
                color=colour_list[count],
            )

        ax2.set(
            xlabel="Temperature gradient (K)",
            ylabel="Vertical velocity index (hPa s-1)",
        )
        ax2.xaxis.set_minor_locator(MultipleLocator(0.1))
        ax2.yaxis.set_minor_locator(MultipleLocator(0.2))
        ax2.set_xlim(min(gradl) - 0.2, max(gradl) + 0.2)
        ax2.set_ylim(min(wapl) - 0.2, max(wapl) + 0.2)
        ax2.set_title(seasons[seas])

        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.95, box.height])

        fig.legend(loc="center left", bbox_to_anchor=(1, 0.5))

        plt.savefig(
            config["plot_dir"] + "/llw_scatter_" + seasons[seas] + "_plot.png",
            bbox_inches="tight",
            dpi=200,
        )


def plot_figure2(ds_list):
    datasets = list(ds_list.keys())

    for seas in seasons:

        height1 = []
        height2 = []
        y_pos = np.arange(len(datasets))
        width = 0.35

        fig, ax1 = plt.subplots()

        for expt in datasets:
            mflux = ds_list[expt]["mflux"].sel(season_number=seas).values.item()
            sp = ds_list[expt]["psl"].sel(season_number=seas).values.item()
            height1.append(mflux)
            height2.append(sp)

        ax1.bar(y_pos - width / 2, height1, width, color="blue")
        ax1.set_ylim(0, max(height1) + 5.0)
        ax1.set_ylabel(
            "Moisture Flux CA Western Boundary (g.Kg-1 m.s-1)",
            fontweight="bold",
            color="blue",
        )
        ax1.set_title(seasons[seas])

        ax2 = ax1.twinx()
        ax2.bar(y_pos + width / 2, height2, width, color="red")
        ax2.set_ylabel("Mean SAH (hPa)", fontweight="bold", color="red")
        ax2.set_ylim(1010, max(height2) + 5.0)

        # Create names on the x-axis
        plt.xticks(y_pos)
        xticklabels = datasets
        ax1.set_xticklabels(xticklabels, rotation="vertical")

        plt.savefig(
            config["plot_dir"] + "/sah_mflx_" + seasons[seas] + "_plot.png",
            bbox_inches="tight",
            dpi=100,
        )


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_data(config)
        data_for_plotting = calculations(data_for_plotting)
        plot_figure1(data_for_plotting)
        plot_figure2(data_for_plotting)
