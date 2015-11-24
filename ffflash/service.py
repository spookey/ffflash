from ffflash import args, now, timeout
from ffflash.lib.container import Container


def recent(changes):
    cnt = Container('recent', args.recent)

    if changes:
        cnt.info.current = {}
        for field, data in changes.items():
            if field not in args.rignore:
                cnt.info.current[field] = cnt.info.current.get(field, 0)
                for node_id, message in data.items():
                    message['time'] = now
                    cnt.data[field][node_id] = message
                    cnt.info.current[field] += 1

    clean = {}
    cnt.info.count = {}

    for field, data in cnt.data.items():
        clean[field] = {}
        cnt.info.count[field] = cnt.info.count.get(field, 0)
        for node_id, message in data.items():
            if message.get('time', 0) > timeout:
                clean[field][node_id] = message
                cnt.info.count[field] += 1
    cnt.data = clean
    cnt.save()
