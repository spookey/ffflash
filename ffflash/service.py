from ffflash import args, now, timeout
from ffflash.lib.container import Container


def recent(changes):
    container = Container('recent', args.recent)
    info = {'recent': {}}

    for field, data in changes.items():
        if field not in args.rignore:
            container.data[field] = container.data.get(field, {})
            info['recent'][field] = info['recent'].get(field, 0)
            for nid, message in data.items():
                message.update({'time': now})
                container.data[field][nid] = message
                info['recent'][field] += 1

    container.data = dict(
        (field, dict(
            (nid, msg) for nid, msg in data.items() if
            msg.get('time') and msg['time'] > timeout
        )) for field, data in container.data.items() if
        not field.startswith('_')
    )

    container.save(info=info)
