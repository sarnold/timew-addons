Timewarrior addon bits
======================

|CI| |chk| |release|

|pre| |pylint|

|tag| |license|

What is timewarrior?
~~~~~~~~~~~~~~~~~~~~

Timewarrior_ is a command line time tracking application, which allows
you to record time spent on activities. You may be tracking your time
for curiosity, or because your work requires it

Timewarrior records time, and associates blocks of time with tags. The
recorded data can be exposed as JSON for any app to consume.

Built-in reports, as well as a set of extension reports, provides
plenty of options, in addition to customizing the time reporting using
any programming language.

.. _Timewarrior: https://timewarrior.net/docs/

But what are the addons?
~~~~~~~~~~~~~~~~~~~~~~~~

This repository is mainly a place for some example report extensions (where
in this case "example" means things actually used for reporting work hrs)
and some experimental UI ideas.

The report extensions here use an existing `Python binding`_ that
parses stdout from ``timew`` so the extension scripts must parse stdin
using the timew-report classes. See `Reporting examples`_ for details.

The current UI script uses the PyGObject_ introspection interface to
import bindings for things like Gtk_, Notify_, and Appindicator_ to render a
simple tray icon/menu and send desktop notifications. See `Appindicator GUI`_
for details.

.. _Gtk: https://pygobject.gnome.org/tutorials/gtk3.html
.. _Notify: https://lazka.github.io/pgi-docs/Notify-0.7/index.html
.. _Appindicator: https://lazka.github.io/pgi-docs/AyatanaAppIndicator3-0.1/index.html
.. _Python binding: https://github.com/lauft/timew-report/

March 2025: Python packaging and metadata patches
-------------------------------------------------

* setuptools not yet caught up with pyproject.toml rules
  - requires patch for project.license TOML type (table vs string)

* conflicting PyGObject version/dependency requirements depending on OS version
  - Jammy requires ``libgirepository1.0-dev`` and ``PyGObject==v3.50.0``
  - Noble requires ``libgirepository-2.0-dev`` and ``PyGObject>=v3.52.1``

The current workaround uses platform patches to work around these wrinkles,
eg, `this patch`_ in the Gentoo overlay.

.. _this patch: https://github.com/VCTLabs/embedded-overlay/blob/master/app-misc/timew-addons/files/interim-for-setuptools-license-str-vs-table.patch


Quick start install
~~~~~~~~~~~~~~~~~~~

The appindicator GUI prefers OS package manager over virtual environment
install due to the icon/desktop file integration with an XDG-compliant
desktop, eg, Gnome or XFCE.  While the extension scripts should work
anywhere ``timew`` can be installed, running the appindicator GUI requires
a real Linux desktop environment.  That said, the GUI script should still
run from local virtual environment, albeit with a fallback set of icons.

* if on Gentoo, add `this portage overlay`_ and install ``timew-addons``
* if on recent Ubuntu LTS, add `this PPA`_ and install ``timew-addons``

Install with OS package manager
-------------------------------

OS packages are deployed via multiple methods, including GH release pages
and package overlays for Gentoo_ and Ubuntu.

Installing using OS package manager is currently supported on Gentoo_
and requires `this portage overlay`_. Use one of the overlay install
methods shown in the overlay readme_ file and sync the overlay;
following the overlay sync, install the package and dependencies::

  $ sudo emaint sync -r embedded-overlay
  $ sudo emerge timew-addons -v --ask

OS package installation is also supported on the last few Ubuntu_ LTS
releases using the following `Ubuntu PPA`_ to install on Focal, Jammy,
or Noble.  Make sure you have the ``add-apt-repository`` command
installed, then add the PPA and install ``timew-addons``:

::

  $ sudo apt-get install software-properties-common
  $ sudo add-apt-repository -y -s ppa:nerdboy/embedded
  $ sudo apt-get install timew-addons

See `Adding this PPA to your system`_ for more info.

A somewhat manual approach using pre-built packages is available for debian
*bookworm*, *trixie*, and *sid*. First install the ``gdebi`` package::

  $ sudo apt install gdebi

Next download the ``.deb`` packages for timew-report and timew-addons from
GitHub for your Debian version, eg, for bookworm do::

  $ wget https://github.com/sarnold/timew-addons/releases/download/0.3.0/timew-addons_0.3.0-3+g478e08a-bookworm_all.deb
  $ wget https://github.com/sarnold/timew-report/releases/download/v1.4.0/timew-report_1.4.0-10+gc66c7b7-bookworm_amd64.deb

