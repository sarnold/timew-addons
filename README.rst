========================
 Timewarrior addon bits
========================

|CI| |pre|

|tag| |license|

What is timewarrior?
====================

Timewarrior_ is a command line time tracking application, which allows
you to record time spent on activities. You may be tracking your time
for curiosity, or because your work requires it

Timewarrior records time, and associates blocks of time with tags. The
recorded data can be exposed as JSON for any app to consume.

Built-in reports, as well as a set of extension reports, provides
plenty of options, in addition to customizing the time reporting using
any programming language.

.. _Timewarrior: https://timewarrior.net/docs/

This repository is mainly a place for some example report extensions (where
in this case "example" means things I actually use for reporting work hrs)
and some experimental (at least for now) UI ideas.

The report extensions here use an existing `Python binding`_ but the easiest
way to get started is probably the (JSON) export interface::

  $ timew export

.. _Python binding: https://github.com/lauft/timew-report/

Reporting examples
==================

* ``csv_rpt.py`` - a simple CSV report based on the `upstream example`_
* ``onelineday.py`` - a real-world custom report example


.. _upstream example: https://github.com/lauft/timew-report/?tab=readme-ov-file#examples

Usage
=====

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

  $ cp path/to/csv_rpt.py ~/.timewarrior/extensions/

Run the extension by substituting the extension name for the usual "summary"
command, eg, instead of ``timew summary june``, use something like::

  $ timew csv_rpt june

Extension names can also be aliases of the full extension filename, so
using::

  $ timew csv june

should also work.


Operating System Support
------------------------

Most of these tools require a basic console environment with timewarrior
installed (usually via system package manager). Installing with ``[gui]``
enabled requires both Python_ and a modern Gtk+ windowing environment
with PyGObject_.

The above platform link shows package support for several Linux distributions
and MacOS.


.. _Python: https://docs.python.org/3/contents.html
.. _PyGObject: https://pygobject.gnome.org/index.html
.. _on your platform: https://timewarrior.net/docs/install/


.. |CI| image:: https://github.com/sarnold/timewarrior-addons/actions/workflows/main.yml/badge.svg
    :target: https://github.com/sarnold/timewarrior-addons/actions/workflows/main.yml
    :alt: CI test status

.. |pre| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&amp;logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

.. |tag| image:: https://img.shields.io/github/v/tag/sarnold/timewarrior-addons?color=green&include_prereleases&label=latest%20release
    :target: https://github.com/sarnold/timewarrior-addons/releases
    :alt: GitHub tag

.. |license| image:: https://img.shields.io/github/license/sarnold/timewarrior-addons
    :target: https://github.com/sarnold/timewarrior-addons/blob/master/LICENSE
    :alt: License
