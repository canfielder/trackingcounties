# ---------------------------------------------------------------------------- #
# IMPORT #
import datetime as dt

import pandas as pd
import siuba as s

from config import DATE_FORMAT, NA_DATE

# ---------------------------------------------------------------------------- #
# CLASSES / FUNCTIONS #


def verify_visit(date_input: dt.datetime) -> int:
    """Return 1 if the date represents a real visit, 0 if it is the NA sentinel."""
    return 0 if date_input == NA_DATE else 1


def parse_dates(
    date: str | None,
    na_date: dt.datetime,
    date_format: str = DATE_FORMAT,
) -> dt.datetime:
    """Parse a date string into a datetime, returning na_date on failure."""
    if isinstance(date, str):
        try:
            return dt.datetime.strptime(date, date_format)
        except ValueError:
            return na_date
    return na_date


def convert_visited_to_categorical(df):
    df.loc[:, "visited"] = pd.Categorical(df["visited"], ordered=False)

    return df


def process_data_visited(df):
    # Convert date strings to datetime
    df.loc[:, "date"] = df["date"].apply(lambda x: parse_dates(x, na_date=NA_DATE))

    # Verify state and county codes have leading zeros
    # State Codes
    df.loc[:, "state_code"] = df["state_code"].apply(lambda x: x.zfill(2))

    # County Codes
    df.loc[:, "county_code"] = df["county_code"].apply(lambda x: x.zfill(3))

    # Create GEOID
    df.loc[:, "geoid"] = df["state_code"] + df["county_code"]

    # Create boolean column for visited / not visited
    df.loc[:, "visited"] = df["date"].apply(verify_visit)

    return df


def create_state_visited(df_county):
    # Create table indicating which states I visited.
    df_state = (
        df_county
        >> s.group_by(s._.state_code)
        >> s.mutate(
            visited=s._.visited.max(),
        )
        >> s.ungroup()
        >> s.distinct(s._.state, s._.state_code, s._.visited)
    )

    # Create table indicating the earliest date I visited a state.
    df_state_date = (
        df_county
        >> s.filter(s._.visited == 1)
        >> s.group_by(s._.state_code)
        >> s.summarize(
            date=s._.date.min(),
        )
    )

    # Join date of state visit to visit record. NA's induced are states that
    # I have not visited.
    df_state = (
        df_state
        >> s.left_join(s._, df_state_date, by="state_code")
        >> s.rename(geoid=s._.state_code)
    )

    # Fill NA dates with placeholder date.
    df_state.loc[:, "date"] = df_state["date"].fillna(NA_DATE)

    return df_state


def process_data(df_visited, gdf_county, gdf_state):
    # Process county visit data
    df_visited_county = process_data_visited(df_visited)

    # Create state visit data
    df_visited_state = create_state_visited(df_visited_county)

    # Join visit data to shapefiles
    select_cols = ["geoid", "visited", "date"]

    gdf_visited_county = gdf_county >> s.left_join(
        s._, df_visited_county[select_cols], by="geoid"
    )

    gdf_visited_state = gdf_state >> s.left_join(
        s._, df_visited_state[select_cols], by="geoid"
    )

    # Convert visit column to categorical after the join so the dtype is preserved
    gdf_visited_county = convert_visited_to_categorical(gdf_visited_county)
    gdf_visited_state = convert_visited_to_categorical(gdf_visited_state)

    return gdf_visited_county, gdf_visited_state
