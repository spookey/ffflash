def test_ffflash_init_empty_apifile(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    assert tmpdir.listdir() == []

    f = fffake(apifile, dry=True)

    assert f
    assert f.args
    assert f.args.APIfile == str(apifile)
    assert f.args.dry is True
    assert f.location is None
    assert f.api is None

    assert tmpdir.remove() is None


def test_ffflash_init_with_apifile(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    apifile.write_text('does not matter', 'utf-8')
    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)

    assert f
    assert f.args
    assert f.args.APIfile == str(apifile)
    assert f.args.dry is True
    assert f.location == str(apifile)
    assert f.api is None

    assert tmpdir.remove() is None
