import pytest

from ffflash.lib.args import parsed_args

F = 'ffapi_test_file.json'


def sys_ex(a):
    with pytest.raises(SystemExit):
        parsed_args(a)


def test_parsed_args_empty_or_wrong_or_help():
    for ta in [[], ['--wrong'], ['--what', '--ever'], ['--help']]:
        sys_ex(ta)


def test_parsed_args_apifile_missing():
    for ta in [
        ['-n', 'nodelist'],
        ['-s', 'a', 'b'],
        ['-d'], ['-v'], ['-h']
    ]:
        sys_ex(ta)


def test_parsed_args_nodelist_or_sidecars_missing():
    for ta in [
        [F, '-n'], [F, '--nodelist'],
        [F, '-s'], [F, '--sidecars']
    ]:
        sys_ex(ta)


def test_parsed_args_rankefile_with_or_without_nodelist():
    N = 'nodelist_test_file.json'
    R = 'rankfile_test_file.json'

    for ta in [
        [F, '-n'], [F, '--nodelist'], [F, '-r'], [F, '--rankfile'],
        [F, '-n', N, '-r'], [F, '--nodelist', N, '--rankfile'],
        [F, '-r'], [F, '--rankfile', R]
    ]:
        sys_ex(ta)
    for ta in [
        [F, '-n', N], [F, '--nodelist', N],
        [F, '-n', N, '-r', R], [F, '--nodelist', N, '--rankfile', R]
    ]:
        assert parsed_args(ta)


def test_parsed_args_rank_details():
    a = vars(parsed_args([F]))

    for t in [
        'rankclients', 'rankoffline', 'rankonline',
        'rankposition', 'rankwelcome'
    ]:
        sys_ex([F, '--{}'.format(t)])
        sys_ex([F, '--{}'.format(t), 'test'])

        v = a.get(t)
        assert isinstance(v, float)
        assert v > 0


def test_parsed_args_valid_options():
    def t(a, nl=None, sc=None, rf=None, d=False, v=False):
        assert a.APIfile == F
        assert a.nodelist == nl
        assert a.rankfile == rf
        assert a.sidecars == ([sc] if sc else None)
        assert a.dry == d
        assert a.verbose == v

    nl = 'http://localhost/nodelist.json'
    sc = 'contact services timeline'
    rf = 'rankfile.json'

    t(parsed_args([F, '-n', nl, '-s', sc, '-d', '-v']),
      nl=nl, sc=sc, d=True, v=True)
    t(parsed_args([F, '-n', nl, '-s', sc, '-d']),
      nl=nl, sc=sc, d=True)
    t(parsed_args([F, '-n', nl, '-s', sc, '-v']),
      nl=nl, sc=sc, v=True)
    t(parsed_args([F, '-n', nl, '-s', sc]),
      nl=nl, sc=sc)
    t(parsed_args([F, '-n', nl]),
      nl=nl)
    t(parsed_args([F, '-s', sc]),
      sc=sc)
    t(parsed_args([F, '-n', nl, '-r', rf]),
      nl=nl, rf=rf)
    t(parsed_args([F, '-n', nl, '-s', sc, '-r', rf]),
      nl=nl, sc=sc, rf=rf)
    t(parsed_args([F, '-n', nl, '-d']),
      nl=nl, d=True)
    t(parsed_args([F, '-s', sc, '-v']),
      sc=sc, v=True)
