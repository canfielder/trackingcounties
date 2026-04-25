import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "src"))

import io

import streamlit as st

from config import EPSG_CODE, NON_CONTIGUOUS_CODES, PLOT_PARAMS, PLOT_PREVIEW_DPI
from scripts.data import import_data
from scripts.plotting import Plot, generate_plot_data
from scripts.processing import process_data

st.set_page_config(page_title="Static Plots", layout="wide")

PLOT_LABELS = {
    "us_inset": "United States",
    "north_carolina": "North Carolina",
    "north_carolina_w_adjacent_states": "North Carolina & Adjacent States",
}


@st.cache_data
def load_data():
    df, counties, states = import_data()
    counties, states = process_data(
        df_visited=df,
        gdf_county=counties,
        gdf_state=states,
    )
    return df, counties, states


@st.cache_data
def load_plot_data(_counties, _states):
    return generate_plot_data(
        _counties,
        _states,
        non_contiguous_codes=NON_CONTIGUOUS_CODES,
        epsg_code=EPSG_CODE,
    )


def render_plot_to_bytes(plotter, plot_label):
    p = plotter.generate_plot(plot_label=plot_label)
    buf = io.BytesIO()
    p.save(
        filename=buf,
        format="png",
        height=PLOT_PARAMS["dimensions"]["height"][plot_label],
        width=PLOT_PARAMS["dimensions"]["width"][plot_label],
        units="in",
        dpi=PLOT_PREVIEW_DPI,
    )
    buf.seek(0)
    return buf


df, counties, states = load_data()
dct_plot = load_plot_data(counties, states)
plotter = Plot(plot_tables=dct_plot, plot_params=PLOT_PARAMS)

st.header("Static Plots")
st.caption("Export any plot as a PNG using the download button beneath it.")

for plot_label, plot_title in PLOT_LABELS.items():
    st.subheader(plot_title)

    with st.spinner(f"Rendering {plot_title}..."):
        buf = render_plot_to_bytes(plotter, plot_label)

    st.image(buf, use_container_width=True)

    st.download_button(
        label=f"⬇ Download {plot_title}",
        data=buf,
        file_name=f"{plot_label}.png",
        mime="image/png",
        key=plot_label,
    )

    st.divider()
