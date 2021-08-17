"""
Diagnostic script for LaunchPAD CAF
"""

# to manipulate iris cubes
import iris
import iris.plot as iplt
import iris.analysis.stats
import cartopy.feature as cfeature
import cartopy.crs as crs

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import numpy as np
from numpy.polynomial.polynomial import polyfit
from scipy.stats import spearmanr
import calendar

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic
from esmvalcore.preprocessor import regrid


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

            if data.ndim > 1:
                # ensure no seam in the middle of our data
                data = data.intersection(longitude=(-180, 180))

            prepped_data[d][v] = data

    return prepped_data


def calc_bias(dataset, obs):
    dataset = regrid(dataset, obs, "linear")
    bias = dataset - obs

    return bias


def plot_CAF(data, expt):

    clevs = np.arange(-3, 3.5, 0.5)

    for i, bias in enumerate(data.slices_over("month_number")):
        plt.figure(figsize=(5, 4))

        plt.subplot(2, 2, i + 1)
        ax = plt.axes(projection=crs.PlateCarree(0))
        cf = iplt.contourf(bias, clevs, cmap="PRGn", extend="both")
        plt.gca().coastlines()
        plt.gca().add_feature(cfeature.BORDERS, linewidth=0.2)
        r = config["region_extent"]
        extent = (
            r["start_longitude"],
            r["end_longitude"],
            r["start_latitude"] + 1,
            r["end_latitude"] - 1,
        )
        plt.gca().set_extent(extent)
        r = config["region_caf"]
        plt.gca().add_patch(
            Rectangle(
                (r["start_longitude"], r["start_latitude"]),
                r["end_longitude"] - r["start_longitude"],
                r["end_latitude"] - r["start_latitude"],
                linewidth=1,
                edgecolor="yellow",
                facecolor="none",
            )
        )
        r = config["region_pr"]
        plt.gca().add_patch(
            Rectangle(
                (r["start_longitude"], r["start_latitude"]),
                r["end_longitude"] - r["start_longitude"],
                r["end_latitude"] - r["start_latitude"],
                linewidth=1,
                edgecolor="blue",
                facecolor="none",
            )
        )
        gl = ax.gridlines(
            crs=crs.PlateCarree(),
            draw_labels=True,
            linewidth=2,
            color="gray",
            alpha=0.5,
            linestyle="--",
        )
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False

        mon = calendar.month_abbr[bias.coord("month_number").points[0]]
        plt.title(mon)

        colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
        colorbar = plt.colorbar(cf, colorbar_axes, orientation="vertical")
        colorbar.set_label("m/s")
        plt.suptitle(expt + " 700 hPa CAF bias")

        plt.savefig(
            config["plot_dir"] + "/" + expt + "_" + mon + "_CAF_plot.png",
            bbox_inches="tight",
            dpi=200,
        )
        plt.close()


def plot_scatter(data, mon):

    shape = [
        ".",
        "o",
        "v",
        "^",
        "<",
        "8",
        "s",
        ">",
        "p",
        "P",
        "*",
        "h",
        "+",
        "X",
        "d",
        "x",
        "D",
        "H",
        "3",
        "1",
        "o",
        "v",
        "^",
        "<",
        ".",
        "o",
        "v",
        "^",
        "<",
        "8",
        "s",
        ">",
        "p",
        "P",
        "*",
        "h",
        "+",
        "X",
        "d",
        "x",
        "D",
        "H",
        "3",
        "1",
        "o",
        "v",
        "^",
        "<",
    ]
    colors = plt.matplotlib.cm.viridis(np.linspace(0, 1, len(data.keys())))
    m_con = iris.Constraint(month_number=mon)

    pr_list = []
    caf_list = []
    for i, expt in enumerate(data.keys()):
        caf_expt = data[expt]["caf"].extract(m_con)
        pr_expt = data[expt]["pr"].extract(m_con)

        if expt == "ERA5":
            plt.scatter(
                pr_expt.data,
                caf_expt.data,
                color=["coral"],
                s=[90],
                marker=shape[i],
                label=expt,
            )
        else:
            plt.scatter(
                pr_expt.data,
                caf_expt.data,
                color=colors[i],
                s=[50],
                marker=shape[i],
                label=expt,
            )
            pr_list.append(pr_expt.data)
            caf_list.append(caf_expt.data)

    correl = spearmanr(pr_list, caf_list)
    print(correl)
    sc = correl[0]

    sy = caf_list
    sx = pr_list
    z = polyfit(sx, sy, 1)
    p = np.poly1d([z[1], z[0]])
    sx = np.arange(
        np.min(sx),
        np.max(sx) + (np.max(sx) - np.min(sx)) / 10,
        (np.max(sx) - np.min(sx)) / 10,
    )
    plt.plot(
        sx, p(sx), "--", color="black", label="r=" + "{:<.3f}".format(sc) + ", p<0.01"
    )

    plt.legend(bbox_to_anchor=(1.1, 1.05), ncol=2)
    # plt.ylim(-9,-1.8)
    # plt.xlim(0.5,8.5)
    plt.xlabel("pr (mm/day)")
    plt.ylabel("CAF zonal wind (m/s)")
    plt.title(calendar.month_abbr[mon])

    # if correl[1] <= 0.01:
    plt.savefig(
        config["plot_dir"] + "/ALL_SCATTER_" + calendar.month_abbr[mon] + "_CAF.png",
        bbox_inches="tight",
        dpi=200,
    )
    # plt.show()
    plt.close()


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        input_data = prep_data(config)
        for ds in input_data.keys():
            # calc bias
            if ds != "ERA5":
                input_data[ds]["bias"] = calc_bias(
                    input_data[ds]["ua"], input_data["ERA5"]["ua"]
                )

                plot_CAF(input_data[ds]["bias"], ds)

        months = input_data[ds]["caf"].coord("month_number").points
        for m in months:
            plot_scatter(input_data, m)
