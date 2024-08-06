"""
"""
import json
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import requests
import xmltodict
from munch import Munch
from platformdirs import PlatformDirs
from requests.exceptions import Timeout

if sys.version_info < (3, 10):
    import importlib_resources
else:
    import importlib.resources as importlib_resources

APP_NAME = 'timew_status_indicator'
APP_AUTHOR = "nerdboy"


def get_config(file_encoding='utf-8'):
    """
    Load configuration file and munchify the data. If local file is not
    found in current directory, the default will be loaded.  Return a
    Munch cfg obj and corresponding Path obj.

    :param file_encoding: file encoding of config file
    :type file_encoding: str
    :return: Munch cfg obj and cfg file as Path obj
    :rtype tuple:
    """
    dirs = get_userdirs()
    cfgfile = dirs[1].joinpath('config.yaml')
    if not cfgfile.exists():
        default = importlib_resources.files('timew_status.data').joinpath('config.yaml')
        defcfg = Munch.fromYAML(default.read_text(encoding=file_encoding))
        cfgfile.write_text(Munch.toYAML(defcfg), encoding=file_encoding)
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))

    return cfgobj, cfgfile


def get_state_icon(state):
    """
    Look up the state msg and return the icon name.
    """
    install_path = '/usr/share/icons/hicolor/scalable/apps'
    icon_name = 'timew.svg'

    fallback_dict = {
        'APP': 'dialog-information-symbolic',
        'INACTIVE': 'dialog-question-symbolic',
        'ACTIVE': 'dialog-information-symbolic',
        'WARNING': 'dialog-warning-symbolic',
        'ERROR': 'dialog-error-symbolic',
    }

    timew_dict = {
        'APP': 'timew',
        'INACTIVE': 'white',
        'ACTIVE': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
    }

    state_dict = timew_dict
    connected_icon = Path(install_path).joinpath(icon_name)
    if not connected_icon.exists():
        state_dict = fallback_dict

    return state_dict.get(state, state_dict['INACTIVE'])


def get_state_str(cmproc):
    """
    Return timew tracking state, ei, the key for dict with icons.

    :param cmproc: completed timew process obj
    :type cmproc: CompletedProcess
    """
    DAY_SUM = [CFG["day_max"] + ':00', CFG["day_snooze"] + ':00']
    SEAT_SUM = [CFG["seat_max"] + ':00', CFG["seat_snooze"] + ':00']
    DAY_LIMIT = sum(map(to_td, DAY_SUM), timedelta())  # noqa:
    SEAT_LIMIT = sum(map(to_td, SEAT_SUM), timedelta())  # noqa:
    DAY_MAX = to_td(CFG["day_max"] + ':00')
    # SEAT_MAX = to_td(CFG["seat_max"] + ':00')

    state = 'INACTIVE' if cmproc.returncode == 1 else 'ACTIVE'
    msg = cmproc.stdout.decode('utf8')
    lines = msg.splitlines()
    for x in [x for x in lines if x.split(',')[0] == 'total']:
        day_total = x.split(',')[1]
    if day_total == '00:00:00':
        return msg, state
    if DAY_MAX < to_td(day_total) < DAY_LIMIT:
        state = 'WARNING'
    if to_td(day_total) > DAY_LIMIT:
        state = 'ERROR'
    return msg, state


def get_status():
    """
    Return timew tracking status.
    """
    try:
        return subprocess.run(["timew"], capture_output=True)
    except FileNotFoundError as exc:
        print(f'Timew status error: {exc}')


def get_userdirs():
    """
    Get platform-agnostic user directory paths via platformdirs.

    :return tuple: Path objs
    """
    dirs = PlatformDirs(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
    cachedir = dirs.user_cache_path
    configdir = dirs.user_config_path
    datadir = dirs.user_data_path
    logdir = dirs.user_log_path

    return cachedir, configdir, datadir, logdir


def fetch_geoip():
    """
    Fetch location info from ubuntu.com geoip server and transform the
    xml payload to json.
    """
    try:
        response = requests.get("https://geoip.ubuntu.com/lookup", timeout=(1, 3))
    except Timeout:
        print("The request timed out")
        return
    payload = xmltodict.parse(response.text)
    return json.dumps(payload, indent=4, separators=(',', ': '))


def run_cmd(action='status'):
    """
    Run timew command subject to the given action.

    :param action: one of <start|stop|status>
    :return: completed proc obj and result msg
    """

    actions = ['start', 'stop', 'status']
    svc_list = ['timew']
    sts_list = ["one", "today"]
    cmd = svc_list
    act_list = [action]

    if action not in actions:
        print(f'Invalid action: {action}')
        return
    if action != 'status':
        cmd = svc_list + act_list
    else:
        cmd = cmd + sts_list
    print(f'Running {cmd}')

    try:
        result = subprocess.run(cmd, capture_output=True)
        print(f'{action} return code: {result.returncode}')
        print(f'{action} result msg: {result.stdout.decode().strip()}')

        return result, result.stdout.decode().strip()

    except Exception as exc:
        print(f'run_cmd exception: {exc}')


def to_td(h):
    """
    Convert a time string in HH:MM:SS format to a timedelta object.
    """
    hrs, mins, secs = h.split(':')
    return timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))


CFG, _ = Munch.toDict(get_config())
