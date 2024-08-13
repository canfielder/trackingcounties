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