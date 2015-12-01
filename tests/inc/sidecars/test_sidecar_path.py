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
