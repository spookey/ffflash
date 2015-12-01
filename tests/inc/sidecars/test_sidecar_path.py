from ffflash.inc.sidecars import _sidecar_path


def test_sidecar_path_is_folder(tmpdir, fffake, capsys):
    sc = tmpdir.ensure('sidecar', dir=True)

    ff = fffake(tmpdir.join('api_file.json', dry=True))
    assert tmpdir.listdir() == [sc]

    assert _sidecar_path(ff, str(sc)) == (False, None, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'folder' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_sidecar_path_wrong_extension(tmpdir, fffake, capsys):
    ff = fffake(tmpdir.join('api_file.json', dry=True))

    assert _sidecar_path(ff, 'yolo.swag') == (False, None, None)
    assert _sidecar_path(ff, 'swag.yolo') == (False, None, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'json' in out
    assert 'yaml' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_sidecar_path_empty_names(tmpdir, fffake, capsys):
    ff = fffake(tmpdir.join('api_file.json', dry=True))

    assert _sidecar_path(ff, 'yolo..yaml') == (False, None, None)
    assert _sidecar_path(ff, 'swag..yolo.json') == (False, None, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'name' in out
    assert 'invalid' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_sidecar_path(tmpdir, fffake, capsys):
    s = tmpdir.join('yolo.yaml')
    c = tmpdir.join('swag.json')
    sc = tmpdir.join('yolo.swag.json')

    ff = fffake(tmpdir.join('api_file.json', dry=True))

    assert _sidecar_path(ff, str(s)) == (str(s), ['yolo'], True)
    assert _sidecar_path(ff, str(c)) == (str(c), ['swag'], False)
    assert _sidecar_path(ff, str(sc)) == (str(sc), ['yolo', 'swag'], False)

    assert tmpdir.remove() is None
