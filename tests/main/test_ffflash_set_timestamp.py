from json import dumps


def test_ffflash_set_timestamp_no_state_lastchange(fffake, tmpdir):
    raw = {'a': 'b'}
    apifile = tmpdir.join('phony_api_file.json')
    apifile.write_text(dumps(raw), 'utf-8')

    f = fffake(apifile, dry=True)
    assert f.api is not None
    assert f.api.c == raw

    assert f.set_timestamp() is None
    assert f.api.c == raw

    assert tmpdir.remove() is None


def test_ffflash_set_timestamp(fffake, tmpdir):
    raw = {'a': 'b', 'state': {'lastchange': 23}}
    apifile = tmpdir.join('phony_api_file.json')
    apifile.write_text(dumps(raw), 'utf-8')

    f = fffake(apifile, dry=True)
    assert f.api is not None
    assert f.api.c == raw

    assert f.set_timestamp() is None
    assert f.api.c != raw
    assert f.api.pull('a') == 'b'
    assert f.api.pull('state', 'lastchange') != 23

    assert tmpdir.remove() is None
