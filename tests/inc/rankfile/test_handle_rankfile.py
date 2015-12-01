from json import dumps

from ffflash.inc.rankfile import handle_rankfile


def test_handle_rankfile_without_nodelist(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert handle_rankfile(ff, {}) is False

    assert tmpdir.remove() is None


def test_handle_rankfile_without_rankfile(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(apifile, nodelist=nodelist, dry=True)
    assert ff.access_for('nodelist') is True
    assert ff.access_for('rankfile') is False
    assert handle_rankfile(ff, {'a': 'b'}) is False

    assert tmpdir.remove() is None


def test_handle_rankfile_empty_nodelist(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(
        apifile, nodelist=nodelist,
        rankfile=tmpdir.join('rankfile.json'), dry=True
    )
    assert ff.access_for('nodelist') is True
    assert ff.access_for('rankfile') is True

    assert handle_rankfile(ff, None) is False
    assert handle_rankfile(ff, {}) is False

    assert tmpdir.remove() is None


def test_handle_rankfile_trashy_rankfile(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(dumps({'a': 'b'}), 'utf-8')
    rankfile = tmpdir.join('rankfile.json')
    rankfile.write_text(dumps({'a': 'b'}), 'utf-8')

    ff = fffake(
        apifile, nodelist=nodelist,
        rankfile=rankfile, dry=True
    )

    assert handle_rankfile(ff, {'a': 'b'}) is False

    assert tmpdir.remove() is None


def test_handle_rankfile_trashy_nodelist(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(dumps({'a': 'b'}), 'utf-8')
    rankfile = tmpdir.join('rankfile.json')
    rankfile.write_text(dumps({'nodes': [], 'updated_at': 'now'}), 'utf-8')

    ff = fffake(
        apifile, nodelist=nodelist,
        rankfile=rankfile, dry=True
    )

    assert handle_rankfile(ff, {'a': 'b'}) is False

    assert tmpdir.remove() is None
