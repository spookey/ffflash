from ffflash.inc.sidecars import handle_sidecars


def test_handle_sidecars_without_sidecars(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert handle_sidecars(ff) is False

    assert tmpdir.remove() is None
