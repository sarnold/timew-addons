Changelog
=========


0.3.2 (2025-03-23)
------------------

Changes
~~~~~~~
- (re)generate changelog after yet another config update. [Stephen L
  Arnold]

  * needs the right regex filters to restore missing commit info
- Include debs in release workflow, add to release. [Stephen L Arnold]
- Add tox lint cmd and cleanup some subprocess lint. [Stephen L Arnold]
- Bump debian package files to jammy with metadata patch. [Stephen L
  Arnold]
- Start more cleanup. [Stephen L Arnold]

Fixes
~~~~~
- Make sure console cov report shows src path, update changelog.
  [Stephen L Arnold]
- Use the right (default) branch for push event. [Stephen L Arnold]
- Add explicit read permissions to pre-commit check. [Stephen L Arnold]
- Add ubuntu pkg deps to pylint workflow, restore bandit config.
  [Stephen L Arnold]


0.3.1 (2025-03-23)
------------------

Changes
~~~~~~~
- Apply reusable workflows to release.yml, update changelog. [Stephen L
  Arnold]
- Still tweaking the exact project.license and ci bits. [Stephen L
  Arnold]

  * relax sphinx version requirement, restore sphinxcontrib-apidoc for now
  * update readme with patch blurb, add pre-commit check workflow
  * update pre-commit-config, apply formatting update
- Split PyGObject version depss across python versions. [Stephen L
  Arnold]

  * in pyproject.toml PyGObject==v3.50.0 up to 3.12 and in ubuntu CI
    install libgirepository-2.0-dev for ubuntu 24.04+
  * this will break some CI bits until new PPA packages with their
    own version-specific patches are available
- Migrate package metadata yo pyproject.toml, move flake8 cfg. [Stephen
  L Arnold]

  * flake8 gets its own config file, setup.py goes away
- Update about() and update debian install in readme, update .gitignore.
  [Stephen Arnold]
- Set larger max for pre-commit large file check. [Stephen Arnold]
- Update release workflow with deb package artifacts. [Stephen Arnold]

  * also enable deb package builds on push to main

Fixes
~~~~~
- Use correct indentation in updated workflows. [Stephen L Arnold]
- Eliminate bandit warning about partial path. [Stephen L Arnold]
- Update python and action versions, add workflow permissions. [Stephen
  L Arnold]

  * also sync new python versions and cleanup tox file
- Remove License classifiers to silence setuptools error. [Stephen L
  Arnold]

  * certain old-style metadata becomes a hard error in python 3.13
- Update debian files in pkging workflow and extension shebangs.
  [Stephen Arnold]

  * start some readme refactoring


0.3.0 (2024-10-13)
------------------

Changes
~~~~~~~
- Add more tests, cleanup readme, build some debs. [Stephen Arnold]
- Use future annotations workaround on python 3.8. [Stephen Arnold]

  * the above import trick is correct for ``get_state_str()`` signature
- Cleanup docstrings and desktop file, update pkg metadata and readme.
  [Stephen Arnold]

Fixes
~~~~~
- Add still more annotations, adjust and apply pre-commit fixes.
  [Stephen Arnold]
- Complete error fix, more import cleanup, add helper func and a test.
  [Stephen Arnold]

  * this commit removes support for legacy AppIndicator3 in favor of
    AyatanaAppIndicator3 only
- Refactoring cleanup, add type hints/ignores and fix an error. [Stephen
  Arnold]

  * mypy helped find an error, but we still need to ignore the optional
    munch YAML attributes
  * update flake8 config bits to allow one more char of line length


0.2.1 (2024-08-29)
------------------

Changes
~~~~~~~
- Add yet another misc docstring. [Stephen Arnold]

Fixes
~~~~~
- Use correct signature for about dialog, cleanup app string. [Stephen
  Arnold]
- Use correct signature for about dialog, cleanup app string. [Stephen
  Arnold]


0.2.0 (2024-08-27)
------------------

New
~~~
- Add menu option to install extensions, beef up tests. [Stephen Arnold]

  * add some pytest fixtures and more tests, improve readme
  * refactor for correctness and testability, cleanup packaging

Changes
~~~~~~~
- Refactor doc extensions to use apidoc, add docs logo icon. [Stephen
  Arnold]

  * cleanup more docstrings and sphinx modules, update changelog again