Then install the ``.deb`` packages for timew-report and timew-addons from
GitHub using gdebi::

  $ sudo gdebi timew-report_1.4.0-10+gc66c7b7-bookworm_amd64.deb
  $ sudo gdebi timew-addons_0.3.0-3+g478e08a-bookworm_all.deb

.. important:: The exact package names and Debian release will be different.
               Substitute the name of your Debian release and use the most
               recent Github release page available.


.. _Adding this PPA to your system:
.. _this PPA:
.. _Ubuntu PPA: https://launchpad.net/~nerdboy/+archive/ubuntu/embedded
.. _Gentoo: https://www.gentoo.org/
.. _Ubuntu: https://ubuntu.com/
.. _readme:
.. _this portage overlay: https://github.com/VCTLabs/embedded-overlay/


Install with pip
----------------

This project is *not* published on PyPI, thus use one of the
following commands to install the latest version in a Python
virtual environment.

From source::

  $ python3 -m venv .venv
  $ source .venv/bin/activate
  (.venv) $ pip install git+https://github.com/sarnold/timew-addons.git

The alternative to python venv is the Tox_ automation tool.  If you have it
installed already, clone this repository and try the following commands
from the top-level source directory.

To create a "dev" environment::

  $ tox -e dev

To run the tests::

  $ tox -e py

.. note:: After installing in dev mode, use the environment created by
          Tox just like any other Python virtual environment.  The dev
          install mode of Pip allows you to edit the script and run it
          again while inside the virtual environment. By default Tox
          environments are created under ``.tox/`` and named after the
          env argument (eg, dev).

.. _Tox: https://github.com/tox-dev/tox

Installed files
---------------

Whether installed via OS packages or ``pip``, the installed files are
essentially the same, other than packaging-specific requirements and
generated python byte-code. In the latter case, the list of installed
files can be obtained with the following command::

  $ python -m pip show -f timew_addons
  Name: timew-addons
  Version: 0.3.1.dev10+g8607982.d20250323
  Summary: A collection of timewarrior extensions and experiments
  Home-page: https://github.com/sarnold/timew-addons
  Author: Stephen Arnold
  Author-email: stephen.arnold42@gmail.com
  License-Expression: GPL-3.0-or-later
  Location: /home/user/src/timew-addons/.tox/check/lib/python3.13/site-packages
  Requires: munch, pycairo, PyGObject, timew-report
  Required-by:
  Files:
    ../../../bin/timew-status-indicator
    ../../../share/applications/timew-status-indicator.desktop
    ../../../share/icons/hicolor/48x48/apps/timew.png
    ../../../share/icons/hicolor/scalable/apps/timew.svg
    ../../../share/icons/hicolor/scalable/status/timew_error.svg
    ../../../share/icons/hicolor/scalable/status/timew_inactive.svg
    ../../../share/icons/hicolor/scalable/status/timew_info.svg
    ../../../share/icons/hicolor/scalable/status/timew_warning.svg
    ../../../share/timew-addons/extensions/__pycache__/csv_rpt.cpython-313.pyc
    ../../../share/timew-addons/extensions/__pycache__/onelineday.cpython-313.pyc
    ../../../share/timew-addons/extensions/__pycache__/totals.cpython-313.pyc
    ../../../share/timew-addons/extensions/csv_rpt.py
    ../../../share/timew-addons/extensions/onelineday.py
    ../../../share/timew-addons/extensions/totals.py
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/INSTALLER
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/METADATA
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/RECORD
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/REQUESTED
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/WHEEL
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/licenses/LICENSE
    timew_addons-0.3.1.dev10+g8607982.d20250323.dist-info/top_level.txt
    timew_status/__init__.py
    timew_status/__pycache__/__init__.cpython-313.pyc
    timew_status/__pycache__/utils.cpython-313.pyc
    timew_status/utils.py

Generated files
---------------

On first run, the ``timew-status-indicator`` script will create its YAML
configuration file in the standard XDG location::

  $HOME/.config/timew_status_indicator/config.yaml

with the following contents:

.. code-block:: yaml

    day_max: 08:00
    day_snooze: 01:00
    seat_max: 01:30
    seat_snooze: 00:40
    seat_reset_on_stop: false
    use_last_tag: false
    use_symbolic_icons: false
    extension_script: onelineday
    default_jtag_str: vct-sw,implement skeleton timew indicator
    jtag_separator: ','
    loop_idle_seconds: 20
    show_state_label: false
    terminal_emulator: gnome-terminal

