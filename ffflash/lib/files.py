from codecs import open as c_open

from ffflash.lib.locations import check_file_location
from ffflash.lib.struct import dump_struct, load_struct


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
    with load_struct(
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
    with dump_struct(content, as_yaml=as_yaml) as data:
        return write_file(location, data) if (data is not None) else None
