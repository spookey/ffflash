from os import path

from ffflash import args, log, now, timeout
from ffflash.lib.files import read_json_file, write_json_file


def recent(changes):
    recent_file = path.abspath(args.recent)
    current = read_json_file(recent_file, fallback={})

    for field, values in changes.items():
        if field not in args.rignore:
            current[field] = current.get(field, {})
            for nid, data in values.items():
                data.update({'time': now})
                current[field][nid] = data

    current = dict(
        (field, dict(
            (nid, data) for nid, data in values.items() if
            data.get('time') and data['time'] > timeout
        )) for field, values in current.items()
    )
    write_json_file(recent_file, current)
    log.info('written recent {}'.format(recent_file))
