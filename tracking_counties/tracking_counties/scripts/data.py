# ---------------------------------------------------------------------------- #
# IMPORT #
import geopandas as gpd
import pandas as pd
import pathlib as pl

from ..config import ROOT_DIR


# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #

def import_data_visit():
    county_path = pl.PurePath(
        ROOT_DIR, 'data', 'tables', 'list_of_counties_active.csv'
        )

    # Define column date types
    dct_dtypes = {
        'state_code': str,
        'state_name': str,
        'county_code': str,
        'county_name': str,
        'visited': int,
        'geoid': str,
        'date': str
    }

    df = pd.read_csv(
        county_path, 
        dtype = dct_dtypes,
        )

    return df


def import_shapefiles():
    # State Shapefile Data ----------------------------------------------------
    sf_path = pl.PurePath(
        ROOT_DIR, 'data', 'shapefiles', 'cb_2023_us_state_500k', 
        'cb_2023_us_state_500k.shp'
    )
    gdf_state = gpd.read_file(str(sf_path))

    # Set clumn names to lower case
    gdf_state.columns = [col.lower() for col in gdf_state.columns]

    # County Shapefile Data ----------------------------------------------------
    sf_path = pl.PurePath(
        ROOT_DIR, 'data', 'shapefiles', 'cb_2023_us_county_500k', 
        'cb_2023_us_county_500k.shp'
    )
    gdf_county = gpd.read_file(str(sf_path))

    # Set column names to lower case
    gdf_county.columns = [col.lower() for col in gdf_county.columns]

    return gdf_county, gdf_state


def import_data():
    # County Visit Data 
    df_visit_county = import_data_visit()

    gdf_county, gdf_state = import_shapefiles()

    return df_visit_county, gdf_county, gdf_state