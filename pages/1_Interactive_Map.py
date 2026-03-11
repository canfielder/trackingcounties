import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

import json
import streamlit as st
import folium
import folium.plugins as plugins
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


def format_date(date, print_fmt="%B %d, %Y"):
    return date.strftime(print_fmt)


def define_tooltip(row):
    date_str = format_date(row["date"]) if row["visited"] == 1 else ""
    return (
        f"State: {row['state_name']}<br>"
        f"County: {row['name']}<br>"
        f"FIPS: {row['geoid']}<br>"
        f"Date Visited: {date_str}"
    )


config_path = PROJECT_ROOT / "config.json"
with open(config_path, "r") as f:
    CONFIG = json.load(f)

st.header("Interactive Map")

with st.spinner("Loading data..."):
    df, counties, states = load_data()

with st.spinner("Building map..."):
    m = folium.Map(location=[39.8283, -98.5795], zoom_start=5, tiles="OpenStreetMap")

    for _, row in states.iterrows():
        style = (
            CONFIG["style"]["state"]["visited"]
            if row["visited"] == 1
            else CONFIG["style"]["state"]["not_visited"]
        )
        folium.GeoJson(
            row["geometry"],
            style_function=lambda x, style=style: style,
        ).add_to(m)

    for _, row in counties.iterrows():
        style = (
            CONFIG["style"]["county"]["visited"]
            if row["visited"] == 1
            else CONFIG["style"]["county"]["not_visited"]
        )
        tooltip = define_tooltip(row)
        folium.GeoJson(
            row["geometry"],
            style_function=lambda x, style=style: style,
            tooltip=tooltip,
        ).add_to(m)

    plugins.Fullscreen(position="topleft").add_to(m)

with st.spinner("Rendering map..."):
    stf.st_folium(
        m,
        width=CONFIG["interactive_map"]["width"],
        height=CONFIG["interactive_map"]["height"],
        returned_objects=[],
    )
