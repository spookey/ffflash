from ffflash.main import FFFlash
from ffflash.lib.args import parsed_args
from json import dumps, loads
from copy import deepcopy


def test_ffflash_save(tmpdir):
    p = tmpdir.join('phony_api_file.txt')
    api = {'a': 'b', 'state': {'lastchange': 'never'}}
    p.write_text(dumps(api), 'utf-8')
    assert tmpdir.listdir() == [str(p)]

    a = parsed_args([str(p), '-d'])

    f = FFFlash(a)

    assert f
    assert f.api is None
    assert f.load_api() is None

    assert f.args.APIfile == str(p)
    assert f.location == str(p)
    assert f.api is not None

    old_c = deepcopy(f.api.c)

    assert f.api.push('c', 'a') is None

    assert loads(f.save()) == f.api.c

    assert f.api.c != old_c

    tstamp = f.api.pull('state', 'lastchange')
    assert tstamp != 'never'

    api['a'] = 'c'
    api['state'].update({'lastchange': tstamp})
    assert loads(p.read_text('utf-8')) == api

    assert tmpdir.remove() is None
