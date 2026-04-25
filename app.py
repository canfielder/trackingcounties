import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

import pandas as pd
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


def build_state_progress(df: pd.DataFrame) -> pd.DataFrame:
    """Build a per-state visited/total/pct summary, sorted by completion."""
    df_progress = (
        df.groupby("state_name")
        .agg(
            visited=("visited", "sum"),
            total=("visited", "count"),
        )
        .reset_index()
    )
    df_progress["pct"] = (df_progress["visited"] / df_progress["total"]) * 100
    return df_progress.sort_values("pct", ascending=False).reset_index(drop=True)


df, counties, states = load_data()

visited_counties = int(df["visited"].sum())
total_counties = len(df)
visited_states = int((df.groupby("state_name")["visited"].sum() > 0).sum())
total_states = df["state_name"].nunique()

st.title("Counties Visited")

# -------------------------------------------------------------------------------- #
# 📊 TOP-LEVEL METRICS
# -------------------------------------------------------------------------------- #
m1, m2, m3 = st.columns(3)
m1.metric("Counties Visited", f"{visited_counties:,}", f"of {total_counties:,}")
m2.metric("States Visited", f"{visited_states:,}", f"of {total_states:,}")
m3.metric(
    "Overall Progress",
    f"{visited_counties / total_counties:.1%}",
)

st.divider()

# -------------------------------------------------------------------------------- #
# 🗺️ PER-STATE PROGRESS
# -------------------------------------------------------------------------------- #
st.subheader("Progress by State")

df_state_progress = build_state_progress(df)

st.dataframe(
    df_state_progress,
    column_config={
        "state_name": st.column_config.TextColumn("State"),
        "visited": st.column_config.NumberColumn("Visited"),
        "total": st.column_config.NumberColumn("Total"),
        "pct": st.column_config.ProgressColumn(
            "Progress",
            format="%.0f%%",
            min_value=0,
            max_value=100,
        ),
    },
    hide_index=True,
    use_container_width=True,
)

# -------------------------------------------------------------------------------- #
# 📋 SIDEBAR
# -------------------------------------------------------------------------------- #
st.sidebar.header("Visit Stats")
st.sidebar.metric("Counties", f"{visited_counties:,} / {total_counties:,}")
st.sidebar.metric("States", f"{visited_states:,}")
