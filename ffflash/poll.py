from os import path

from ffflash import args, log
from ffflash.lib.data import Element, load_json, merge_dicts
from ffflash.lib.files import read_json_file, write_json_file
from ffflash.lib.shell import construct_alfred_command, launch


def announced():
    result = {}
    for channel in args.dchannels:
        pass

    return result


def _ask_alfred(cmdline):
    with launch(cmdline) as (code, out, err):
        if code == 0 and out:
            with load_json(out, fallback={}) as data:
                return data
        log.error('error in alfred data {}'.format(err))


def alfred():
    result = {}
    for channel in args.achannels:
        cmdline = construct_alfred_command(channel)
        new = _ask_alfred(cmdline)
        if not new:
            log.error('could not fetch data for channel {}'.format(channel))
            return
        result = merge_dicts(result, new)
    if args.raw:
        raw_file = path.join(path.abspath(args.raw), 'alfred_result.json')
        write_json_file(raw_file, result)
        log.info('written raw file {}'.format(raw_file))
    return result


def collect():
    if all([args.dsock, args.dbatif]):
        return announced()
    if args.asock:
        return alfred()
    if args.raw:
        raw_file = path.join(path.abspath(args.raw), 'alfred_result.json')
        return read_json_file(raw_file, fallback={})


def poll():
    fresh = collect()
    if fresh:
        for key, data in fresh.items():
            node_id = data.get('node_id', key.replace(':', ''))
            node = Element(data)
            if not all([node_id, node.hostname]):
                continue

            yield node_id, Element({
                'batman_version': node.software['batman-adv'].get(
                    'version', None
                ),
                'clients_total': node.clients.get('total', 0),
                'clients_wifi': node.clients.get('wifi', 0),
                'gateway': node.get('gateway', None),
                'hostname': node.hostname,
                'release': node.software.firmware.get('release', None),
                'fastd_uplink': node.software.fastd.get('enabled', False),
                'model': node.hardware.get('model', None),
                'role': node.system.get('role', None),
                'branch': node.software.autoupdater.get('branch', None),
                'uptime': 1000 * node.get('uptime', 0),
            })
