from ffflash.inc.nodelist import handle_nodelist


def test_handle_nodelist_without_nodelist(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert handle_nodelist(ff) is False

    assert tmpdir.remove() is None
