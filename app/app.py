###############################################################################
# IMPORT #
import folium
import folium.plugins as plugins
import geopandas as gpd
import hashlib
import json
import streamlit as st
import streamlit_folium as stf

from pathlib import Path

from tracking_counties.config import EPSG_CODE, NON_CONTIGUOUS_CODES, PLOT_PARAMS, ROOT_DIR
from tracking_counties.scripts.data import import_data
from tracking_counties.scripts.plotting import generate_plot_data, Plot
from tracking_counties.scripts.processing import process_data

# Set page configuraotin
st.set_page_config(
    page_title = "Tracking Counties",
    layout = "wide"
    )

###############################################################################
# FUNCTIONS #
def hash_file_content(url):
    """Compute the hash of file content from a URL."""
    gdf = gpd.read_file(url)
    content_hash = hashlib.sha256(gdf.to_json().encode()).hexdigest()
    return gdf, content_hash


def format_date(date, print_fmt = "%B %d, %Y"):
    return date.strftime(print_fmt)


def define_tooltip(row):
    # Reformat date string
    if row['visited'] == 1:

        date_format_str = format_date(row['date'])
    
    else:
        date_format_str = ''
    
    tooltip = (
        f"State: {row['state_name']}<br>"
        f"County: {row['name']}<br>"
        f"FIPS: {row['geoid']}<br>"
        f"Date Visited: {date_format_str}"
    )

    return tooltip


###############################################################################
# DATA #
# Get the absolute path to the config file relative to this script
config_file_path = ROOT_DIR / "app" / "config.json"

with open(config_file_path, "r") as f:
    CONFIG = json.load(f)


# State and county data
df, counties, states = import_data()

# Process Datasets
counties, states = process_data(
        df_visited = df,
        gdf_county = counties,
        gdf_state  = states
    )

# Convert datasets to plot specific data
dct_plot = generate_plot_data(
    counties, 
    states,
    non_contiguous_codes = NON_CONTIGUOUS_CODES,
    epsg_code            = EPSG_CODE
    )

# Initialize plotter
plotter = Plot(
    plot_tables = dct_plot,
    plot_params = PLOT_PARAMS
)


###############################################################################
# APP #
# Streamlit app title
st.title("Counties Visited")

# Sidebar for file data
st.sidebar.header("Visit Stats")

# Count counties and states visited
visited_counties = df[df["visited"] == 1].shape[0]
visited_states = df[df['visited'] == 1]['state'].nunique()

st.sidebar.write(f"Counties: {visited_counties:,}")
st.sidebar.write(f"States: {visited_states:,}")

# Main tab for interactive map
tab1, tab2 = st.tabs(["Interactive Map", "Static Plots"])

# Tab 1: Interactive Map ----------------------------------------------
with tab1:
    st.header("Interactive Map")

    # Create a Folium map
    m = folium.Map(
        location = [
            39.8283, 
            -98.5795
            ], 
        zoom_start = 5, 
        tiles = "OpenStreetMap"
        )

    # State Plot --------------------------------------------
    for _, row in states.iterrows():
        # Select style settings
        style = CONFIG["style"]["state"]["visited"] if row["visited"] == 1 else CONFIG["style"]["state"]["not_visited"]

        # Add state date to folium map
        folium.GeoJson(
            row["geometry"],
            style_function = lambda x, 
            style = style: style,
        ).add_to(m)

    # County Plot -------------------------------------------
    for _, row in counties.iterrows():
        # Access sytle settings
        style = CONFIG["style"]["county"]["visited"] if row["visited"] == 1 else CONFIG["style"]["county"]["not_visited"]

        # Define tooltip for county
        tooltip = define_tooltip(row)

        # Add county date to folium map
        folium.GeoJson(
            row["geometry"],
            style_function = lambda x, 
            style = style: style,
            tooltip = tooltip,
        ).add_to(m)

    # Render the map
    plugins.Fullscreen(position="topleft").add_to(m)
    stf.st_folium(
        m, 
        width = CONFIG['interactive_map']['width'], 
        height = CONFIG['interactive_map']['height'],
        returned_objects = []
        )

# Tab 2: Static Plots -------------------------------------------------
with tab2:
    st.header("Static Plots")

    # for plot_label in dct_plot['county'].keys():
    #     p = plotter.generate_plot(plot_label = plot_label)
    #     st.pyplot(p)
