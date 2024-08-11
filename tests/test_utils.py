from timew_status.utils import get_config, get_userdirs, parse_for_tag

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


def test_get_config():
    cfgobj, cfgfile = get_config()
    assert repr(cfgobj).startswith("Munch({'")
    assert cfgfile.name == 'config.yaml'
    print(f'\n{cfgfile.name}')
    print(cfgobj)


def test_get_userdirs():
    udir = get_userdirs()
    print(f'\nuserdir: {udir}')


def test_parse_for_tag():
    ret = parse_for_tag(start_txt)
    print(f'\n{ret}')
    ret = parse_for_tag(stop_text)
    print(ret)
