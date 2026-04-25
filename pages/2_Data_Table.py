import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

import streamlit as st

from config import NA_DATE
from scripts.data import import_data
from scripts.processing import process_data

st.set_page_config(page_title="Data Table", layout="wide")


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

st.header("Data Table")

# --- Filters ---
col_state, col_visited, col_year = st.columns(3)

with col_state:
    all_states = sorted(df["state_name"].unique())
    selected_states = st.multiselect("Filter by state", all_states, default=[])

with col_visited:
    visited_filter = st.radio(
        "Visit status",
        options=["All", "Visited", "Not visited"],
        horizontal=True,
    )

with col_year:
    visit_years = sorted(df[df["visited"] == 1]["date"].apply(lambda d: d.year).unique())
    year_range = st.slider(
        "Year visited",
        min_value=visit_years[0],
        max_value=visit_years[-1],
        value=(visit_years[0], visit_years[-1]),
        disabled=(visited_filter == "Not visited"),
    )

# --- Apply filters ---
display_df = df.copy()

if selected_states:
    display_df = display_df[display_df["state_name"].isin(selected_states)]

if visited_filter == "Visited":
    display_df = display_df[display_df["visited"] == 1]
elif visited_filter == "Not visited":
    display_df = display_df[display_df["visited"] == 0]

if visited_filter == "Visited":
    year = display_df["date"].apply(lambda d: d.year)
    display_df = display_df[year.between(int(year_range[0]), int(year_range[1]))]

# Sort: visited first, then most recent → oldest; unvisited fall to the bottom
display_df = display_df.sort_values(
    ["visited", "date"], ascending=[False, False]
).reset_index(drop=True)

# --- Format for display ---
display_df = display_df[["state_name", "county_name", "geoid", "date", "notes"]].copy()
display_df["date"] = display_df["date"].apply(
    lambda d: d.strftime("%B %d, %Y") if d != NA_DATE else ""
)
display_df.columns = ["State", "County", "FIPS", "Date Visited", "Notes"]

# --- Metrics ---
m1, m2, m3 = st.columns(3)
m1.metric("Showing", f"{len(display_df):,}")
m2.metric("Visited (shown)", f"{(display_df['Date Visited'] != '').sum():,}")
m3.metric("Not visited (shown)", f"{(display_df['Date Visited'] == '').sum():,}")

st.dataframe(display_df, use_container_width=True, hide_index=True)
