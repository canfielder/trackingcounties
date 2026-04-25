# ---------------------------------------------------------------------------- #
# IMPORT #
import datetime as dt

# ---------------------------------------------------------------------------- #
# VALUES #

# String format of date field after import
DATE_FORMAT = "%m/%d/%y"

# Placeholder for missing dates
NA_DATE = dt.datetime(1900, 1, 1)

# AK + HI + US territories
NON_CONTIGUOUS_CODES = ["02", "15", "60", "66", "69", "72", "78"]

# Territories only (AK/HI excluded) — used where shift_geometry requires 50 states
TERRITORY_CODES = ["60", "66", "69", "72", "78"]

EPSG_CODE = "3082"

# State FIPS codes for region-specific plots
FIPS_ALASKA = "02"
FIPS_HAWAII = "15"
FIPS_NC = "37"
FIPS_NC_ADJACENT = ["13", "37", "45", "47", "51"]  # GA, NC, SC, TN, VA

# DPI for saved plot files vs. on-demand web preview
PLOT_DPI = 1000
PLOT_PREVIEW_DPI = 150


PLOT_PARAMS = {
    "color": {
        0: "#F4F6F6",
        1: "#1F618D",
    },
    "opacity": {0: 0, 1: 0.15},
    "entity_border": {
        "color": {"county": "#717d7e", "state": "#000000"},  # Gray80  # Black
        "thickness": {"county": 0.2, "state": 0.5},
    },
    "dimensions": {
        "height": {
            "contiguous": 6,
            "alaska": 6,
            "hawaii": 6,
            "north_carolina": 5,
            "north_carolina_w_adjacent_states": 6,
            "us_inset": 8,
        },
        "width": {
            "contiguous": 10,
            "alaska": 7,
            "hawaii": 6,
            "north_carolina": 10,
            "north_carolina_w_adjacent_states": 8,
            "us_inset": 12,
        },
    },
}
