from contextlib import contextmanager
from copy import deepcopy
from json import dumps as j_dump
from json import loads as j_load

from yaml import dump as y_dump
from yaml import load as y_load
from yaml.parser import ParserError
from yaml.scanner import ScannerError


def merge_dicts(first, second):
    if not isinstance(second, dict):
        return second
    res = deepcopy(first)
    if isinstance(res, dict):
        for key in second.keys():
            res[key] = (
                merge_dicts(res[key], second[key]) if
                res.get(key) and isinstance(res[key], dict) else
                deepcopy(second[key])
            )
    return res


@contextmanager
def struct_load(content, fallback=None, as_yaml=False,):
    try:
        yield (
            y_load(content) if as_yaml else j_load(content)
        ) if isinstance(content, str) else fallback
    except (ValueError, ScannerError, ParserError):
        yield fallback


@contextmanager
def struct_dump(content, as_yaml=False):
    try:
        yield y_dump(
            content, indent=4, default_flow_style=False
        ) if as_yaml else j_dump(
            content, indent=2, sort_keys=True
        )
    except TypeError:
        yield None
