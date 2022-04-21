"""
Diagnostic script for LaunchPAD Turkana Jet.
"""

# to manipulate iris cubes
import iris
import xarray as xr

import matplotlib.pyplot as plt
import iris.plot as iplt
import cartopy.feature as cfeature

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic
from esmvalcore.preprocessor import climate_statistics

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
    Arrange data to be ready for further calculations.
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
            prepped_data[d][v] = data

    return prepped_data


def calculations(ds_list):
    """Further calculations of pre processed data

    Args:
        ds_list (dict): Processed dictionary of data
    Returns:
        dictionary of data ready for plotting
    """
    # loop over datasets
    for d in ds_list.keys():
        ua = ds_list[d]["ua"]
        va = ds_list[d]["va"]
        hus = ds_list[d]["hus"]

        # calculate scalar wind
        windspeed = (ua ** 2 + va ** 2) ** 0.5

        # calculate mflux (conv hus to g/kg)
        mflx = windspeed * hus * 1000

        # calculate climatology
        ua_clim = climate_statistics(ua, "mean", "month")
        va_clim = climate_statistics(va, "mean", "month")
        mflux_clim = climate_statistics(mflx, "mean", "month")

        # mask winds
        thresh = 5

        ua_clim = xr.DataArray.from_iris(ua_clim)
        va_clim = xr.DataArray.from_iris(va_clim)

        # windspeed of masked clim data
        windspeed = (ua_clim ** 2 + va_clim ** 2) ** 0.5

        ua_clim = ua_clim.where(windspeed > thresh)
        va_clim = va_clim.where(windspeed > thresh)

        ua_clim = ua_clim.to_iris()
        va_clim = va_clim.to_iris()

        # add data to dictionary
        ds_list[d]["ua_clim"] = ua_clim
        ds_list[d]["va_clim"] = va_clim
        ds_list[d]["mflux_clim"] = mflux_clim

    return ds_list


def plot_TJ1(ds_data, ds):

    ua = ds_data["ua_clim"]
    va = ds_data["va_clim"]
    mflx = ds_data["mflux_clim"]

    plt.figure(figsize=(6, 6))
    clevs = np.arange(0, 102, 1)

    for mon in range(1, 13):

        ua_mon = ua.extract(iris.Constraint(month_number=mon))
        va_mon = va.extract(iris.Constraint(month_number=mon))
        mflx_mon = mflx.extract(iris.Constraint(month_number=mon))

        x = ua_mon.coord("longitude").points
        y = ua_mon.coord("latitude").points

        xm, ym = np.meshgrid(x, y)
        u = ua_mon.data
        v = va_mon.data

        xskip = 4
        yskip = 4
        scale_fact = 10
        arrow_scale = scale_fact * xskip * 1.5

        plt.subplot(3, 4, mon)
        cf = iplt.contourf(mflx_mon, clevs, cmap="coolwarm", extend="both")
        qv = plt.quiver(
            xm[::xskip, ::xskip],
            ym[::yskip, ::yskip],
            u[::xskip, ::xskip],
            v[::yskip, ::yskip],
            pivot="middle",
            units="inches",
            minlength=0,
            scale=arrow_scale,
            width=0.0075,
        )
        plt.quiverkey(
            qv,
            0.9,
            1.05,
            scale_fact,
            r"$10 \frac{m}{s}$",
            labelpos="E",
            fontproperties={"size": 7},
        )
        plt.gca().coastlines()
        plt.gca().add_feature(cfeature.BORDERS, linewidth=0.2)
        plt.gca().set_extent((32, 43, -5, 6))
        plt.title(mon_names[mon])

    colorbar_axes = plt.gcf().add_axes([0.95, 0.3, 0.025, 0.4])
    colorbar = plt.colorbar(cf, colorbar_axes, orientation="vertical")
    colorbar.set_label("$\overline{qV} (g/Kg/ms^{-1}$)")
    plt.suptitle(ds + " TJ1 ")

    plt.savefig(
        config["plot_dir"] + "/" + ds + "_TJ_plot.png", bbox_inches="tight", dpi=200
    )


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_data(config)
        data_for_plotting = calculations(data_for_plotting)
        for ds in data_for_plotting.keys():
            plot_TJ1(data_for_plotting[ds], ds)
