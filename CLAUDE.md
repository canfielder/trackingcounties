# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
make launch        # Start Streamlit app at localhost:8501 (default target)
make sync          # Install/sync all dependencies via uv
make lint          # Run Ruff linter on src/
make format        # Auto-format with Black
make clean         # Remove build artifacts

# Regenerate all static plot PNGs
PYTHONPATH=src uv run python src/generate_plots.py
```

The app requires `PYTHONPATH=src` at runtime — `make launch` handles this. All `uv run` commands should be prefixed the same way when running scripts directly.

## Architecture

**Data flow:**
```
data/tables/list_of_counties_active.csv  ←  source of truth for visits
        ↓
src/scripts/data.py        import_data()  — loads CSV + pygris shapefiles
        ↓
src/scripts/processing.py  process_data() — joins visits onto county/state GeoDataFrames
        ↓
    ┌───────────────────────────────────┐
    │  app.py + pages/                  │  Streamlit UI (4 pages)
    │  src/generate_plots.py            │  Standalone PNG generation
    └───────────────────────────────────┘
```

**Pages:**
- `app.py` — dashboard with visit counts, loads and caches data for all pages via `@st.cache_data`
- `pages/1_Interactive_Map.py` — Folium choropleth; styling from `config.json`
- `pages/2_Data_Table.py` — filterable county table
- `pages/3_Static_Plots.py` — renders plots on-demand with download buttons

**src/ modules:**
- `config.py` — all constants: `EPSG_CODE` (3082, Texas SP for contiguous US), `NON_CONTIGUOUS_CODES`, `PLOT_PARAMS` (colors, border styles, per-region dimensions), `NA_DATE` (1900-01-01 sentinel for unvisited rows), `DATE_FORMAT`
- `paths.py` — `PROJECT_ROOT` and `DATA_DIR` as `pathlib.Path` constants
- `generate_plots.py` — entry point for CI/standalone plot regeneration; calls the full pipeline and saves PNGs to `data/plots/`
- `scripts/data.py` — `import_data()` wraps both CSV ingestion and `pygris` shapefile fetching (counties + states, CB=True, year=2023)
- `scripts/processing.py` — `process_data()` joins visit DataFrame to GeoDataFrames by GEOID (`state_code + county_code`); `verify_visit()` flags visited if date ≥ 1970-01-01
- `scripts/plotting.py` — `generate_plot_data()` splits data into regions and reprojects; `Plot` class renders and saves plotnine maps
- `scripts/mapping.py` — `adjust_crs()` reprojects a GeoDataFrame; `shift_meridian()` shifts Alaska's Aleutians to prevent wrapping

## Key data details

- **GEOID** is `state_code + county_code` (e.g. `"02013"`), zero-padded — used to join CSV data to shapefiles
- **Unvisited rows** have an empty date in the CSV; they get `NA_DATE` (1900-01-01) after parsing and `visited=0`
- **Non-contiguous codes** (`NON_CONTIGUOUS_CODES`) exclude AK, HI, and territories from the contiguous US plot; Alaska gets meridian-shifted to keep Aleutians contiguous
- Shapefiles are fetched from the Census via `pygris` and cached in `~/.cache/pygris`

## CI/CD

`.github/workflows/update-plots.yml` triggers on push to `master` when `data/tables/list_of_counties_active.csv` changes (or via `workflow_dispatch`). It runs `generate_plots.py` and commits the updated PNGs back to the repo with `[skip ci]`.

## Deployment

Deployed on Streamlit Cloud at `tracking-counties.streamlit.app`. The app's Python version is pinned to 3.12 via `runtime.txt`.
