from datetime import timedelta

from munch import Munch

from timew_status.utils import (
    do_install,
    get_config,
    get_delta_limits,
    get_state_icon,
    get_userdirs,
    parse_for_tag,
)

CFG = {
    "day_max": "08:00",
    "day_snooze": "01:00",
    "seat_max": "01:30",
    "seat_snooze": "00:40",
    "use_symbolic_icons": False,
    "extensions_dir": "~/.timewarrior/extensions",
    "install_dir": "lib/timew-addons/extensions",
    "install_prefix": "/usr",
}

start_txt = """
Note: '"vct-sw,refactor timew indicator config to yaml"' is a new tag.
Tracking "vct-sw,refactor timew indicator config to yaml"
  Started 2024-08-04T20:32:05
  Current                  05
  Total               0:00:00
"""

stop_text = """
Recorded "vct-sw,refactor timew indicator config to yaml"
  Started 2024-08-05T10:11:36
  Ended              12:44:48
  Total               2:33:12
"""


def test_do_install(script_loc, tmpdir_session):
    cfg = Munch.fromDict(CFG)
    # destination dir
    tgt_dir = tmpdir_session / 'extensions'
    tgt_dir.mkdir(exist_ok=True)
    cfg.extensions_dir = str(tgt_dir)
    # source dir
    cfg.install_prefix = str(script_loc)
    cfg.install_dir = 'testdata'
    # print(cfg)

    ret = do_install(cfg.toDict())
    print(ret)


def test_get_config():
    cfgobj, cfgfile = get_config()
    assert repr(cfgobj).startswith("Munch({'")
    assert cfgfile.name == 'config.yaml'
    print(f'\n{cfgfile.name}')
    print(cfgobj)


def test_get_delta_limits():
    for td in get_delta_limits(CFG):
        assert isinstance(td, timedelta)
        print(td)
    tds = get_delta_limits(CFG)
    print(len(tds))
    assert isinstance(tds, tuple)
    assert len(tds) == 4


def test_get_state_icon():
    states = ['INACTIVE', 'ACTIVE', 'WARNING', 'ERROR', 'APP']
    for state in states:
        icon = get_state_icon(state, CFG)
        assert 'timew' in icon or 'dialog' in icon
        print(icon)


def test_get_state_icon_fallback():
    states = ['INACTIVE', 'ACTIVE', 'WARNING', 'ERROR', 'APP']
    cfg = Munch.fromDict(CFG)
    cfg.use_symbolic_icons = True
    for state in states:
        icon = get_state_icon(state, cfg.toDict())
        assert 'symbolic' in icon
        print(icon)


def test_get_userdirs():
    udir = get_userdirs()
    print(f'\nuserdir: {udir}')


def test_parse_for_tag():
    ret = parse_for_tag(start_txt)
    print(f'\n{ret}')
    ret = parse_for_tag(stop_text)
    print(ret)
