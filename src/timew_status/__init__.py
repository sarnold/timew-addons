"""
Appindicator monitoring tool for displaying Timew tracking intervals
with optional alerts for too much keyboard time.
"""
import sys

from .utils import (
    CFG,
    fetch_geoip,
    get_state_icon,
    get_state_str,
    get_status,
    run_cmd,
    to_td,
)

if sys.version_info < (3, 8):
    from importlib_metadata import version
else:
    from importlib.metadata import version

__description__ = "A Timew status indicator for monitoring work hours"

__version__ = version('timew_addons')

__all__ = [
    "__description__",
    "__version__",
    "CFG",
    "fetch_geoip",
    "get_state_icon",
    "get_state_str",
    "get_status",
    "run_cmd",
    "to_td",
]
