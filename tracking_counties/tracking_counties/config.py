# ---------------------------------------------------------------------------- #
# IMPORT #
import datetime as dt

from .scripts.misc import get_project_directory

# ---------------------------------------------------------------------------- #
# VALUES #

SEED = 5590

ROOT_DIR = get_project_directory()

# String format of date field after import
DATE_FORMAT = "%m/%d/%y"

# Placeholder for missing dates
NA_DATE = dt.datetime(1900, 1, 1)

NON_CONTIGUOUS_CODES = [
    '02', '15', '60', '66', '69', '72', '78'
]

EPSG_CODE = '3082'


PLOT_PARAMS = {
    'color': {
        0: "#F4F6F6", 
        1: "#1F618D",
    },
    'opacity': {
        0: 0, 
        1: 0.15
    },
    'entity_border': {
        'color': {
            'county': "#717d7e", # Gray80
            'state': "#000000"   # Black
        },
        'thickness': {
            'county': 0.2,
            'state': 0.5
        }
    },
    'dimensions': {
        'height': {
            'contiguous': 6,
            'alaska': 6,
            'hawaii': 6,
            'north_carolina': 5,
            'north_carolina_w_adjacent_states': 6
        },
        'width': {
            'contiguous': 10,
            'alaska': 7,
            'hawaii': 6,
            'north_carolina': 10,
            'north_carolina_w_adjacent_states': 8
        }
    }
}