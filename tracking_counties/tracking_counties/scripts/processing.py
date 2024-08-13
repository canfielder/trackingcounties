# ---------------------------------------------------------------------------- #
# IMPORT #
import datetime as dt
import pandas as pd
import siuba as s

from ..config import NA_DATE, DATE_FORMAT


# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #

def verify_visit(date_input):
    if date_input >= dt.datetime(1970, 1, 1):
        visited = 1
    else:
        visited = 0 
    return visited


def parse_dates(date, na_date, date_format = DATE_FORMAT):
    if isinstance(date, str):
        output = dt.datetime.strptime(date, date_format)
    else:
        output = na_date
    return output


def convert_visited_to_categorical(df):
    df.loc[:,'visited'] = pd.Categorical(
        df['visited'],
        ordered = False
    )

    return df


def process_data_visited(df):
    # Convert date strings to datetime
    df.loc[:,'date'] = df['date'] \
        .apply(lambda x: parse_dates(x, na_date = NA_DATE))

    # Verify state and county codes have leading zeros
    # State Codes
    df.loc[:,'state_code'] = df['state_code'].apply(lambda x: x.zfill(2))

    # County Codes
    df.loc[:,'county_code'] = df['county_code'].apply(lambda x: x.zfill(3))

    # Create GEOID 
    df.loc[:,'geoid'] = df['state_code'] + df['county_code']

    # Create boolean column for visited / not visited
    df.loc[:,'visited'] = df['date'].apply(verify_visit)

    return df


def create_state_visited(df_county):
    # Create table indicating which states I visited.
    df_state = (
        df_county
        >> s.group_by(s._.state_code)
        >> s.mutate(
            visited = s._.visited.max(),
        )
        >> s.ungroup()
        >> s.distinct(
            s._.state,
            s._.state_code,
            s._.visited
        )
    )

    # Create table indicating the earliest date I visited a state.
    df_state_date = (
        df_county
        >> s.filter(s._.visited == 1)
        >> s.group_by(s._.state_code)
        >> s.summarize(
            date = s._.date.min(),
        )
    )

    # Join date of state visit to visit record. NA's induced are states that 
    # I have not visited.
    df_state = (
        df_state
        >> s.left_join(
            s._,
            df_state_date,
            by = 'state_code'
        )
        >> s.rename(
            geoid = s._.state_code
            )
    )

    # Fill NA dates with placeholder date.
    df_state.loc[:,'date'] = df_state['date'].fillna(NA_DATE)

    return df_state


def process_data(
        df_visited,
        gdf_county,
        gdf_state
    ):

    # Process county visit data
    df_visited_county = process_data_visited(df_visited)

    # Create state visit data
    df_visited_state = create_state_visited(df_visited_county)

    # Convert visit column to categorical
    df_visited_county = convert_visited_to_categorical(df_visited_county)
    df_visited_state = convert_visited_to_categorical(df_visited_state)

    # Join visit data to shapefiles
    select_cols = ['geoid', 'visited', 'date']

    gdf_visited_county = (
        gdf_county
        >> s.left_join(
            s._,
            df_visited_county[select_cols],
            by = 'geoid'
        )   
    )

    gdf_visited_state = (
        gdf_state
        >> s.left_join(
            s._,
            df_visited_state[select_cols],
            by = 'geoid'
        )   
    )

    return gdf_visited_county, gdf_visited_state