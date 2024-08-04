"""
"""
import json
import subprocess
from datetime import timedelta
from pathlib import Path

import requests
import xmltodict
from requests.exceptions import Timeout

CFG = {
    "day_max": "08:00",
    "day_snooze": "01:00",
    "seat_max": "01:30",
    "seat_snooze": "01:00",
    "default_jtag_str": 'vct-sw,"implement skeleton timew indicator"',
    "jtag_separator": ",",
    "show_state_label": False,
    "terminal_emulator": "gnome-terminal",
}


def get_state_icon(state):
    """
    Look up the state msg and return the icon name.
    """
    install_path = '/usr/share/icons/hicolor/48x48/apps'
    icon_name = 'timew.svg'

    fallback_dict = {
        'INACTIVE': 'dialog-question-symbolic.svg',
        'ACTIVE': 'dialog-information-symbolic.svg',
        'WARNING': 'dialog-warning-symbolic.svg',
        'ERROR': 'dialog-error-symbolic.svg',
    }

    timew_dict = {
        'INACTIVE': 'timew.svg',
        'ACTIVE': 'green.svg',
        'WARNING': 'yellow.svg',
        'ERROR': 'red.svg',
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
    :return: cmd result or nothing
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
        result_msg = result.stdout.decode().strip()
        if result.returncode == 1:
            print('return code not equal zero')
        else:
            print(f'{action} return code: {result.returncode}')
        print(f'result msg: {result_msg}')

        return result, result_msg

    except Exception as exc:
        print(f'run_cmd exception: {exc}')


def to_td(h):
    """
    Convert a time string in HH:MM:SS format to a timedelta object.
    """
    hrs, mins, secs = h.split(':')
    return timedelta(hours=int(hrs), minutes=int(mins), seconds=int(secs))
