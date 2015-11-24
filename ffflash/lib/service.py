from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime
from sys import argv as _argv


def args(argv=None):
    p = ArgumentParser(
        prog='ffflash',
        description='',
        epilog='',
        add_help=True
    )
    p.add_argument(
        'APIfile', action='store',
        help='Freifunk API File to modify'
    )
    p.add_argument(
        '-n', '--nodelist', action='store',
        help='URL to map\'s nodelist.json, updates nodes count'
    )
    p.add_argument(
        '-s', '--sidecars', nargs='*',
        help='sync updates from/with sidecar files'
    )
    p.add_argument(
        '-d', '--dry', action='store_true',
        help='do not save output, displays only a preview'
    )

    p.add_argument(
        '-v', '--verbose', action='store_true',
        help='show verbose output'
    )
    return p.parse_args(argv if argv else _argv[1:])


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


def api_timestamp():
    return datetime.now().isoformat('T')
