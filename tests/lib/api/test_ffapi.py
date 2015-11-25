from copy import deepcopy
from pprint import pformat

from ffflash.lib.api import FFApi

A = {
    'a': {'b': 'c', 'd': ['e', 'f']},
    'g': ['h'],
    'i': {'j': 23}
}


def test_ffapi_init_content():
    f = FFApi(deepcopy(A))
    assert f.c == A


def test_ffapi_pull():
    f = FFApi(deepcopy(A))
    assert f.pull() is None
    assert f.pull('a') == A.get('a')
    assert f.pull('a', 'b') == A.get('a').get('b')
    assert f.pull('a', 'b', 'c') is None
    assert f.pull('a', 'd') == A.get('a').get('d')
    assert f.pull('a', 'd', 'e') is None
    assert f.pull('a', 'd', 'f') is None
    assert f.pull('g') == A.get('g')
    assert f.pull('g', 'h') is None
    assert f.pull('h') is None
    assert f.pull('i') == A.get('i')
    assert f.pull('i', 'j') == A.get('i').get('j')


def test_ffapi_push():
    f = FFApi(deepcopy(A))
    assert f.push(None) is None
    assert f.c == A

    assert f.push({'x': 'y'}, 'a', 'b') is None
    A['a']['b'] = {'x': 'y'}

    assert f.push(1337, 'a', 'd') is None
    A['a']['d'] = 1337

    assert f.push([23, 42], 'g') is None
    A['g'] = [23, 42]

    assert f.push('test', 'i', 'j') is None
    A['i']['j'] = 'test'

    assert f.c == A


def test_ffapi_show():
    for tc in [
        {}, {'a': 'b'}, {'a': {'b': 'c'}}, {'a': ['b', 'c']}
    ]:
        assert FFApi(tc).show() == pformat(tc)


def test_ffapi_timestamp_no_field():
    raw = {'a': 'b'}
    f = FFApi(deepcopy(raw))
    assert f.c == raw
    f.timestamp()
    assert f.c == raw


def test_ffapi_timestamp():
    raw = {'a': 'b', 'state': {'lastchange': 23}}
    f = FFApi(deepcopy(raw))
    assert f.c == raw
    f.timestamp()
    assert f.c != raw
