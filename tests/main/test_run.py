from json import dumps as j_dump
from json import loads as j_load
from pprint import pformat

import pytest
from yaml import load as y_load

from ffflash.main import run


def test_run_no_or_empty_apifile(tmpdir):
    with pytest.raises(SystemExit):
        run([])

    assert run([str(tmpdir.join('phony_api_file.txt')), '-d']) is True

    assert tmpdir.remove() is None


def test_run_dump_apifile(tmpdir, capsys):
    c = {'a': 'b', 'c': 'd'}
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(j_dump(c), 'utf-8')

    assert run([str(apifile), '-d']) is True
    out, err = capsys.readouterr()
    assert pformat(c) in out
    assert err == ''

    assert tmpdir.remove() is None


def test_run_apifile_not_modified(tmpdir):
    c = {'a': 'b', 'c': 'd'}
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(j_dump(c), 'utf-8')

    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(j_dump({
        'will': {'not': {'be': 'recognized'}}
    }), 'utf-8')

    side = tmpdir.join('wrong_extension.txt')
    car = tmpdir.join('double..dot.yaml')

    assert run([
        str(apifile),
        '-n', str(nodelist),
        '-s', str(side), str(car)
    ]) is True

    assert tmpdir.remove() is None


def test_run_apifile_modified(tmpdir):
    c = {'a': 'b', 'c': 'd', 'state': {'nodes': 0}}
    apifile = tmpdir.join('api_file.json')
    apifile.write_text(j_dump(c), 'utf-8')

    nodelist = tmpdir.join('nodelist.json')
    nodelist.write_text(j_dump({
        'version': 1,
        'nodes': [
            {'status': {'clients': 23, 'online': True}},
            {'status': {'clients': 42, 'online': False}}
        ],
        'updated_at': 'never'
    }), 'utf-8')

    side = tmpdir.join('a.json')
    car = tmpdir.join('c.yaml')

    assert tmpdir.listdir() == [apifile, nodelist]

    assert run([
        str(apifile),
        '-n', str(nodelist),
        '-s', str(side), str(car)
    ]) is False

    assert sorted(tmpdir.listdir()) == sorted([side, apifile, car, nodelist])

    assert j_load(side.read_text('utf-8')) == 'b'
    assert y_load(car.read_text('utf-8')) == 'd'

    c['state']['nodes'] = 1
    assert j_load(apifile.read_text('utf-8')) == c

    assert tmpdir.remove() is None
