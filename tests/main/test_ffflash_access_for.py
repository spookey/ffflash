from json import dumps


def test_ffflash_access_for_with_empty_paths(tmpdir, fffake):
    f = fffake(
        tmpdir.join('api_file.json'),
        nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'),
        sidecars=[tmpdir.join('side.yaml'), tmpdir.join('cars.yaml')]
    )

    assert f.access_for('api') is False
    assert f.access_for('nodelist') is False
    assert f.access_for('sidecars') is False
    assert f.access_for('rankfile') is False
    assert f.access_for('whatever') is False

    assert tmpdir.remove() is None


def test_ffflash_access_for_with_correct_paths(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(dumps({'a': 'b'}), 'utf-8')

    assert tmpdir.listdir() == [apifile, nodelist]

    f = fffake(
        apifile, nodelist=nodelist, rankfile=tmpdir.join('rankfile.json'),
        sidecars=[tmpdir.join('side.yaml'), tmpdir.join('cars.yaml')]
    )

    assert f.access_for('api') is True
    assert f.access_for('nodelist') is True
    assert f.access_for('sidecars') is True
    assert f.access_for('rankfile') is True
    assert f.access_for('whatever') is False

    assert tmpdir.remove() is None
