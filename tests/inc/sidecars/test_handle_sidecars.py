from json import dumps

from ffflash.inc.sidecars import handle_sidecars


def test_handle_sidecars_without_sidecars(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert handle_sidecars(ff) is False

    assert tmpdir.remove() is None


def test_handle_sidecars_wrong_keys(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('sc.json')

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert handle_sidecars(ff) is False

    assert tmpdir.remove() is None


def test_handle_sidecarts_invalid_filenames(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(apifile, sidecars=[
        str(tmpdir.join('sc.txt')),
        str(tmpdir.join('does.not.exist.json')),
        str(tmpdir.join('a..b.yaml')),
    ], dry=True)

    assert handle_sidecars(ff) is False

    assert tmpdir.remove() is None


def test_handle_sidecars_self_not_existing(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('a.json')
    assert tmpdir.listdir() == [apifile]

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert handle_sidecars(ff) is True

    assert tmpdir.listdir() == [sc, apifile]

    assert tmpdir.remove() is None


def test_handle_sidecars_existing_overwrites_api(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    sc = tmpdir.join('a.json')
    sc.write_text(dumps('c'), 'utf-8')
    assert tmpdir.listdir() == [sc, apifile]

    ff = fffake(apifile, sidecars=[sc], dry=True)

    assert handle_sidecars(ff) is True

    assert ff.api.c.get('a') == 'c'

    assert tmpdir.remove() is None
