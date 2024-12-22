# ---------------------------------------------------------------------------- #
# IMPORT #

from .config import EPSG_CODE, NON_CONTIGUOUS_CODES, PLOT_PARAMS
from .scripts.data import import_data 
from .scripts.plotting import generate_plot_data, Plot
from .scripts.processing import process_data


# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #

def tracking_counties(print_plot = True, save_plot = True):
    # Import datasets
    df_visit_county, gdf_county, gdf_state = import_data()

    # Process Datasets
    gdf_county, gdf_state = process_data(
            df_visited = df_visit_county,
            gdf_county = gdf_county,
            gdf_state  = gdf_state
        )

    # Convert datasets to plot specific data
    dct_plot = generate_plot_data(
        gdf_county, 
        gdf_state,
        non_contiguous_codes = NON_CONTIGUOUS_CODES,
        epsg_code            = EPSG_CODE
        )


    # Initialize plotter
    plotter = Plot(
        plot_tables = dct_plot,
        plot_params = PLOT_PARAMS
    )

    # Generate plots
    for plot_label in dct_plot['county'].keys():

        plotter(
            plot_label = plot_label,
            save_plot  = save_plot,
            print_plot = print_plot
            )