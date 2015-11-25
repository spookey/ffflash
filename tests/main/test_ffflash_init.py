from ffflash.lib.args import parsed_args
from ffflash.main import FFFlash


def test_ffflash_init_apifile_does_not_exist(tmpdir):
    p = tmpdir.join('phony_api_file.json')
    assert tmpdir.listdir() == []

    a = parsed_args([str(p), '-d'])
    f = FFFlash(a)

    assert f
    assert f.args == a
    assert f.args.APIfile == str(p)
    assert f.args.dry is True
    assert f.location is None
    assert f.api is None

    assert tmpdir.remove() is None


def test_ffflash_init_apifile_does_exist(tmpdir):
    p = tmpdir.join('phony_api_file.json')
    p.write_text('does not matter', 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    a = parsed_args([str(p), '-d'])
    f = FFFlash(a)

    assert f
    assert f.args == a
    assert f.args.APIfile == str(p)
    assert f.args.dry is True
    assert f.location == str(p)
    assert f.api is None

    assert tmpdir.remove() is None
