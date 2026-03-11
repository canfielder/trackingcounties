import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

import streamlit as st

from scripts.data import import_data
from scripts.processing import process_data

st.set_page_config(
    page_title="Tracking Counties",
    layout="wide",
)


@st.cache_data
def load_data():
    df, counties, states = import_data()
    counties, states = process_data(
        df_visited=df,
        gdf_county=counties,
        gdf_state=states,
    )
    return df, counties, states


df, counties, states = load_data()

visited_counties = df[df["visited"] == 1].shape[0]
visited_states = df[df["visited"] == 1]["state"].nunique()
total_counties = df.shape[0]

st.title("Counties Visited")

st.sidebar.header("Visit Stats")
st.sidebar.metric("Counties", f"{visited_counties:,} / {total_counties:,}")
st.sidebar.metric("States", f"{visited_states:,}")
