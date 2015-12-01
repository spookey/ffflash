from json import dumps

from ffflash.inc.rankfile import _rankfile_score


def test_rankfile_score_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _rankfile_score(ff, {}, {}) is False

    assert tmpdir.remove() is None


def test_rankfile_score_wrong_input(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True
    )

    assert _rankfile_score(ff, None, None) is False
    assert _rankfile_score(ff, {}, {}) is False
    assert _rankfile_score(ff, {'nodes': []}, {}) is False
    assert _rankfile_score(ff, {}, {'nodes': []}) is False

    assert tmpdir.remove() is None


def test_rankfile_score_nodes_without_id(tmpdir, fffake, capsys):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True, verbose=True
    )

    assert _rankfile_score(ff, {'nodes': []}, {'nodes': []}) == {'nodes': []}
    assert _rankfile_score(ff, {'nodes': []}, {'nodes': [{}]}) == {'nodes': []}
    out, err = capsys.readouterr()
    assert 'without' in out
    assert 'id' in out
    assert err == ''

    assert tmpdir.remove() is None


def test_rankfile_score_spot_known_nodes(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True, verbose=True
    )

    res = _rankfile_score(ff, {'nodes': [
        {'id': 'a', 'score': 23},
        {'id': 'b', 'score': 42},
    ]}, {'nodes': [
        {'id': 'a', 'name': 'A', 'status': {'online': True}},
        {'id': 'b', 'name': 'B'}
    ]})
    assert res.get('nodes')
    for n in res.get('nodes'):
        assert n['clients'] == 0
        assert n['id'] == n['name'].lower()
        if n['id'] == 'a':
            assert n['online'] is True
            assert n['score'] == (23 + ff.args.rankonline)
        else:
            assert n['online'] is False
            assert n['score'] == (42 - ff.args.rankoffline)

    assert tmpdir.remove() is None


def test_rankfile_score_welcome_new_nodes(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True, verbose=True
    )

    res = _rankfile_score(ff, {'nodes': []}, {'nodes': [
        {'id': 'a', 'name': 'A', 'status': {'online': True}},
        {'id': 'b', 'name': 'B'}
    ]})
    assert res.get('nodes')
    for n in res.get('nodes'):
        assert n['clients'] == 0
        assert n['id'] == n['name'].lower()
        if n['id'] == 'a':
            assert n['online'] is True
            assert n['score'] == (ff.args.rankwelcome + ff.args.rankonline)
        else:
            assert n['online'] is False
            assert n['score'] == (ff.args.rankwelcome - ff.args.rankoffline)

    assert tmpdir.remove() is None


def test_rankfile_score_rank_known_nodes(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(
        apifile, nodelist=tmpdir.join('nodelist.json'),
        rankfile=tmpdir.join('rankfile.json'), dry=True, verbose=True
    )

    res = _rankfile_score(ff, {'nodes': [
        {'id': 'a', 'score': 23},
        {'id': 'b', 'score': 42},
    ]}, {'nodes': [
        {'id': 'a', 'name': 'A', 'status': {'online': True, 'clients': 5}},
        {'id': 'b', 'name': 'B', 'position': {'lat': 0.0, 'lon': 0.0}}
    ]})
    assert res.get('nodes')
    for n in res.get('nodes'):
        assert n['id'] == n['name'].lower()
        if n['id'] == 'a':
            assert n['online'] is True
            assert n['score'] == (
                23 + ff.args.rankonline + (5 * ff.args.rankclients)
            )
        else:
            assert n['online'] is False
            assert n['score'] == (
                42 - ff.args.rankoffline + ff.args.rankposition
            )

    assert tmpdir.remove() is None
