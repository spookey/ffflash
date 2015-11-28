from json import loads as j_load

from yaml import load as y_load

from ffflash.lib.struct import load_struct


def test_load_struct_wrong_input_data():
    for fd in [None, True, '', {}, (), 23]:
        for asy in [True, False]:
            with load_struct(fd, as_yaml=asy) as t:
                assert t is None


def test_load_struct_fallback():
    for fb in [None, {}, 1, 'whatever', ('a', 'b')]:
        for asy in [True, False]:
            with load_struct(False, fallback=fb, as_yaml=asy) as t:
                assert t == fb


def test_load_struct_json_fishy():
    for fj in ['"', 'a', '\n', '"a":', '{"a": "b",}']:
        with load_struct(fj, fallback='wrong', as_yaml=False) as t:
            assert t == 'wrong'


def test_load_struct_yaml_fishy():
    for fy in ['"', ':', '>>>']:
        with load_struct(fy, fallback='wrong', as_yaml=True) as t:
            assert t == 'wrong'


def test_load_struct_json():
    for tj in ['""', '"a"', '{}', '{"a": "b"}']:
        with load_struct(tj, as_yaml=False) as t:
            assert t == j_load(tj)


def test_load_struct_yaml():
    for ty in ['', 'a', 'a:', 'a: b', 'a: [b, c]']:
        with load_struct(ty, as_yaml=True) as t:
            assert t == y_load(ty)
