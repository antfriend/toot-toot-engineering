"""bbs/config.py

Configuration for the UNIHIKER K10 MicroPython TCP BBS.

Keep values conservative for memory and low-bandwidth clients.
"""

# Network / AP settings (update to taste)
AP_SSID = "TOOT-TOOT-BBS"
AP_PASSWORD = "toottootbbs"  # not secure; MVP only

TCP_HOST = "0.0.0.0"
TCP_PORT = 2323

# Protocol / UI pacing
LINE_ENDING = "\r\n"

# Pagination budgets (tune if clients struggle)
PAGE_MAX_LINES = 18
PAGE_MAX_BYTES = 900

# Input limits
MAX_LINE_BYTES = 120           # max bytes per command line
MAX_HANDLE_LEN = 16
MAX_POST_BYTES = 512           # body size limit (ASCII)

# Storage
DB_PATH = "/bbs_data/mpdb_lite.mmpdb"

# Banner text (ASCII)
BANNER_LINES = [
    "TOOT-TOOT BBS (K10)",
    "LOW BANDWIDTH MODE",
    "TYPE HELLO",
]
