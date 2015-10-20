from argparse import ArgumentParser


def main_args(argv):
    parser = ArgumentParser(
        prog='ffflash',
        description='manage your freifunk api file, store statistics, '
                    'rank nodes, and so much more',
        epilog='now with less features, but more bugs. enjoy!',
        add_help=True
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='show verbose output'
    )
    parser.add_argument(
        '-as', '--asock', action='store',
        help='full path to socket of alfred instance'
    )
    parser.add_argument(
        '--ajson', action='store', default='alfred-json',
        help='name or path of alfred-json executable'
    )
    parser.add_argument(
        '--achannels', nargs='*', default=['158', '159'],
        help='list of alfred channel numbers to query'
    )
    parser.add_argument(
        '--sudo', action='store_true',
        help='prefix alfred-json run with sudo'
    )
    parser.add_argument(
        '--ssh', action='store',
        help='run alfred-json over ssh with this options'
    )
    parser.add_argument(
        '-ds', '--dsock', action='store',
        help='address to bind for announced multicast'
    )
    parser.add_argument(
        '-di', '--dbatif', action='store',
        help='batman interface for announced multicast'
    )
    parser.add_argument(
        '--dchannels', nargs='*', default=['nodeinfo', 'statistics'],
        help='list of announced channel names to query'
    )
    parser.add_argument(
        '-st', '--store', action='store',
        help='full path to storage file'
    )
    parser.add_argument(
        '-t', '--timeout', action='store', default='1209600',
        help='remove node from storage if not seen within timeout seconds'
    )
    parser.add_argument(
        '-ff', '--ffapi', action='store',
        help='full path to freifunk-api file'
    )
    parser.add_argument(
        '-rc', '--recent', action='store',
        help='full path to recent file'
    )
    parser.add_argument(
        '--rignore', nargs='*', default=[
            'clients_total', 'clients_wifi', 'uptime'
        ], help='ignore these fields in recent file'
    )
    parser.add_argument(
        '-tp', '--top', action='store',
        help='full path to top file'
    )
    parser.add_argument(
        '-raw', '--raw', action='store',
        help='keep raw input files in this folder, or read them from there'
    )
    return parser.parse_args(argv)


def spock(args, log):
    if any([args.sudo, args.ssh]) and not args.asock:
        log.warn('ignoring sudo or ssh - no alfred socket given')
    if not args.store:
        log.error('no storage file given')
        return False
    return True
