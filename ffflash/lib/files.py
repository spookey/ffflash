from codecs import open as c_open
from os import path

from ffflash import CODING, log
from ffflash.lib.data import dump_json, load_json


def read_file(name, fallback=None):
    name = path.abspath(name)

    if path.exists(name) and path.isfile(name):
        with c_open(name, 'r', encoding=CODING) as fh:
            data = fh.read()
            if data is not None:
                return data
    log.warn('got empty file {}'.format(name))
    return fallback


def write_file(name, data):
    name = path.abspath(name)
    parent_dir = path.dirname(name)

    if not path.isdir(parent_dir) or path.isdir(name):
        log.error('path to file does not exist or is a folder {}'.format(name))
        return
    if data is not None:
        with c_open(name, 'w', encoding=CODING) as fh:
            fh.write(data)
            return data


def read_json_file(name, fallback=None):
    with load_json(read_file(name), fallback=fallback) as content:
        return content


def write_json_file(name, content):
    if content is not None:
        with dump_json(content) as data:
            return write_file(name, data)
