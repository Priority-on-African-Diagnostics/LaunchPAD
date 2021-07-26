"""
Diagnostic script for LaunchPAD AEJ.
"""

# to manipulate iris cubes
import iris
import matplotlib.pyplot as plt

# import internal esmvaltool modules here
from esmvaltool.diag_scripts.shared import group_metadata, run_diagnostic
from esmvalcore.preprocessor import area_statistics


def process_for_plotting(cfg):
    """
    Arrange data to be ready for plotting. Target is lists of cubes
    (uN, uS, T)

    Arguments:
        cfg - nested dictionary of metadata

    Returns:
        cube lists ready for plotting

    """
    # assemble the data dictionary keyed by dataset name
    # first organise by variable
    variables = group_metadata(cfg["input_data"].values(), "variable")

    return variables


if __name__ == "__main__":
    # always use run_diagnostic() to get the config (the preprocessor
    # nested dictionary holding all the needed information)
    with run_diagnostic() as config:
        # list here the functions that need to run
        process_for_plotting(config)
