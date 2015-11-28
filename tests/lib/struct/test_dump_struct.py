from json import dumps as j_dump

from yaml import dump as y_dump

from ffflash.lib.struct import dump_struct


def test_dump_struct_wrong_input_data():
    for fj in [range, set, y_dump, j_dump]:
        with dump_struct(fj, as_yaml=False) as t:
            assert t is None


def test_dump_struct_json():
    for tj in ['', 'a', {}, {'a': 'b'}]:
        with dump_struct(tj, as_yaml=False) as t:
            assert t == j_dump(
                tj, indent=2, sort_keys=True
            )


def test_dump_struct_yaml():
    for ty in [None, 'a', {'a': None}, {'a': 'b'}, {'a': ['b', 'c']}, range]:
        with dump_struct(ty, as_yaml=True) as t:
            assert t == y_dump(
                ty, indent=4, default_flow_style=False
            )
