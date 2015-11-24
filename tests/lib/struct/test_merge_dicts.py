from ffflash.lib.struct import merge_dicts


def test_merge_dicts_on_faulty_input():
    assert merge_dicts(None, None) is None
    assert merge_dicts({}, None) is None
    assert merge_dicts(None, {}) is None
    assert merge_dicts('a', {}) == 'a'
    assert merge_dicts({}, 'b') == 'b'

    assert merge_dicts(False, {'a': 'b'}) is False
    assert merge_dicts({'a': 'b'}, False) is False
    assert merge_dicts('a', {'b': 'c'}) == 'a'
    assert merge_dicts({'a': 'b'}, 'c') == 'c'


def test_merge_dicts_simple():
    assert merge_dicts({}, {}) == {}

    assert merge_dicts(
        {'a': 'b'}, {}
    ) == {'a': 'b'}

    assert merge_dicts(
        {'a': 'b'}, {'a': 'c'}
    ) == {'a': 'c'}

    assert merge_dicts(
        {'a': 'b'}, {'c': 'd'}
    ) == {'a': 'b', 'c': 'd'}

    assert merge_dicts(
        {'a': {'b': {'c': 'd'}}},
        {'a': {'b': {'c': 'e'}}}
    ) == {'a': {'b': {'c': 'e'}}}

    assert merge_dicts(
        {'a': {'b': {'c': 'd'}}},
        {'a': {'b': {'e': 'f'}}}
    ) == {'a': {'b': {'c': 'd', 'e': 'f'}}}


def test_merge_dicts_nested():
    A = {'a': {'b': {'c': {'d': 'e'}}}}
    Z = {'z': {'y': {'x': {'w': 'v'}}}}

    assert merge_dicts(
        A['a']['b']['c'], Z['z']['y']['x']
    ) == {'d': 'e', 'w': 'v'}

    assert merge_dicts(
        A['a']['b'], Z['z']['y']
    ) == {'c': {'d': 'e'}, 'x': {'w': 'v'}}

    assert merge_dicts(
        A['a'], Z['z']
    ) == {'b': {'c': {'d': 'e'}}, 'y': {'x': {'w': 'v'}}}

    assert merge_dicts(
        A, Z
    ) == {'a': {'b': {'c': {'d': 'e'}}}, 'z': {'y': {'x': {'w': 'v'}}}}
