Timewarrior addon bits
======================

|CI| |release|

|pre|

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

Install with package manager
----------------------------

OS packages are deployed via multiple methods, including GH release pages
and package overlays for Gentoo_ and Ubuntu.

Installing using system package manager is currently only supported on
Gentoo_ and requires `this portage overlay`_. Use one of the overlay
install methods shown in the readme_ file and sync the overlay; following
the overlay sync, install the package and dependencies::

  $ sudo emerge timew-addons -v --ask

When available, use the following `Ubuntu PPA`_ to install on at least
Focal and Jammy.  Make sure you have the ``add-apt-repository`` command
installed and then add the PPA:

::

  $ sudo apt-get install software-properties-common
  $ sudo add-apt-repository -y -s ppa:nerdboy/embedded
  $ sudo apt-get install timew-addons

See `Adding this PPA to your system`_ for more info.

.. _Adding this PPA to your system:
.. _this PPA:
.. _Ubuntu PPA: https://launchpad.net/~nerdboy/+archive/ubuntu/embedded
.. _Gentoo: https://www.gentoo.org/
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

Indicator states
################

It would not be an Appindicator_ without icons, so we use icons as one way
to show current state.


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

.. |release| image:: https://github.com/sarnold/timew-addons/actions/workflows/release.yml/badge.svg
    :target: https://github.com/sarnold/timew-addons/actions/workflows/release.yml
    :alt: Release workflow status

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&amp;logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/timew-addons?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/timew-addons/releases
    :alt: GitHub tag

.. |license| image:: https://img.shields.io/github/license/sarnold/timew-addons
    :target: https://github.com/sarnold/timew-addons/blob/master/LICENSE
    :alt: License
