from json import dumps

from ffflash.lib.args import parsed_args
from ffflash.main import FFFlash


def test_ffflash_load_api_no_json(tmpdir):
    p = tmpdir.join('phony_api_file.txt')
    p.write_text('this is no json', 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    f = FFFlash(parsed_args([str(p), '-d']))

    assert f
    assert f.args.APIfile == str(p)
    assert f.location == str(p)
    assert f.api is None

    assert f.load_api() is None

    assert f.api is None

    assert tmpdir.remove() is None


def test_ffflash_load_api(tmpdir):
    p = tmpdir.join('phony_api_file.json')
    api = {'a': 'b'}
    p.write_text(dumps(api), 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    f = FFFlash(parsed_args([str(p), '-d']))

    assert f
    assert f.api is None

    assert f.load_api() is None

    assert f.api is not None
    assert f.api.pull('a') == 'b'

    assert tmpdir.remove() is None


def test_ffflash_reload_api(tmpdir):
    p = tmpdir.join('phony_api_file.json')
    api = {'a': 'b'}
    p.write_text(dumps(api), 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    f = FFFlash(parsed_args([str(p), '-d']))

    assert f
    assert f.api is None

    assert f.load_api() is None

    assert f.api is not None
    assert f.api.pull('a') == 'b'
    assert f.api.push('c', 'a') is None

    assert f.load_api() is None
    assert f.api.pull('a') != 'b'
    assert f.api.pull('a') == 'c'

    assert tmpdir.remove() is None
