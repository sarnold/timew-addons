Changelog
=========

0.0.1.dev25 (2024-08-16)
------------------------

New
~~~
- Reset seat counter on stop after err, plus cleanup. [Stephen L Arnold]

  * abstract out delta_limits, hide some prints behind DEBUG
- Wire up seat-time counter and related value checks. [Stephen L Arnold]
- Add tag editing widget for start cmd plus a simple test. [Stephen L
  Arnold]

  * update config with more tag parameters, allow last_tag reuse
- Add default yaml config file with platform user dirs. [Stephen L
  Arnold]
- Add app and indicator icons, update packaging. [Stephen L Arnold]
- Add very minimal example appindicator gui. [Stephen L Arnold]

Changes
~~~~~~~
- Try setting position and gravity options, cleanup entry window bits.
  [Stephen L Arnold]
- Try rounding a Decimal for timer status. [Stephen L Arnold]

  * revert app icon back to red
- Add menu option to reset seat timer, string and extensions cleanup.
  [Stephen L Arnold]

  * add extension scripts to package data, install to pfx/lib/name
- Remove geoip menu option and rename indicator status icons. [Stephen L
  Arnold]
- Cleanup menu and doc strings, add icon for inactive state. [Stephen L
  Arnold]
- Cleanup icon names and expand tox file. [Stephen L Arnold]
- Cleanup state mechanism, compare timedeltas not strings. [Stephen L
  Arnold]
- Flesh out basic indicator bits, use static cfg for now. [Stephen L
  Arnold]
- Add terse output mode via INDICATOR_FMT environment var. [Stephen L
  Arnold]

  * prints CSV rows of per-jobtag totals plus total total

Other
~~~~~
- Enable pre-commit and apply some cleanup. [Stephen L Arnold]
- Initial commit base files plus 2 timew extensions. [Stephen L Arnold]
- Initial commit. [Steve Arnold]
