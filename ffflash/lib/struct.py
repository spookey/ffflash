from contextlib import contextmanager
from copy import deepcopy
from json import dumps as j_dump
from json import loads as j_load

from yaml import dump as y_dump
from yaml import load as y_load


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
def load(content, fallback={}, as_yaml=False,):
    if isinstance(content, str):
        try:
            yield y_load(content) if as_yaml else j_load(content)
        except ValueError:
            yield fallback
    return


@contextmanager
def dump(content, as_yaml=False):
    if content is not None:
        try:
            yield y_dump(
                content, indent=4, default_flow_style=False
            ) if as_yaml else j_dump(
                content, indent=2, sort_keys=True
            )
        except ValueError:
            yield None
    return
