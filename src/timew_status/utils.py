"""
"""
import json
import subprocess
from pathlib import Path

import requests
import xmltodict
from requests.exceptions import Timeout

CFG = {
    "day_max": "07:30",
    "day_max_snooze": "01:00",
    "seat_max": "01:30",
    "seat_max_snooze": "01:00",
}


def get_state_icon(state):
    """
    Look up the state msg and return the icon name.
    """
    install_path = '/usr/share/icons/hicolor/scalable/status'
    icon_name = 'green.svg'

    fallback_dict = {
        'INACTIVE': 'dialog-question-symbolic.svg',
        'ACTIVE': 'dialog-information-symbolic.svg',
        'WARNING': 'dialog-warning-symbolic.svg',
        'ERROR': 'dialog-error-symbolic.svg',
    }

    timew_dict = {
        'INACTIVE': 'notifications-disabled-symbolic.svg',
        'ACTIVE': 'green.svg',
        'WARNING': 'yellow.svg',
        'ERROR': 'red.svg',
    }

    state_dict = timew_dict
    connected_icon = Path(install_path).joinpath(icon_name)
    if not connected_icon.exists():
        state_dict = fallback_dict

    return state_dict.get(state, state_dict['INACTIVE'])


def get_status():
    """
    Return timew tracking status.
    """
    try:
        result = subprocess.run(["timew"], capture_output=True)
    except Exception as exc:
        print(f'Timew status error: {exc}')
    return result


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
    cmd = svc_list
    act_list = [action]

    if action not in actions:
        print(f'Invalid action: {action}')
        return
    if action != 'status':
        cmd = svc_list + act_list
    print(f'Running {cmd}')

    try:
        result = subprocess.run(cmd, capture_output=True)
        if result.retcode == 1:
            print('return code not equal zero')
        else:
            print(f'{action} return code: {result.retcode}')

        return result.stdout.decode('utf8')

    except Exception as exc:
        print(f'run_cmd exception: {exc}')
