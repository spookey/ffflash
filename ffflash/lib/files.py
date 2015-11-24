from codecs import open as c_open
from json import dumps as j_dump
from json import loads as j_load
from os import path

from yaml import dump as y_dump
from yaml import load as y_load


def read_file(location, fallback=None):
    location = path.abspath(location)
    if path.exists(location) and path.isfile(location):
        with c_open(location, 'r', encoding='utf-8') as rl:
            data = rl.read()
            if data is not None:
                return data
    return fallback


def write_file(location, data):
    location = path.abspath(location)
    parent = path.dirname(location)
    if not path.isdir(parent) or path.isdir(location):
        return False
    if data is not None:
        with c_open(location, 'w', encoding='utf-8') as wl:
            return wl.write(data)


def load_file(location, fallback={}, as_yaml=False):
    data = read_file(location)
    if data is not None:
        try:
            return (
                y_load(data) if as_yaml else j_load(data)
            )
        except ValueError:
            pass
    return fallback


def dump_file(location, content, as_yaml=False):
    if content is not None:
        return write_file(location, (
            y_dump(
                content, indent=4, default_flow_style=False
            ) if as_yaml else j_dump(
                content, indent=2, sort_keys=True
            )
        ))
