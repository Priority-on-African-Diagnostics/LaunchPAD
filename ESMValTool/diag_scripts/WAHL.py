"""
Diagnostic script for LaunchPAD WAHL.
"""

# to manipulate iris cubes
import iris
import math

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import cartopy.feature as cfeature
import cartopy.crs as ccrs

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic


obs_list = ["ERA5", "MERRA2"]
mon_names = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


def prep_data(cfg):
    """
    Arrange data to be ready for plotting.
    Return a dictionary of the prepped data

    Arguments:
        cfg - nested dictionary of metadata

    Returns:
        dictionary of cubes
    """
    # organise data by dataset, then variable
    datasets = group_metadata(cfg["input_data"].values(), "dataset")
    prepped_data = {}

    # process
    for d in datasets:
        # load data
        data = iris.load_cube(datasets[d][0]["filename"])
        if d in ["ERA-Interim", "ERA5"]:
            data = data / 9.80665

        p700 = data.extract(iris.Constraint(pressure_level=70000))
        p925 = data.extract(iris.Constraint(pressure_level=92500))

        data = p700 - p925
        prepped_data[d] = data

    return prepped_data


def bestfit_colrow(total=1):

    if (total / 3.0) > 2:
        cols = 3
        rows = math.ceil(total / 3.0)
    elif (total / 2.0) > 1:
        cols = 2
        rows = math.ceil(total / 2.0)
    else:
        cols = 1
        rows = 1

    return cols, rows


def plot_WAHL(ds_data, expt):

    Cube0 = ds_data

    cmap_zg = cm.get_cmap("jet", 30)
    cmap_hb = cm.get_cmap("jet", 8)
    cmap_pr = cm.get_cmap("Blues", 150)

    arr_zg = []
    arr_hb = []
    arr_pr = []

    arr_zg.append("#ffffff")
    arr_zg.append("#ffffff")
    arr_hb.append("#ffffff")
    arr_pr.append("#ffffff")

    for i in range(cmap_zg.N):
        rgb = cmap_zg(i)[:3]
        arr_zg.append(matplotlib.colors.rgb2hex(rgb))

    for i in range(cmap_hb.N):
        rgb = cmap_hb(i)[:3]
        arr_hb.append(matplotlib.colors.rgb2hex(rgb))

    for i in range(cmap_pr.N):
        rgb = cmap_pr(i)[:3]
        arr_pr.append(matplotlib.colors.rgb2hex(rgb))

    plt.figure(figsize=(6, 6))
    clevs_zg = np.arange(0, 30, 1)
    # clevs_pr = np.arange(0, 150, 1)
    # clevs_hb = np.arange(0, 9, 1)

    cols, rows = bestfit_colrow(12)
    lon_step = 10
    lat_step = 10

    col_no = 0
    row_no = 0

    vari_line = "WAHL"
    si_line = "m"

    fig, axs = plt.subplots(
        cols, rows, subplot_kw={"projection": ccrs.PlateCarree()}, figsize=(10, 10)
    )
    fig.suptitle(vari_line + " @ 0600 for " + expt + " 1983-2012 " + si_line)

    for counter, Cube1 in enumerate(Cube0.slices(["latitude", "longitude"])):

        # calculate 90th% over area (i.e. per month)
        Cube90 = Cube1.collapsed(
            ["longitude", "latitude"], iris.analysis.PERCENTILE, percent=[90]
        )
        # subtract from LLAT
        Cube1 = iris.analysis.maths.subtract(Cube1, Cube90[0])
        # threshold of 2 m
        Cube1.data = np.ma.masked_where(Cube1.data <= 2, Cube1.data)

        month = mon_names[Cube1.coord("month").points[0]]

        x = Cube1.coord("longitude").points
        y = Cube1.coord("latitude").points

        xm, ym = np.meshgrid(x, y)

        # plt.subplot(3,4,counter+1)
        current_ax = axs[col_no, row_no]

        cf = current_ax.contourf(
            xm, ym, np.array(Cube1.data), clevs_zg, colors=arr_zg, extend="both"
        )

        extent = [-25, 30, -10, 40]

        if col_no == 2:
            axs[col_no, row_no].set_xlabel("Longitude (°)", labelpad=20)
        if row_no == 0:
            axs[col_no, row_no].set_ylabel("Latitude (°)", labelpad=20)

        meridians = np.arange(extent[0], extent[1] + lon_step, lon_step)
        parallels = np.arange(extent[2], extent[3] + lat_step, lat_step)
        axs[col_no, row_no].grid()
        axs[col_no, row_no].set_xlim([extent[0], extent[1]])
        axs[col_no, row_no].set_ylim([extent[2], extent[3]])

        axs[col_no, row_no].set_yticks(parallels)
        axs[col_no, row_no].set_yticklabels(parallels)
        axs[col_no, row_no].set_xticks(meridians)
        axs[col_no, row_no].set_xticklabels(meridians)
        axs[col_no, row_no].add_feature(cfeature.BORDERS)
        axs[col_no, row_no].add_feature(cfeature.COASTLINE)
        # axs[col_no, row_no].add_feature(cfeature.LAND, facecolor='#808080', zorder=1)
        axs[col_no, row_no].set_extent((-25, 30, -10, 40))

        title = month
        axs[col_no, row_no].title.set_text(title)

        row_no = row_no + 1
        if row_no == rows:
            row_no = 0
            col_no = col_no + 1

    colorbar_axes = plt.gcf().add_axes([0.25, 0.03, 0.5, 0.025])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation="horizontal")
    # plt.suptitle()

    plt.savefig(
        config["plot_dir"] + "/" + expt + "_" + vari_line + "_plot.png",
        bbox_inches="tight",
        dpi=100,
    )


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_data(config)
        for ds in data_for_plotting.keys():
            plot_WAHL(data_for_plotting[ds], ds)
