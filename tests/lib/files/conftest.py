import pytest

from ffflash.lib.files import dump_file, load_file, read_file, write_file
from ffflash.lib.struct import struct_dump, struct_load


def df(loc, cont):
    return write_file(loc, cont)


def dj(loc, cont):
    return dump_file(loc, cont, as_yaml=False)


def dy(loc, cont):
    return dump_file(loc, cont, as_yaml=True)


def lf(loc, fb=None):
    return read_file(loc, fallback=fb)


def lj(loc, fb=None):
    return load_file(loc, fallback=fb, as_yaml=False)


def ly(loc, fb=None):
    return load_file(loc, fallback=fb, as_yaml=True)


def sdf(cont):
    return cont


def sdj(cont):
    with struct_dump(cont, as_yaml=False) as res:
        return res


def sdy(cont):
    with struct_dump(cont, as_yaml=True) as res:
        return res


def slf(cont):
    return cont


def slj(cont):
    with struct_load(cont, as_yaml=False) as res:
        return res


def sly(cont):
    with struct_load(cont, as_yaml=True) as res:
        return res


@pytest.fixture(params=[(df, sdf, slf), (dj, sdj, slj), (dy, sdy, sly)])
def write_f(request):
    return request.param


@pytest.fixture(params=[(lf, slf, sdf), (lj, slj, sdj), (ly, sly, sdy)])
def read_f(request):
    return request.param