Edit the above file to set your preferred values. Note the default value
of ``loop_idle_seconds`` seems to be a happy medium between update rate
and wasted CPU cycles.

Uninstalling
------------

Depending on how it was installed, use on or more of the following:

* delete the cloned directory, eg, ``rm -rf path/to/timew-addons``
* delete the virtual environment, eg, ``rm -rf ``.venv``

If you installed into a local env via ``pip`` then run::

    $ pip uninstall timew-addons

* or, remove the OS package, eg, on Ubuntu:

::

    $ sudo apt remove timew-addons
    $ sudo apt autoremove

Finally, delete the configuration file::

    $ rm $HOME/.config/timew_status_indicator/config.yaml


Reporting examples
~~~~~~~~~~~~~~~~~~

The following extension examples can be found in the ``extensions`` folder
in the top-level of the sdist or repository:

* ``onelineday.py`` - a real-world custom report example
* ``totals.py`` - a totals-by-tag report based on the `upstream example`_
* ``csv_rpt.py`` - a simple CSV report also based on the `upstream example`_

They must be manually installed to the location shown below.

.. _upstream example: https://github.com/lauft/timew-report/blob/master/README.md

Extension usage
---------------

In general, report extension scripts are installed under ``$HOME`` in the
timewarrior extensions folder, which on Linux equates to::

  $ ls ~/.timewarrior/extensions
  csv_rpt.py  onelineday.py totals.py

To use the report extensions, first install timewarrior `on your platform`_
and run the command from a console prompt, then find the extensions directory,
something like::

  $ sudo emerge app-misc/timew --ask
  $ timew -h
  $ find $HOME -maxdepth 1 -name .timewarrior -type d
  /home/user/.timewarrior
  $ ls /home/user/.timewarrior
  data  extensions  timewarrior.cfg

Finally, copy the desired extension(s) into the extensions folder::

  $ cp /usr/lib/timew-addons/extensions/onelineday.py ~/.timewarrior/extensions/

When using OS packages, extensions should be installed to the above path.

Run the extension by substituting the extension name for the usual "summary"
command, eg, instead of ``timew summary june``, use something like::

  $ timew onelineday june

Extension names can also be aliases of the full extension filename, so
using::

  $ timew one today

should also work.

Environment
-----------

The report extensions used by the `Appindicator GUI`_ have 2 output formats:

* the default verbose mode is "human" report output
* the optional terse mode is consumed and displayed by the GUI

The output mode and job-tag separator are exported as shell environment
variables by the GUI script on startup, which affects *only the internal*
runtime environment of the GUI. However, this means the variables are set
in the shell environment of the terminal launched by the menu option, so
running ``timew`` commands from this terminal instance will use the "terse"
output mode unless the environment variable is unset, eg, after launching
a terminal from the GUI menu, run the following in that terminal window::

  $ timew one yesterday
  xyz-test;08:39:36
  vctlabs;00:36:20
  total;09:15:56
  $ unset INDICATOR_FMT
  $ timew one yesterday
  Duration has 1 days and 2 total job tags:
  ['xyz-test', 'vctlabs']

  -- xyz-test
  2024-08-23 3:58:47 xyz-test,continue test case document structure
  2024-08-23 2:38:37 xyz-test,test doc development
  2024-08-23 0:18:55 xyz-test,test doc development discussion
  2024-08-23 1:43:17 xyz-test,test status mtg

  Total for xyz-test: 08:39:36 hrs

  -- vctlabs
  2024-08-23 0:36:20 vctlabs,project status/planning mtg

  Total for vctlabs: 00:36:20 hrs

  Final total for all jobs in duration: 09:15:56 hrs


Appindicator GUI
~~~~~~~~~~~~~~~~

timew-status-indicator is a control and status application for timew that
runs from the system tray on XDG-compliant Linux desktops.

And by "application" we mean a simple appindicator-based GUI which is
basically just an icon with a menu. It loads in the indicator area or the
system tray (whatever is available in your desktop environment). The icon's
menu allows you to start and stop time tracking, as well as get status
and edit the timew tag string. The tray icon appearance will
update to show the current state of timew vs configurable limits.

GUI usage
---------

