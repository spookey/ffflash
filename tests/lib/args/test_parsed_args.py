import pytest

from ffflash.lib.args import parsed_args

F = 'ffapi_test_file.json'


def ex(a):
    with pytest.raises(SystemExit):
        parsed_args(a)


def test_parsed_args_empty_or_wrong_or_help():
    for ta in [[], ['--wrong'], ['--what', '--ever'], ['--help']]:
        ex(ta)


def test_parsed_args_apifile_missing():
    for ta in [
        ['-n', 'nodelist'],
        ['-s', 'a', 'b'],
        ['-d'], ['-v'], ['-h']
    ]:
        ex(ta)


def test_parsed_args_nodelist_or_sidecars_missing():
    for ta in [
        [F, '-n'], [F, '--nodelist'],
        [F, '-s'], [F, '--sidecars']
    ]:
        ex(ta)


def test_parsed_args_valid_options():
    def t(a, nl=None, sc=None, d=False, v=False):
        assert a.APIfile == F
        assert a.nodelist == nl
        assert a.sidecars == ([sc] if sc else None)
        assert a.dry == d
        assert a.verbose == v

    nl = 'http://localhost/nodelist.json'
    sc = 'contact services timeline'

    t(
        parsed_args([F, '-n', nl, '-s', sc, '-d', '-v']),
        nl=nl, sc=sc, d=True, v=True
    )
    t(
        parsed_args([F, '-n', nl, '-s', sc, '-d']),
        nl=nl, sc=sc, d=True
    )
    t(
        parsed_args([F, '-n', nl, '-s', sc, '-v']),
        nl=nl, sc=sc, v=True
    )
    t(
        parsed_args([F, '-n', nl, '-s', sc]),
        nl=nl, sc=sc
    )
    t(
        parsed_args([F, '-n', nl]),
        nl=nl
    )
    t(
        parsed_args([F, '-s', sc]),
        sc=sc
    )
    t(
        parsed_args([F, '-n', nl, '-d']),
        nl=nl, d=True
    )
    t(
        parsed_args([F, '-s', sc, '-v']),
        sc=sc, v=True
    )
