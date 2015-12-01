from json import dumps

from ffflash.inc.nodelist import _nodelist_dump


def test_nodelist_dump_no_access(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _nodelist_dump(ff, 23, 42) is False

    assert tmpdir.remove() is None


def test_nodelist_dump_no_fields_present(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')
    nl = tmpdir.join('nodelist.json')

    ff = fffake(apifile, nodelist=nl, dry=True)

    assert _nodelist_dump(ff, 23, 42) is False

    assert tmpdir.remove() is None


def test_nodelist_dump_state_nodes_present(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'state': {'nodes': 0}}), 'utf-8')
    nl = tmpdir.join('nodelist.json')

    ff = fffake(apifile, nodelist=nl, dry=True)

    assert ff.api.c.get('state').get('nodes') == 0
    assert _nodelist_dump(ff, 23, 42) is True
    assert ff.api.c.get('state').get('nodes') == 23

    assert tmpdir.remove() is None


def test_nodelist_dump_state_description_present_leaves_it(tmpdir, fffake):
    descr = 'test test test'
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'state': {'description': descr}}), 'utf-8')
    nl = tmpdir.join('nodelist.json')

    ff = fffake(apifile, nodelist=nl, dry=True)

    assert ff.api.c.get('state').get('description') == descr
    assert _nodelist_dump(ff, 23, 42) is True
    assert ff.api.c.get('state').get('description') == descr

    assert tmpdir.remove() is None


def test_nodelist_dump_state_description_empty_present_fills(tmpdir, fffake):
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(dumps({'state': {'description': ''}}), 'utf-8')
    nl = tmpdir.join('nodelist.json')

    ff = fffake(apifile, nodelist=nl, dry=True)

    assert ff.api.c.get('state').get('description') == ''
    assert _nodelist_dump(ff, 23, 42) is True
    d = ff.api.c.get('state').get('description')
    assert d != ''
    assert '23 nodes' in d.lower()
    assert '42 clients' in d.lower()

    assert tmpdir.remove() is None
