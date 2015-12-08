from json import dumps

from ffflash.inc.rankfile import _rankfile_load


def test_rankfile_load_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _rankfile_load(ff) == (False, None)

    assert tmpdir.remove() is None


def test_rankfile_load_wrong_location(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    rf = tmpdir.mkdir('rankfolder')
    assert tmpdir.listdir() == [apifile, rf]
    assert rf.listdir() == []

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'), rankfile=rf, dry=True
    )
    assert ff.access_for('api') is True
    assert ff.access_for('nodelist') is True
    assert ff.access_for('rankfile') is True

    assert _rankfile_load(ff) == (False, None)

    assert tmpdir.remove() is None


def test_rankfile_load_wrong_extension(tmpdir, fffake, capsys):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.txt'), dry=True
    )
    assert ff.access_for('api') is True
    assert ff.access_for('nodelist') is True
    assert ff.access_for('rankfile') is True

    assert _rankfile_load(ff) == (False, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'json' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_rankfile_load_non_existing_file(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    rf = tmpdir.join('rankfile.json')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=rf, dry=True
    )

    assert _rankfile_load(ff) == (
        str(rf), {'updated_at': 'never', 'nodes': []}
    )

    assert tmpdir.remove() is None


def test_rankfile_load_existing_file_with_errors(tmpdir, fffake, capsys):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')

    rf = tmpdir.join('rankfile.json')
    rf.write_text(dumps(None), 'utf-8')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=rf, dry=True
    )
    assert _rankfile_load(ff) == (False, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'could' in out
    assert 'not' in out
    assert err == ''

    rf = tmpdir.join('rankfile.json')
    rf.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=rf, dry=True
    )
    assert _rankfile_load(ff) == (False, None)
    out, err = capsys.readouterr()
    assert 'ERROR' in out
    assert 'is' in out
    assert 'no' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_rankfile_load_existing_file(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    rankfile = {'updated_at': 'now', 'nodes': [{'a': 'b'}, {'c': 'd'}]}
    rf = tmpdir.join('rankfile.json')
    rf.write_text(dumps(rankfile), 'utf-8')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=rf, dry=True
    )
    assert _rankfile_load(ff) == (str(rf), rankfile)

    assert tmpdir.remove() is None
