# ---------------------------------------------------------------------------- #
# IMPORT #
import pandas as pd
import pygris

from paths import DATA_DIR

# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #


def import_data_visit():
    county_path = DATA_DIR / "tables" / "list_of_counties_active.csv"

    # Define column date types
    dct_dtypes = {
        "state_code": str,
        "state_name": str,
        "county_code": str,
        "county_name": str,
        "visited": int,
        "geoid": str,
        "date": str,
    }

    df = pd.read_csv(
        county_path,
        dtype=dct_dtypes,
    )

    return df


def import_shapefiles():
    gdf_state = pygris.states(cb=True, year=2023, cache=True)
    gdf_state.columns = [col.lower() for col in gdf_state.columns]

    gdf_county = pygris.counties(cb=True, year=2023, cache=True)
    gdf_county.columns = [col.lower() for col in gdf_county.columns]

    return gdf_county, gdf_state


def import_data():
    # County Visit Data
    df_visit_county = import_data_visit()

    gdf_county, gdf_state = import_shapefiles()

    return df_visit_county, gdf_county, gdf_state
