from os import path

from ffflash.lib.locations import get_basedir


def test_get_basedir():
    assert get_basedir() == path.abspath(
        path.dirname(path.dirname(path.dirname(path.dirname(__file__))))
    )
