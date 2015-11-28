from argparse import ArgumentParser
from sys import argv as _argv

from ffflash.info import info


def parsed_args(argv=None):
    '''
    Parse arguments from commandline

    :param argv: List of Arguments to parse. - If omitted **sys.argv** is used
    :return Namespace: arguments from **ArgumentParser** for ``argv``
    '''
    parser = ArgumentParser(
        prog=info.name,
        description=info.description,
        epilog=info.ident,
        add_help=True
    )
    parser.add_argument(
        'APIfile', action='store',
        help='Freifunk API File to modify'
    )
    parser.add_argument(
        '-n', '--nodelist', action='store',
        help='URL or location to map\'s nodelist.json, updates nodes count'
    )
    parser.add_argument(
        '-s', '--sidecars', nargs='+',
        help='sync updates from/with sidecar files'
    )
    parser.add_argument(
        '-d', '--dry', action='store_true',
        help='do not save output, displays only a preview'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show verbose output'
    )
    return parser.parse_args(argv if argv else _argv[1:])
