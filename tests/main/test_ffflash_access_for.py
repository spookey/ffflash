from ffflash.lib.args import parsed_args
from ffflash.main import FFFlash
from json import dumps


def test_ffflash_access_for_correct_paths_but_empty(tmpdir):
    f = FFFlash(parsed_args([
        str(tmpdir.join('api_file.json')),
        '-n', str(tmpdir.join('nodelist.json')),
        '-s', str(tmpdir.join('side.yaml')), str(tmpdir.join('cars.json')),
        '-r', str(tmpdir.join('rankfile.json'))
    ]))

    assert f.access_for('nodelist') is False
    assert f.access_for('sidecars') is False
    assert f.access_for('rankfile') is False

    assert tmpdir.remove() is None


def test_ffflash_access_for_correct_paths(tmpdir):
    a = tmpdir.join('api_file.json')
    a.write_text(dumps({'a': 'b'}), 'utf-8')

    n = tmpdir.join('nodelist.json')
    n.write_text(dumps({'a': 'b'}), 'utf-8')

    assert tmpdir.listdir() == [a, n]

    f = FFFlash(parsed_args([
        str(a),
        '-n', str(n),
        '-s', str(tmpdir.join('side.yaml')), str(tmpdir.join('cars.json')),
        '-r', str(tmpdir.join('rankfile.json'))
    ]))

    assert f.load_api() is None

    assert f.access_for('nodelist') is True
    assert f.access_for('sidecars') is True
    assert f.access_for('rankfile') is True
    assert f.access_for('whatever') is False

    assert tmpdir.remove() is None
