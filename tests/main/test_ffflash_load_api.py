from ffflash.main import FFFlash
from ffflash.lib.args import parsed_args
from json import dumps


def test_ffflash_load_api_no_json(tmpdir):
    p = tmpdir.join('phony_api_file.txt')
    p.write_text('this is no json', 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    a = parsed_args([str(p), '-d'])
    f = FFFlash(a)

    assert f
    assert f.args.APIfile == str(p)
    assert f.location == str(p)
    assert f.api is None

    assert not f.load_api()

    assert f.api is None

    assert tmpdir.remove() is None


def test_ffflash_load_api(tmpdir):
    p = tmpdir.join('phony_api_file.txt')
    api = {'a': 'b'}
    p.write_text(dumps(api), 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    a = parsed_args([str(p), '-d'])

    f = FFFlash(a)

    assert f
    assert f.api is None
    assert not f.load_api()

    assert f.args.APIfile == str(p)
    assert f.location == str(p)
    assert f.api is not None
    assert f.api.pull('a') == 'b'

    assert tmpdir.remove() is None
