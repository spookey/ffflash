from codecs import open as c_open
from os import path

from .struct import struct_dump, struct_load


def check_file_location(location, must_exist=False):
    location = path.abspath(location)
    parent = path.dirname(location)
    if all([
        path.isdir(parent),
        not path.isdir(location),
        (
            path.exists(location) and path.isfile(location)
        ) if must_exist else True
    ]):
        return location


def read_file(location, fallback=None):
    location = check_file_location(location, must_exist=True)
    if location:
        with c_open(location, 'r', encoding='utf-8') as rl:
            data = rl.read()
            if data is not None:
                return data
    return fallback


def write_file(location, data):
    location = check_file_location(location)
    if location and (data is not None):
        with c_open(location, 'w', encoding='utf-8') as wl:
            wl.write(data)
            return data


def load_file(location, fallback=None, as_yaml=False):
    with struct_load(
        read_file(location), fallback=fallback, as_yaml=as_yaml
    ) as data:
        return data


def dump_file(location, content, as_yaml=False):
    with struct_dump(content, as_yaml=as_yaml) as data:
        return write_file(location, data) if (data is not None) else None
