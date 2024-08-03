"""
Appindicator monitoring tool for displaying Timew tracking intervals
with optional alerts for too much keyboard time.
"""
import sys

from .utils import fetch_geoip, get_state_icon, get_status, run_cmd

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

__version__ = version('timew_status')
__all__ = [
    "__description__",
    "__version__",
    "get_state_icon",
    "get_status",
    "fetch_geoip",
    "run_cmd",
]
__description__ = "A Timew status indicator for monitoring work hours"
