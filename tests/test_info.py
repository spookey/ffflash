from ffflash.info import Info, info


def test_info():
    for attr, val in Info().__dict__.items():
        assert getattr(info, attr) == val


def test_info_release():
    assert info.release.startswith(info.version)


def test_info_download_url():
    assert info.download_url.startswith(info.url)
    assert info.download_url.endswith('{}.tar.gz'.format(info.release))
