from copy import deepcopy


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
