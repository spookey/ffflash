def test_ffflash_log_non_verbose(tmpdir, capsys, fffake):
    f = fffake(tmpdir.join('phony_api_file.json'), dry=True)

    assert f.log('error message', level=False) is False
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'ERROR\terror message\n'

    assert f.log('warn message', level=None) is None
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'WARN\twarn message\n'

    assert f.log('info message', level=True) is True
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert f.log('info message') is True
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''

    assert f.log('custom message', level='whatever') == 'whatever'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'WHATEVER\tcustom message\n'

    assert tmpdir.remove() is None


def test_ffflash_log_verbose(tmpdir, capsys, fffake):
    f = fffake(tmpdir.join('phony_api_file.json'), dry=True, verbose=True)

    assert f.log('error message', level=False) is False
    out, err = capsys.readouterr()
    assert out == 'ERROR\terror message\n'

    assert f.log('warn message', level=None) is None
    out, err = capsys.readouterr()
    assert out == 'WARN\twarn message\n'

    assert f.log('info message', level=True) is True
    out, err = capsys.readouterr()
    assert out == 'INFO\tinfo message\n'

    assert f.log('custom message', level='whatever') == 'whatever'
    out, err = capsys.readouterr()
    assert out == 'WHATEVER\tcustom message\n'

    assert tmpdir.remove() is None


def test_ffflash_log_level_returns(tmpdir, fffake):
    f = fffake(tmpdir.join('phony_api_file.json'), dry=True)

    assert f.log('message', level=False) is False
    assert f.log('message', level=None) is None
    assert f.log('message', level=True) is True
    assert f.log('message', level='testing') == 'testing'
    assert f.log('message', level={}) == {}
    assert f.log('message', level=[]) == []

    assert tmpdir.remove() is None
