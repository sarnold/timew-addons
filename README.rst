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
.. _Notify: https://lazka.github.io/pgi-docs/#Notify-0.7
.. _Appindicator: https://lazka.github.io/pgi-docs/#AyatanaAppIndicator3-0.1
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
.. _this portage overlay: https://github.com/VCTLabs/embedded-overlay/
.. _readme: https://github.com/VCTLabs/embedded-overlay?tab=readme-ov-file#install-the-overlay-without-layman

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

* ``csv_rpt.py`` - a simple CSV report based on the `upstream example`_
* ``onelineday.py`` - a real-world custom report example

They must be manually installed to the location shown below.

.. _upstream example: https://github.com/lauft/timew-report/?tab=readme-ov-file#examples

Extension usage
---------------

In general, report extension scripts are installed under ``$HOME`` in the
timewarrior extensions folder, which on Linux equates to::

  $ ls ~/.timewarrior/extensions
  csv_rpt.py  onelineday.py

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

  $ cp path/to/onelineday.py ~/.timewarrior/extensions/

Run the extension by substituting the extension name for the usual "summary"
command, eg, instead of ``timew summary june``, use something like::

  $ timew onelineday june

Extension names can also be aliases of the full extension filename, so
using::

  $ timew one today

should also work.

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

Select Timew Status Tool from the Applications View or the Internet menu in
your desktop of choice, eg, Gnome, Unity, Xfce, etc.  You can also add it to
your session startup or run it from an X terminal to get some debug output::

  $ timew-status-indicator


Operating System Support
########################

The extension scripts require a basic console environment with both
timewarrior and the timew-report packages installed (usually via system
package manager). Running the indicator GUI script requires both
Python_ and a modern Gtk+ windowing environment with Gtk3+_ and
PyGObject_.

.. note:: The GUI script also requires the ``onelineday.py`` extension to
          be installed (as shown above) in order to interact with ``timew``.

The above (timew) platform support link shows package support for several
Linux distributions.


.. _Python: https://docs.python.org/3/contents.html
.. _PyGObject: https://pygobject.gnome.org/index.html
.. _on your platform: https://timewarrior.net/docs/install/


PyGObject references
####################

* https://lazka.github.io/pgi-docs/  PyGObject API Reference
* https://pygobject-tutorial.readthedocs.io/en/latest/index.html  Tutorial
* https://github.com/candidtim/vagrant-appindicator  (old)


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
