from json import loads as j_load

from yaml import load as y_load

from ffflash.lib.struct import struct_load


def test_struct_load_wrong_input_data():
    for fd in [None, True, '', {}, (), 23]:
        for asy in [True, False]:
            with struct_load(fd, as_yaml=asy) as t:
                assert t is None


def test_struct_load_fallback():
    for fb in [None, {}, 1, 'whatever', ('a', 'b')]:
        for asy in [True, False]:
            with struct_load(False, fallback=fb, as_yaml=asy) as t:
                assert t == fb


def test_struct_load_json_fishy():
    for fj in ['"', 'a', '\n', '"a":', '{"a": "b",}']:
        with struct_load(fj, fallback='wrong', as_yaml=False) as t:
            assert t == 'wrong'


def test_struct_load_yaml_fishy():
    for fy in ['"', ':', '>>>']:
        with struct_load(fy, fallback='wrong', as_yaml=True) as t:
            assert t == 'wrong'


def test_struct_load_json():
    for tj in ['""', '"a"', '{}', '{"a": "b"}']:
        with struct_load(tj, as_yaml=False) as t:
            assert t == j_load(tj)


def test_struct_load_yaml():
    for ty in ['', 'a', 'a:', 'a: b', 'a: [b, c]']:
        with struct_load(ty, as_yaml=True) as t:
            assert t == y_load(ty)
