from copy import deepcopy
from json import dumps, loads


def test_ffflash_save(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    apifile.write_text(dumps({'a': 'b'}), 'utf-8')

    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)
    assert f
    assert f.args.APIfile == str(apifile)
    assert f.location == str(apifile)
    assert f.api is not None

    old_c = deepcopy(f.api.c)
    assert f.api.push('c', 'a') is None
    assert loads(f.save()) == f.api.c

    assert f.api.c != old_c

    assert loads(apifile.read_text('utf-8')) == {'a': 'c'}

    assert tmpdir.remove() is None


def test_ffflash_save_check_timestamp(tmpdir, fffake):
    apifile = tmpdir.join('phony_api_file.json')
    apifile.write_text(dumps({'state': {'lastchange': 'never'}}), 'utf-8')

    assert tmpdir.listdir() == [apifile]

    f = fffake(apifile, dry=True)
    assert f
    assert f.api is not None
    old_t = f.api.pull('state', 'lastchange')
    assert loads(f.save()) == f.api.c

    new_t = f.api.pull('state', 'lastchange')
    assert old_t != new_t

    assert loads(
        apifile.read_text('utf-8')
    ) == {'state': {'lastchange': new_t}}

    assert tmpdir.remove() is None
