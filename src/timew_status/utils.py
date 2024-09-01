"""
Base configuration and app helper functions.
"""
import os
import subprocess
from datetime import timedelta
from pathlib import Path

from munch import Munch

APP_NAME = 'timew_status_indicator'
CFG = {
    # time strings are HH:MM (no seconds)
    "day_max": "08:00",
    "day_snooze": "01:00",
    "seat_max": "01:30",
    "seat_snooze": "00:40",
    "seat_reset_on_stop": False,
    "use_last_tag": False,
    "use_symbolic_icons": False,
    "extension_script": "onelineday",
    "default_jtag_str": "vct-sw,implement skeleton timew indicator",
    "jtag_separator": ",",
    "loop_idle_seconds": 20,
    "show_state_label": False,
    "terminal_emulator": "gnome-terminal",
    "extensions_dir": ".timewarrior/extensions",
    "install_dir": "share/timew-addons/extensions",
    "install_prefix": "/usr",
}


def do_install(cfg):
    """
    Install report extensions to timew extensions directory. The default src
    paths are preconfigured and should probably not be changed unless you
    know what you are doing, since *they are created during install or setup*.
    You should, however, adjust the destination path in ``extensions_dir`` if
    needed for your platform. Returns the destination path string for each
    installed extension script.

    :param cfg: runtime CFG dict
    :return files: list of strings
    """
    prefix = cfg["install_prefix"]
    srcdir = Path(prefix) / cfg["install_dir"]
    destdir = Path.home() / cfg["extensions_dir"]
    extensions = ['totals.py', 'onelineday.py']
    files = []

    for file in extensions:
        dest = destdir / file
        src = srcdir / file
        if DEBUG:
            print(f"do_install: src is {src}")
            print(f"do_install: dest is {dest}")
        dest.write_bytes(src.read_bytes())
        print(f"{str(file)} written successfully")
        files.append(str(file))
    return files


def get_config(file_encoding='utf-8'):
    """
    Load configuration file and munchify the data. If local file is not
    found in config directory, the default will be loaded and saved to
    XDG config directory. Return a Munch cfg obj and corresponding Path
    obj.

    :param file_encoding: file encoding of config file
    :type file_encoding: str
    :return: tuple of Munch and Path objs
    """
    cfgdir = get_userdirs()
    cfgfile = cfgdir.joinpath('config.yaml')
    if not cfgfile.exists():
        print(f"Saving initial config data to {cfgfile}")
        cfgfile.write_text(Munch.toYAML(CFG), encoding=file_encoding)
    cfgobj = Munch.fromYAML(cfgfile.read_text(encoding=file_encoding))

    return cfgobj, cfgfile


def get_delta_limits(ucfg):
    """
    Return config max/snooze limits as timedeltas. Everything comes from
    static config values and gets padded with seconds.

    :param ucfg: runtime CFG dict
    :return: tuple of 4 timedeltas
    """
    cfg = Munch.fromDict(ucfg)
    pad = ':00'
    day_sum = [cfg.day_max + pad, cfg.day_snooze + pad]
    seat_sum = [cfg.seat_max + pad, cfg.seat_snooze + pad]
    day_limit = sum(map(to_td, day_sum), timedelta())  # noqa:
    seat_limit = sum(map(to_td, seat_sum), timedelta())  # noqa:
    day_max = to_td(cfg.day_max + pad)
    seat_max = to_td(cfg.seat_max + pad)

    return day_max, day_limit, seat_max, seat_limit


def get_state_icon(state, cfg):
    """
    Look up the state msg and return the icon name. Use builtin symbolic
    icons as fallback.

    :param state: name of state key
    :type state: str
    :param cfg: runtime CFG (dict)

    :return: matching icon name (str)
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
    app_icon = Path(install_path).joinpath(icon_name)
    if cfg["use_symbolic_icons"] or not app_icon.exists():
        state_dict = fallback_dict

    return state_dict.get(state, state_dict['INACTIVE'])


def get_state_str(cmproc, count, cfg):
    """
    Return timew state message and tracking state, ie, the key for dict
    with icons.

    :param cmproc: completed timew process obj
    :type cmproc: CompletedProcess
    :param count: seat time counter value
    :type count: timedelta
    :param cfg: runtime CFG
    :type cfg: Dict

    :return: tuple of state msg and state string
    """
    DAY_MAX, DAY_LIMIT, SEAT_MAX, SEAT_LIMIT = get_delta_limits(cfg)

    state = 'INACTIVE' if cmproc.returncode == 1 else 'ACTIVE'
    msg = cmproc.stdout.decode('utf8')
    lines = msg.splitlines()
    day_total = '00:00:00'

    for x in [x for x in lines if x.split(';')[0] == 'total']:
        day_total = x.split(';')[1]
    if DAY_MAX < to_td(day_total) < DAY_LIMIT:
        state = 'WARNING'
        msg = f'WARNING: day max of {DAY_MAX} has been exceeded\n' + msg
    if to_td(day_total) > DAY_LIMIT:
        state = 'ERROR'
        msg = f'ERROR: day limit of {DAY_LIMIT} has been exceeded\n' + msg
    if cfg["seat_max"] != "00:00" and cfg["seat_snooze"] != "00:00":
        if SEAT_MAX < count < SEAT_LIMIT:
            state = 'WARNING'
            msg = f'WARNING: seat max of {SEAT_MAX} has been exceeded\n' + msg
        if count > SEAT_LIMIT:
            state = 'ERROR'
            msg = f'ERROR: seat limit of {SEAT_LIMIT} has been exceeded\n' + msg
    return msg, state


def get_status():
    """
    Return timew tracking status (output of ``timew`` with no arguments).

    :param None:
    :return: timew output str or None
    """
    try:
        return subprocess.run(["timew"], capture_output=True)
    except FileNotFoundError as exc:
        print(f'Timew status error: {exc}')


def get_userdirs():
    """
    Get XDG user configuration path defined as ``XDG_CONFIG_HOME`` plus
    application name. This may grow if needed.

    :param None:
    :return: XDG Path obj
    """
    xdg_path = os.getenv('XDG_CONFIG_HOME')
    config_home = Path(xdg_path) if xdg_path else Path.home().joinpath('.config')
    configdir = config_home.joinpath(APP_NAME)
    configdir.mkdir(parents=True, exist_ok=True)

    return configdir


def parse_for_tag(text):
    """
    Parse the output of timew start/stop commands for the tag string.

    :param text: start or stop output from ``timew`` (via run_cmd)
    :return: timew tag string
    """
    for line in text.splitlines():
        if line.startswith(("Tracking", "Recorded")):
            return line.split('"')[1]


def run_cmd(action='status', tag=None):
    """
    Run timew command subject to the given action.

    :param action: one of <start|stop|status>
    :return: completed proc obj and result msg
    """

    actions = ['start', 'stop', 'status']
    svc_list = ['timew']
    sts_list = [CFG["extension_script"], "today"]
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

        return result, result.stdout.decode()

    except Exception as exc:
        print(f'run_cmd exception: {exc}')


def to_td(hms):
    """
    Convert a time string in HH:MM:SS format to a timedelta object.

    :param hms: time string
    :return: timedelta obj
    """
    hrs, mins, secs = hms.split(':')
    return timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))


DEBUG = os.getenv('DEBUG', default=None)
