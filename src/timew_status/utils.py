"""
"""
import os
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

from munch import Munch
from platformdirs import PlatformDirs

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


def get_delta_limits():
    """
    Return config max/snooze limits as timedeltas. Everything comes from
    static config values and gets padded with seconds.

    :return: tuple of timedeltas
    """
    day_sum = [CFG["day_max"] + ':00', CFG["day_snooze"] + ':00']
    seat_sum = [CFG["seat_max"] + ':00', CFG["seat_snooze"] + ':00']
    day_limit = sum(map(to_td, day_sum), timedelta())  # noqa:
    seat_limit = sum(map(to_td, seat_sum), timedelta())  # noqa:
    day_max = to_td(CFG["day_max"] + ':00')
    seat_max = to_td(CFG["seat_max"] + ':00')

    return day_max, day_limit, seat_max, seat_limit


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
        'INACTIVE': 'timew_inactive',
        'ACTIVE': 'timew_info',
        'WARNING': 'timew_warning',
        'ERROR': 'timew_error',
    }

    state_dict = timew_dict
    connected_icon = Path(install_path).joinpath(icon_name)
    if not connected_icon.exists():
        state_dict = fallback_dict

    return state_dict.get(state, state_dict['INACTIVE'])


def get_state_str(cmproc, count):
    """
    Return timew tracking state, ei, the key for dict with icons.

    :param cmproc: completed timew process obj
    :type cmproc: CompletedProcess
    :param count: seat time counter value
    :type count: timedelta
    """
    DAY_MAX, DAY_LIMIT, SEAT_MAX, SEAT_LIMIT = get_delta_limits()

    state = 'INACTIVE' if cmproc.returncode == 1 else 'ACTIVE'
    msg = cmproc.stdout.decode('utf8')
    lines = msg.splitlines()

    for x in [x for x in lines if x.split(',')[0] == 'total']:
        day_total = x.split(',')[1]
    if DAY_MAX < to_td(day_total) < DAY_LIMIT:
        state = 'WARNING'
        msg = f'WARNING: day max of {DAY_MAX} has been exceeded\n' + msg
    if to_td(day_total) > DAY_LIMIT:
        state = 'ERROR'
        msg = f'ERROR: day limit of {DAY_LIMIT} has been exceeded\n' + msg
    if SEAT_MAX < count < SEAT_LIMIT:
        state = 'WARNING'
        msg = f'WARNING: seat max of {SEAT_MAX} has been exceeded\n' + msg
    if count > SEAT_LIMIT:
        state = 'ERROR'
        msg = f'ERROR: seat limit of {SEAT_LIMIT} has been exceeded\n' + msg
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


def parse_for_tag(text):
    """
    Parse the output of timew start/stop commands for the tag string.
    """
    sep = CFG["jtag_separator"]
    for line in text.splitlines():
        if line.startswith(("Tracking", "Recorded")):
            data = line.split('"')[1].split(sep)
            return f'{data[0]}{sep}"{data[1]}"'


def run_cmd(action='status', tag=None):
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
    if action == 'start' and tag:
        act_list.append(tag)
    if action != 'status':
        cmd = svc_list + act_list
    else:
        cmd = cmd + sts_list
    print(f'Running {cmd}')

    try:
        result = subprocess.run(cmd, capture_output=True)
        if action == 'stop':
            tag = parse_for_tag(result.stdout.decode())
            if DEBUG:
                print(f'run_cmd {action} result tag: {tag}')
            return result, tag
        if DEBUG:
            print(f'run_cmd {action} return code: {result.returncode}')
            print(f'run_cmd {action} result msg: {result.stdout.decode().strip()}')

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
DEBUG = os.getenv('DEBUG', default=None)
