import numpy as np

def shift_meridian(geo_df, new_centerline): 
    """
    Shift geometries in a GeoDataFrame to be centered around a new central meridian.

    Parameters
    ----------
    geo_df : geopandas.GeoDataFrame
        A GeoDataFrame containing the geometries to be shifted.
    new_centerline : float
        The longitude of the new central meridian (in degrees).

    Returns
    -------
    geopandas.GeoDataFrame
        A new GeoDataFrame with geometries shifted to the new central meridian.
    """

    # Define new central meridian
    central_meridian = LineString([
        (new_centerline, 90),
        (new_centerline, -90)
        ])

    # Init
    gframes  = []

    for _, row in geo_df.iterrows():

        # Extract values
        element = row['geometry']

        # Split current geometry by new central meridian.
        split_geoms = split(element, central_meridian)

        # Init
        shifted_parts = []
        for part in split_geoms.geoms:
            
            min_x = part.bounds[0]  # Extract minimum x (longitude)

            # Determine the translation direction
            if min_x >= new_centerline:
                adjust_factor = -1
            else:
                adjust_factor = 1
            
            # Calculate the translation offset
            x_off = (180 * adjust_factor) - new_centerline

            # Translate geometry
            shifted_part = translate(
                part, 
                xoff = x_off
                )

            shifted_parts.append(shifted_part)
        
        # Combine the shifted parts into a single geometry
        unified_geom = gpd.GeoSeries(unary_union(shifted_parts))

        # Converty unified geometries into geo dataframe
        gdf_geom_shift = geopandas.GeoDataFrame(
            {
                "geometry": unified_geom
                }
            )
        gframes.append(gdf_geom_shift)

    # Concatenate all geo dataframes togeter
    gdf_unify = pd.concat(gframes)

    # Assign original index to new geometry dataframe
    gdf_unify.index = geo_df.index

    # Concatenate new transposed geo dataframe back to initial 
    geo_df = pd.concat(
        [
            geo_df.drop(columns= ['geometry']), 
            gdf_unify
            ],
        axis = 1
    )

    return geo_df
