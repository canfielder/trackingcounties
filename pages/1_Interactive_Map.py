import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

import json

import folium
import folium.plugins as plugins
import geopandas as gpd
import streamlit as st
import streamlit_folium as stf

from paths import PROJECT_ROOT
from scripts.data import import_data
from scripts.processing import process_data

st.set_page_config(page_title="Interactive Map", layout="wide")


@st.cache_data
def load_data():
    df, counties, states = import_data()
    counties, states = process_data(
        df_visited=df,
        gdf_county=counties,
        gdf_state=states,
    )
    return df, counties, states


def format_date(date, print_fmt: str = "%B %d, %Y") -> str:
    """Format a datetime as a human-readable string."""
    return date.strftime(print_fmt)


def _prepare_states(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Subset state GeoDataFrame to columns needed by folium."""
    out = gdf[["geometry", "visited"]].copy()
    out["visited"] = out["visited"].astype(int)
    return out


def _prepare_counties(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Subset county GeoDataFrame and pre-format dates for folium tooltips."""
    cols = ["geometry", "visited", "state_name", "name", "geoid", "date"]
    out = gdf[cols].copy()
    out["visited"] = out["visited"].astype(int)
    out["date_str"] = out.apply(
        lambda row: format_date(row["date"]) if row["visited"] == 1 else "",
        axis=1,
    )
    return out.drop(columns=["date"])


config_path = PROJECT_ROOT / "config.json"
with open(config_path, "r") as f:
    CONFIG = json.load(f)

st.header("Interactive Map")

with st.spinner("Loading data..."):
    df, counties, states = load_data()

with st.spinner("Building map..."):
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=5, tiles="OpenStreetMap")

    state_styles = CONFIG["style"]["state"]
    county_styles = CONFIG["style"]["county"]

    folium.GeoJson(
        _prepare_states(states),
        style_function=lambda f: (
            state_styles["visited"]
            if f["properties"]["visited"] == 1
            else state_styles["not_visited"]
        ),
    ).add_to(m)

    folium.GeoJson(
        _prepare_counties(counties),
        style_function=lambda f: (
            county_styles["visited"]
            if f["properties"]["visited"] == 1
            else county_styles["not_visited"]
        ),
        tooltip=folium.GeoJsonTooltip(
            fields=["state_name", "name", "geoid", "date_str"],
            aliases=["State:", "County:", "FIPS:", "Date Visited:"],
        ),
    ).add_to(m)

    plugins.Fullscreen(position="topleft").add_to(m)

with st.spinner("Rendering map..."):
    stf.st_folium(
        m,
        width=CONFIG["interactive_map"]["width"],
        height=CONFIG["interactive_map"]["height"],
        returned_objects=[],
    )