- Update changelog for next version, remove sphinx git hash. [Stephen
  Arnold]

  * also suppress duplicate label warnings from autosectionlabel
- Respin doc symlinks using vendored copies. [Stephen Arnold]
- Update docs and packaging, post refactoring cleanup. [Stephen Arnold]

  * add symlinks so icons are available for both sphinx and GH rendering
  * optionally disable seat-timer by setting params to 00:00

Fixes
~~~~~
- Make sure release docs have all the package deps. [Steve Arnold]


0.1.1 (2024-08-20)
------------------

New
~~~
- Add vendoring bits for stand-alone sum repo. [Steve Arnold]
- Update readme, add sphinx docs build, cleanup docstrings. [Stephen L
  Arnold]

  * add example extension based on totals for use without jtag split
  * update base config with extension_script key for script name
- Add a changelog plus .gitchangelog.rc and update tox env. [Stephen L
  Arnold]
- Reset seat counter on stop after err, plus cleanup. [Stephen L Arnold]

  * abstract out delta_limits, hide some prints behind DEBUG
- Wire up seat-time counter and related value checks. [Stephen L Arnold]
- Add basic CI workflow for github and update readme. [Stephen L Arnold]
- Add tag editing widget for start cmd plus a simple test. [Stephen L
  Arnold]

  * update config with more tag parameters, allow last_tag reuse
- Add default yaml config file with platform user dirs. [Stephen L
  Arnold]
- Add app and indicator icons, update packaging. [Stephen L Arnold]
- Add very minimal example appindicator gui. [Stephen L Arnold]

Changes
~~~~~~~
- Add config option to select symbolic icons instead of default. [Steve
  Arnold]

  * revert the .keepdir bits and cleanup sphinx config and index
  * update changelog and get ready for release version, cleanup
    docs CI workflows
- Still more readme updates and a docstring tweak. [Stephen L Arnold]
- (re)enable sphinx builds in github ci, push to gh-pages. [Stephen L
  Arnold]
- Update ci workflow and add release workflow. [Stephen L Arnold]
- Try setting position and gravity options, cleanup entry window bits.
  [Stephen L Arnold]
- Try rounding a Decimal for timer status. [Stephen L Arnold]

  * revert app icon back to red
- Simplify and remove a dep, use base config instead of file. [Stephen L
  Arnold]

  * pass one more env var to extension script, sanitize for mypy
- Add menu option to reset seat timer, string and extensions cleanup.
  [Stephen L Arnold]

  * add extension scripts to package data, install to pfx/lib/name
- Refactor config handling, add another test, big readme update.
  [Stephen L Arnold]
- Cleanup tag handling, split last tag from widget string. [Stephen L
  Arnold]

  * use separate dict for passing TAG string instead of mangling CFG
  * select tag string via config option where tag is actually applied
- Remove geoip menu option and rename indicator status icons. [Stephen L
  Arnold]
- Cleanup menu and doc strings, add icon for inactive state. [Stephen L
  Arnold]
- Cleanup and sync flake8 config, add extra opt for pep8speaks. [Stephen
  L Arnold]
- Cleanup icon names and expand tox file. [Stephen L Arnold]
- Cleanup state mechanism, compare timedeltas not strings. [Stephen L
  Arnold]
- Flesh out basic indicator bits, use static cfg for now. [Stephen L
  Arnold]
- Add terse output mode via INDICATOR_FMT environment var. [Stephen L
  Arnold]

  * prints CSV rows of per-jobtag totals plus total total

Fixes
~~~~~
- Update doc deploy workflows per current deploy action docs. [Steve
  Arnold]

  * use permissions instead of the older github token setting
- Add directory keepers to required sphinx dirs, change to _build.
  [Steve Arnold]

  * update .gitignore (again) after this commit
- Even more docstring and readme/rst doc cleanup. [Stephen L Arnold]
- Cleanup some oddball link anchors flagged by sphinx check. [Stephen L
  Arnold]

Other
~~~~~
- Enable pre-commit and apply some cleanup. [Stephen L Arnold]
- Initial commit base files plus 2 timew extensions. [Stephen L Arnold]
- Initial commit. [Steve Arnold]
