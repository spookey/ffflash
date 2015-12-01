from json import dumps
from random import choice

from ffflash.inc.nodelist import handle_nodelist


def test_handle_nodelist_without_nodelist(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert handle_nodelist(ff) is False

    assert tmpdir.remove() is None


def test_handle_nodelist_invalid_nodelist_locations(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    for nodelist in [
        tmpdir.join('nodelist.json'),
        'http://localhost/404/not-found/does/not/exist.json',
    ]:

        ff = fffake(apifile, nodelist=nodelist, dry=True)
        assert handle_nodelist(ff) is False

    assert tmpdir.remove() is None


def test_handle_nodelist_empty_nodelist(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nl = tmpdir.join('nodelist.json')
    nl.write_text(dumps(''), 'utf-8')

    ff = fffake(apifile, nodelist=nl, dry=True)
    assert handle_nodelist(ff) is False

    nl.write_text(dumps({'a': 'b'}), 'utf-8')
    ff = fffake(apifile, nodelist=nl, dry=True)
    assert handle_nodelist(ff) is False

    nl.write_text(dumps({
        'version': 1, 'nodes': [{}], 'updated_at': 'never'
    }), 'utf-8')
    ff = fffake(apifile, nodelist=nl, dry=True)
    assert handle_nodelist(ff) is False

    assert tmpdir.remove() is None


def test_handle_nodelist_count_some_nodes(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({
        'state': {'nodes': 0, 'description': ''}
    }), 'utf-8')
    nl = tmpdir.join('nodelist.json')

    def _n(c, o):
        return {'status': {'clients': c, 'online': o}}

    dt = [(choice(range(42)), choice([True, False])) for _ in range(23)]
    nl.write_text(dumps({
        'version': 1, 'nodes': [
            _n(c, o) for c, o in dt
        ], 'updated_at': 'never'
    }), 'utf-8')

    ff = fffake(apifile, nodelist=nl, dry=True)

    assert ff.api.c.get('state').get('nodes') == 0
    assert handle_nodelist(ff) is True
    assert ff.api.c.get('state').get('nodes') == sum([o for _, o in dt])

    assert tmpdir.remove() is None


def test_handle_nodelist_launch_rankfile(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nl = tmpdir.join('nodelist.json')
    nl.write_text(dumps({
        'version': 1, 'nodes': [{}], 'updated_at': 'never'
    }), 'utf-8')
    rf = tmpdir.join('rankfile.json')

    ff = fffake(apifile, nodelist=nl, rankfile=rf, dry=True)

    assert handle_nodelist(ff) is False

    assert tmpdir.remove() is None
