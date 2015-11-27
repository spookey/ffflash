from codecs import open as c_open
from os import path

from .struct import struct_dump, struct_load


def check_file_location(location, must_exist=False):
    '''
    Validate path for a file.

    Checks for the parent folder to exist, and that ``location`` itself is
    not a folder.
    Optionally, if ``location`` is an already existing file.

    :param location: Path to check.
    :param must_exist: Check also if ``location`` really exists and is a file
    :return str: Validated path of ``location`` if all above conditions
        are met or ``None``
    '''
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
    '''
    Read string data from files

    :param location: filename where to write to
    :param fallback: data to return in case of read failure
    :return: read data from ``location`` if successful else ``fallback``
    '''
    location = check_file_location(location, must_exist=True)
    if location:
        with c_open(location, 'r', encoding='utf-8') as rl:
            data = rl.read()
            if data is not None:
                return data
    return fallback


def write_file(location, data):
    '''
    Write string data into files

    :param location: filename where to write to
    :param data: content to write into ``filename``
    :return: ``data`` if successful
    '''
    location = check_file_location(location)
    if location and (data is not None):
        with c_open(location, 'w', encoding='utf-8') as wl:
            wl.write(data)
            return data


def load_file(location, fallback=None, as_yaml=False):
    '''
    Unpickle either *json* or *yaml* from a file

    :param location: path where to unpickle from
    :param fallback: data to return in case of unpickle failure
    :param as_yaml: read as *yaml* instead of *json*
    :return: unpickled data from ``location``
    '''
    with struct_load(
        read_file(location), fallback=fallback, as_yaml=as_yaml
    ) as data:
        return data


def dump_file(location, content, as_yaml=False):
    '''
    Pickle either *json* or *yaml* into a file

    :param location: path where to pickle into
    :param content: data to store
    :param as_yaml: output as *yaml* instead of *json*
    '''
    with struct_dump(content, as_yaml=as_yaml) as data:
        return write_file(location, data) if (data is not None) else None
