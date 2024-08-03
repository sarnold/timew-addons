# This code was adapted from an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import json
import signal

import gi
import requests
import xmltodict
from requests.exceptions import Timeout

gi.require_version('Notify', '0.7')

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator
except ValueError:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator

from gi.repository import Gtk as gtk
from gi.repository import Notify as notify

APPINDICATOR_ID = 'indicator_test'


def main():
    indicator = appindicator.Indicator.new(
        APPINDICATOR_ID,
        "dialog-information-symbolic.svg",
        appindicator.IndicatorCategory.APPLICATION_STATUS,
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()


def build_menu():
    menu = gtk.Menu()
    item_geoip = gtk.MenuItem(label='Geoip')
    item_geoip.connect('activate', geoip)
    menu.append(item_geoip)
    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu


def fetch_geoip():
    try:
        response = requests.get("https://geoip.ubuntu.com/lookup", timeout=(1, 3))
    except Timeout:
        print("The request timed out")
        return
    payload = xmltodict.parse(response.text)
    return json.dumps(payload)


def geoip(_):
    notify.Notification.new("Geoip", fetch_geoip(), None).show()


def quit(_):
    notify.uninit()
    gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
