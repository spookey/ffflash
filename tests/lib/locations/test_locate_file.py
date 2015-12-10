from os import path

from ffflash.lib.locations import get_basedir, locate_file


def test_locate_file():
    assert locate_file() is None

    ttgt = path.join(get_basedir(), 'test')
    assert locate_file('test', must_exist=True) is None
    assert locate_file('test', must_exist=False) == ttgt

    itgt = path.join(get_basedir(), 'ffflash', 'info.py')
    assert locate_file('ffflash', 'info.py', must_exist=False) == itgt
    assert locate_file('ffflash', 'info.py', must_exist=True) == itgt

    assert locate_file('ffflash', must_exist=False) is None
    assert locate_file('ffflash', must_exist=True) is None

    assert locate_file('ffflash', 'what', 'ever', must_exist=False) is None
    assert locate_file('ffflash', 'what', 'ever', must_exist=True) is None
