from os import path

from ffflash import args, log
from ffflash.lib.data import load_json, merge_dicts
from ffflash.lib.files import read_json_file, write_json_file
from ffflash.lib.shell import construct_alfred_command, launch


def announced():
    result = {}
    for channel in args.dchannels:
        pass

    return result


def _ask_alfred(cmdline, so_far={}):
    with launch(cmdline) as (code, out, err):
        if code == 0 and out:
            with load_json(out, fallback={}) as data:
                return merge_dicts(so_far, data), data
        log.error('wrong alfred data {}'.format(err))
    return so_far, {}


def alfred():
    result = {}
    for channel in args.achannels:
        cmdline = construct_alfred_command(channel)
        result, raw = _ask_alfred(cmdline, result)
        if raw and args.raw:
            write_json_file(
                path.join(args.raw, 'alfred{}.json'.format(channel)), raw
            )
    if result and args.raw:
        write_json_file(
            path.join(args.raw, 'alfred_result.json'), result
        )
    return result


def collect():
    if all([args.dsock, args.dbatif]):
        return announced()
    elif args.asock:
        return alfred()
    elif args.raw:
        return read_json_file(
            path.join(args.raw, 'alfred_result.json')
        )
    return {}


def poll():
    fresh = collect()
    if fresh:
        for key, data in fresh.items():
            node_id = data.get('node_id', key.replace(':', ''))
            hostname = data.get('hostname')
            if not all([node_id, hostname]):
                continue

            clients = data.get('clients', {})
            hardware = data.get('hardware', {})
            software = data.get('software', {})
            system = data.get('system', {})

            batman_adv = software.get('batman-adv', {})
            autoupdater = software.get('autoupdater', {})
            fastd = software.get('fastd', {})
            firmware = software.get('firmware', {})

            yield node_id, {
                'batman_version': batman_adv.get('version'),
                'clients_total': clients.get('total', 0),
                'clients_wifi': clients.get('wifi', 0),
                'gateway': data.get('gateway'),
                'hostname': hostname,
                'release': firmware.get('release'),
                'fastd_uplink': fastd.get('enabled', False),
                'model': hardware.get('model'),
                'role': system.get('role'),
                'branch': autoupdater.get('branch'),
                'uptime': 1000 * data.get('uptime', 0),
            }
