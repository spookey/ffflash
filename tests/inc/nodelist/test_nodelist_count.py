from random import choice

from ffflash.inc.nodelist import _nodelist_count


def test_nodelist_count_no_nodes_in_nodelist(tmpdir, fffake, capsys):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    assert _nodelist_count(ff, {}) == (0, 0)
    out, err = capsys.readouterr()
    assert 'empty' in out
    assert 'ERROR' in out
    assert err == ''

    assert _nodelist_count(ff, {'what': 'ever'}) == (0, 0)

    assert tmpdir.remove() is None


def test_nodelist_count(tmpdir, fffake):
    ff = fffake(tmpdir.join('api_file.json'), dry=True)

    def _n(c, o):
        return {'status': {'clients': c, 'online': o}}

    assert _nodelist_count(ff, {'nodes': [
        _n(23, True), _n(42, False)
    ]}) == (1, 23)

    dt = [(choice(range(42)), choice([True, False])) for _ in range(23)]

    assert _nodelist_count(ff, {'nodes': [
        _n(c, o) for c, o in dt
    ]}) == (
        sum([o for _, o in dt]),
        sum([c for c, o in dt if o])
    )

    assert tmpdir.remove() is None
