from ffflash.info import Info, info


def test_info():
    for attr, val in vars(Info()).items():
        assert getattr(info, attr) == val
        assert isinstance(val, str)


def test_info_name():
    assert info.name == info.cname.lower()


def test_info_release():
    assert info.release.startswith(info.version)


def test_info_ident():
    assert info.ident.startswith(info.name)
    assert info.ident.endswith(info.release)


def test_info_download_url():
    assert info.download_url.startswith(info.url)
    assert info.download_url.endswith('{}.tar.gz'.format(info.release))


def test_info_rst_epilog():
    assert isinstance(info.rst_epilog, str)
    e = [e for e in info.rst_epilog.split('\n') if e]
    assert e
    for attr, val in vars(info).items():
        assert '.. |info_{}| replace:: {}'.format(attr, val) in e
