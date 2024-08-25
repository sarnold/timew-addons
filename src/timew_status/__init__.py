"""
Monitoring and reporting tools for Timew tracking intervals with optional
appindicator alerts for keyboard time and daily hours.
"""
import sys

from .utils import (
    CFG,
    DEBUG,
    do_install,
    get_config,
    get_delta_limits,
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

__description__ = "Timew addons for reporting and monitoring tracked hours"
__version__ = version('timew_addons')
TAG = {'text': ''}

__all__ = [
    "__description__",
    "__version__",
    "CFG",
    "DEBUG",
    "TAG",
    "do_install",
    "get_config",
    "get_delta_limits",
    "get_state_icon",
    "get_state_str",
    "get_status",
    "run_cmd",
    "to_td",
]
