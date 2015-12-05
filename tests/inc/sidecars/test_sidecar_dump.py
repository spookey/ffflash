from json import dumps, loads

from ffflash.inc.sidecars import _sidecar_dump


def test_sidecar_dump_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _sidecar_dump(ff, '/no/path/sc.yaml', {}, ['sc'], True) is False

    assert tmpdir.remove() is None


def test_sidecar_dump_not_existing_key(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('sc.json')

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert _sidecar_dump(ff, str(sc), {}, ['sc'], False) is None

    assert tmpdir.remove() is None


def test_sidecar_dump_but_self_not_existing(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('a.json')
    assert tmpdir.listdir() == [apifile]

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert _sidecar_dump(ff, str(sc), 'c', ['a'], False) is True

    assert ff.api.c.get('a') == 'c'
    assert sorted(tmpdir.listdir()) == sorted([sc, apifile])
    assert loads(sc.read_text('utf-8')) == 'c'

    assert tmpdir.remove() is None
