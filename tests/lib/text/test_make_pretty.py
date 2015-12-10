from pprint import pformat

from ffflash.lib.text import make_pretty


def test_make_pretty_unprintables():
    for u in [
        list, dict, set, str, int, bool, type,
        vars, dir, len, max, min, range, isinstance,
        pformat, make_pretty
    ]:
        assert make_pretty(u) is None


def test_make_pretty():
    for u in [
        None, False, True, 0, 23, 42, 13.37,
        list(), dict(), set(), 'a', 'b', ['c', 'd'],
        {'e': 'f'}, {'g', 'h', 'i'}
    ]:
        assert make_pretty(u) == pformat(u)
