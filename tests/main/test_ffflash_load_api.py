from json import dumps


def test_ffflash_load_api_this_is_no_json(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.txt')
    apifile.write_text('this is no json', 'utf-8')
    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)
    assert f

    assert f.args.APIfile == str(apifile)
    assert f.location == str(apifile)
    assert f.api is None

    assert tmpdir.remove() is None


def test_ffflash_load_api(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    c = {'a': 'b'}
    apifile.write_text(dumps(c), 'utf-8')
    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)
    assert f

    assert f.api is not None
    assert f.api.c == c
    assert f.api.pull('a') == 'b'

    assert tmpdir.remove() is None


def test_ffflash_reload_api(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    c = {'a': 'b'}
    apifile.write_text(dumps(c), 'utf-8')
    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)
    assert f

    assert f.api is not None
    assert f.api.c == c
    assert f.api.pull('a') == 'b'

    assert f.api.push('c', 'a') is None
    assert f.api.pull('a') == 'c'
    assert f.load_api() is None
    assert f.api.pull('a') != 'b'
    assert f.api.pull('a') == 'c'

    assert tmpdir.remove() is None
