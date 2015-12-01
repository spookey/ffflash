from json import dumps

from ffflash.inc.nodelist import _nodelist_fetch


def test_nodelist_fetch_without_nodelist(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _nodelist_fetch(ff) is False

    assert tmpdir.remove() is None


def test_nodelist_fetch_non_existing_nodelist(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')

    for nodelist in [
        tmpdir.join('nodelist.json'),
        'http://localhost/404/not-found/does/not/exist.json'
    ]:
        ff = fffake(apifile, nodelist=nodelist, dry=True)
        assert _nodelist_fetch(ff) is False

    assert tmpdir.remove() is None


def test_nodelist_fetch_wrong_format_or_empty(tmpdir, fffake, capsys):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nl = tmpdir.join('nodelist.json')
    nl.write_text(dumps(''), 'utf-8')

    ff = fffake(apifile, nodelist=nl, dry=True)
    assert _nodelist_fetch(ff) is False
    out, err = capsys.readouterr()
    assert 'not' in out
    assert 'fetch' in out
    assert err == ''

    nl.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(apifile, nodelist=nl, dry=True)
    assert _nodelist_fetch(ff) is False
    out, err = capsys.readouterr()
    assert 'no' in out
    assert 'nodelist' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_nodelist_fetch(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = {'version': 0, 'nodes': [], 'updated_at': 'never'}
    nl = tmpdir.join('nodelist.json')
    nl.write_text(dumps(nodelist), 'utf-8')
    assert tmpdir.listdir() == [apifile, nl]

    ff = fffake(apifile, nodelist=nl, dry=True)
    assert _nodelist_fetch(ff) == nodelist

    assert tmpdir.remove() is None
