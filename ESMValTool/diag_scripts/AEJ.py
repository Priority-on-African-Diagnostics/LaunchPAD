"""
Diagnostic script for LaunchPAD AEJ.
"""

# to manipulate iris cubes
import iris
import xarray as xr

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic
from esmvalcore.preprocessor import climate_statistics, zonal_statistics


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


def calc_for_plotting(ds_list):
    """Calculation of AEJ components for plotting.

    Args:
        ds_list ([type]): [description]

    Returns:
        Dictionary of data ready for plotting
    """
    for ds in ds_list:
        # calc jet intensity and jet latitudes
        ds_list[ds]["N_lat"], ds_list[ds]["N_intensity"] = find_lat_int(
            ds_list[ds]["uN"], ds
        )
        ds_list[ds]["S_lat"], ds_list[ds]["S_intensity"] = find_lat_int(
            ds_list[ds]["uS"], ds
        )

    return ds_list


def find_lat_int(cube, ds):

    thresh = -6.0

    lat = []
    xr_cube = xr.DataArray.from_iris(cube)
    if ds in ["ERA5", "ERA-Interim"]:
        xr_min = xr_cube.min(dim="latitude")
    else:
        xr_min = xr_cube.min(dim="lat")
    xr_min = xr_min.where(xr_min < thresh)
    for m in xr_cube.month_number:
        try:
            if ds in ["ERA5", "ERA-Interim"]:
                lat.append(
                    xr_cube.latitude.where(
                        xr_cube.sel(month_number=m) == xr_min.sel(month_number=m),
                        drop=True,
                    ).values.item()
                )
            else:
                lat.append(
                    xr_cube.lat.where(
                        xr_cube.sel(month_number=m) == xr_min.sel(month_number=m),
                        drop=True,
                    ).values.item()
                )
        except:
            lat.append(np.nan)

    cube = xr.DataArray.to_iris(xr_min)

    return lat, cube


def plot_TG(ds_list):
    """Produce figure 1 plot

    Args:
        ds_list ([dict]): Dictionary of datasets and variables prepared by 
        prep_for_plotting function
    """

    cmap = cm.get_cmap("coolwarm")
    clevs = np.arange(-5, 6, 1)
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

    for ds in ds_list:
        LN = ds_list[ds]["N_lat"]
        LS = ds_list[ds]["S_lat"]

        fig, ax = plt.subplots()
        nameOfPlot = (
            ds + " African Easterly Jet (Giresse Turin) Temperature Gradient (K/m)"
        )
        plt.suptitle(nameOfPlot, fontsize=12)

        cubeT = ds_list[ds]["ta"]

        cubeT.data = np.gradient(cubeT.data, axis=1)
        cubeT.data = cubeT.data * (-12.5)

        x = np.arange(0, 12, 1)
        y = cubeT.coord("latitude").points
        xm, ym = np.meshgrid(x, y)

        linethick = 2.5
        plt.plot(LN, color="black", lw=linethick, zorder=2)
        plt.plot(LS, color="red", lw=linethick, zorder=2)

        plt.ylabel("Latitude (Degrees)", fontsize=10)
        ax.set_xticks(np.arange(12))
        ax.set_xticklabels(mon_names, rotation=45)
        # plt.xticks(ticks=np.arange(12), labels=mon_names, rotation=45)

        cf = plt.contourf(
            xm, ym, cubeT.data.T, clevs, cmap=cmap, extend="both", zorder=1
        )
        colorbar_axes = plt.gcf().add_axes([0.91, 0.15, 0.02, 0.65])
        plt.colorbar(cf, colorbar_axes, orientation="vertical")

        plt.savefig(
            config["plot_dir"] + "TG_plot_" + ds + "_AEJ_plot.png",
            bbox_inches="tight",
            dpi=100,
        )


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        data_for_plotting = prep_data(config)
        data_for_plotting = calc_for_plotting(data_for_plotting)
        plot_TG(data_for_plotting)
