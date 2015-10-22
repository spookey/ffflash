from contextlib import contextmanager
from copy import deepcopy
from json import dumps, loads

from ffflash import log


@contextmanager
def load_json(content, fallback=None):
    try:
        yield loads(content) if isinstance(content, str) else fallback
    except ValueError as ex:
        log.error('could not load json {}'.format(ex))
        yield fallback


@contextmanager
def dump_json(data, indent=2):
    try:
        yield dumps(data, indent=indent, sort_keys=True)
    except TypeError as ex:
        log.error('could not dump json {}'.format(ex))
        yield ''


def merge_dicts(left, right):
    if not isinstance(right, dict):
        return right
    res = deepcopy(left)
    if isinstance(res, dict):
        for key in right.keys():
            res[key] = (
                merge_dicts(res[key], right[key]) if
                res.get(key) and isinstance(res[key], dict) else
                deepcopy(right[key])
            )
    return res


class Element(dict):
    def __getattr__(self, key):
        return self.__getitem__(key)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        if isinstance(value, dict):
            value = Element(value)
            self.__setitem__(key, value)
        return value

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __delattr__(self, key):
        self.__delitem__(key)

    def __missing__(self, key):
        self.__setitem__(key, Element())
        return self.__getitem__(key)