Select Timew Status Tool from the Applications View or the Utils menu in
your desktop of choice, eg, Gnome, Unity, Xfce, etc.  You can also add it to
your session startup or run it from an X terminal to get some debug output::

  $ timew-status-indicator

What exactly are we tracking?
#############################

Simply put, we want to track work hours and seat time in the context of
the daily hours tracked via the ``timew`` command. The configuration file
contains 2 parameters each for setting desired limits, the base max value,
and an optional "snooze" period:

:day_max: target number of daily work hours
:day_snooze: additional snooze period appended to daily max
:seat_max: max number of minutes to stay seated
:seat_snooze: additional snooze period appended to seat max

Values for the above are given in hours and minutes formatted
as "time" strings, eg, the following sets an 8-hour max:

.. code-block:: yaml

    day_max: "08:00"

The seat timer can be disabled by setting both *max* and *snooze* to
zeros, ie, set both values like so:

.. code-block:: yaml

    seat_max: "00:00"
    seat_snooze: "00:00"


Status indicator GUI
####################

It would not be an Appindicator_ without icons, so we use icons as one way
to show current state. This has nothing to do with application state; in
this case we only care about the state of our *timew tracking interval*;
note this includes the seat timer warnings when there is an active timew
tracking interval. The states and corresponding icons are shown below:

:INACTIVE: |inactive| The state when there is no active tracking interval.
:INFO: |info| The default active state when tracking interval is open.
:WARNING: |warn| The state when either timer has reached the snooze period.
:ERROR: |err| The state when either snooze period has expired.
:APP: |app| While not a state, we use this to retrieve the app icon.

.. |app| image:: gh/images/timew.svg
.. |inactive| image:: gh/images/timew_inactive.svg
.. |info| image:: gh/images/timew_info.svg
.. |warn| image:: gh/images/timew_warning.svg
.. |err| image:: gh/images/timew_error.svg


PyGObject references
--------------------

* https://lazka.github.io/pgi-docs/  PyGObject API Reference
* https://pygobject-tutorial.readthedocs.io/en/latest/index.html  Tutorial
* https://github.com/candidtim/vagrant-appindicator  (old)


Operating System Support
~~~~~~~~~~~~~~~~~~~~~~~~

The extension scripts require a basic console environment with both
timewarrior and the timew-report packages installed (usually via system
package manager). Running the indicator GUI script requires both
Python_ and a modern Gtk+ windowing environment with Gtk3_ and
PyGObject_.

.. important:: The GUI script requires one of the following extensions to
               to parse the current time total from the ``timew`` output.
               They have been modified to check an environment variable
               and output a summary CSV format.

Install either ``onelineday.py`` or ``totals.py`` as shown above, depending
on preferred tag format:

onelineday
  Use for job-tag prefix format with sub-totals. See the docstring in
  ``onelineday.py`` for more details.

totals
  Use for free-form tag format *without* a job-tag prefix.

Set the extension script in the config file with the following key, using
either "onelineday" or "totals" for the value. Similarly set the job-tag
separator if needed:

.. code-block:: yaml

  extension_script: onelineday
  jtag_separator: ";"


.. _Python: https://docs.python.org/3/contents.html
.. _Gtk3: https://pygobject.gnome.org/tutorials/gtk3.html
.. _PyGObject: https://pygobject.gnome.org/index.html
.. _on your platform: https://timewarrior.net/docs/install/


.. |CI| image:: https://github.com/sarnold/timew-addons/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/sarnold/timew-addons/actions/workflows/ci.yml
    :alt: CI workflow status

.. |chk| image:: https://github.com/sarnold/timew-addons/actions/workflows/check.yml/badge.svg
    :target: https://github.com/sarnold/timew-addons/actions/workflows/check.yml
    :alt: Pre-commit status

.. |release| image:: https://github.com/sarnold/timew-addons/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/timew-addons/actions/workflows/release.yml
    :alt: Release workflow status

.. |pylint| image:: https://raw.githubusercontent.com/sarnold/timew-addons/badges/main/pylint-score.svg
    :target: https://github.com/sarnold/timew-addons/actions/workflows/pylint.yml
    :alt: Pylint Score

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&amp;logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/timew-addons?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/timew-addons/releases
    :alt: GitHub tag

.. |license| image:: https://img.shields.io/github/license/sarnold/timew-addons
    :target: https://github.com/sarnold/timew-addons/blob/master/LICENSE
    :alt: License
