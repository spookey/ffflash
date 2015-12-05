from json import dumps, loads

from ffflash.inc.rankfile import _rankfile_dump
from ffflash.info import info


def test_rankfile_dump_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _rankfile_dump(ff, None, {}, {}) is False

    assert tmpdir.remove() is None


def test_rankfile_dump_wrong_input(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    rf = tmpdir.join('rankfile.yaml')

    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.yaml'), dry=True
    )

    assert _rankfile_dump(ff, None, None, None) is False
    assert _rankfile_dump(ff, 'test', {}, None) is False
    assert _rankfile_dump(ff, str(rf), {}, True) is False
    assert _rankfile_dump(ff, str(rf), {'nodes': []}, True) is False
    assert _rankfile_dump(ff, str(rf), {'updated_at': 'now'}, True) is False

    assert tmpdir.remove() is None


def test_rankfile_dump_data(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    rf = tmpdir.join('rankfile.yaml')
    rk = {'updated_at': 'never', 'nodes': [{'a': 'b'}, {'c': 'd'}]}

    assert tmpdir.listdir() == [apifile]
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True
    )

    assert _rankfile_dump(ff, str(rf), rk, False) is True

    assert tmpdir.listdir() == [apifile, rf]
    r = loads(rf.read_text('utf-8'))
    assert r
    assert r.get('nodes') == rk['nodes']
    assert r.get('updated_at') != 'never'
    assert r.get('version') == info.release

    assert tmpdir.remove() is None
