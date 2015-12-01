from json import dumps

from ffflash.inc.sidecars import _sidecar_load


def test_sidecar_load_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _sidecar_load(ff, '/no/path/sc.yaml', ['sc'], True) is False

    assert tmpdir.remove() is None


def test_sidecar_load_not_existing_key(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('sc.json')

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert _sidecar_load(ff, str(sc), ['sc'], False) is None

    assert tmpdir.remove() is None


def test_sidecar_load_but_self_not_existing(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('a.json')
    assert tmpdir.listdir() == [apifile]

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert _sidecar_load(ff, str(sc), ['a'], False) is 'b'

    assert tmpdir.remove() is None


def test_sidecar_load_existing_overwrites_api(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('a.json')
    sc.write_text(dumps('c'), 'utf-8')

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert _sidecar_load(ff, str(sc), ['a'], False) is 'c'

    assert tmpdir.remove() is None
