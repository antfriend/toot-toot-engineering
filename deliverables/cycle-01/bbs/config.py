# config.py - Toot-Toot BBS / K10
# Keep configuration centralized and simple.

PORT = 2323

# Networking mode:
#   "ap"     -> attempt to start Access Point (preferred for the prompt)
#   "sta"    -> attempt to connect as station (optional)
WIFI_MODE = "ap"

# AP settings (only used when WIFI_MODE == "ap")
AP_SSID = "TOOT-TOOT-BBS"
AP_PASSWORD = ""  # open AP by default; keep empty for simplicity
AP_CHANNEL = 6

BANNER_LINES = [
    "TOOT-TOOT BBS / K10",
    "RAW TCP 2323",
    "TYPE HELP",
]

# Low-bandwidth UI limits
MAX_LINE_BYTES = 120          # maximum inbound line length (ASCII)
PAGE_MAX_LINES = 12           # page by line count
PAGE_MAX_BYTES = 600          # and/or by byte count

# Message constraints
MAX_BODY_BYTES = 512          # hard cap for posts
POST_TIMEOUT_S = 20

# Storage
DB_PATH = "db/mpdb-lite.mmpdb"

# Simple idle timeout (seconds) for sessions
IDLE_TIMEOUT_S = 300
