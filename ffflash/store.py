from ffflash import log, now, timeout
from ffflash.lib.container import Container
from ffflash.lib.clock import epoch_repr


class Storage(Container):
    def __init__(self, storage):
        super(Storage, self).__init__('storage', storage)
        self.data['nodes'] = self.data.get('nodes', {})
        self.changes = {}

    def _prepare_all(self):
        clean = {}

        for node_id, data in self.data['nodes'].items():
            hostname = data.get('hostname')
            last_seen = data.get('last_seen')
            if last_seen and last_seen > timeout:
                clean[node_id] = {}
                for name, val in data.items():
                    if name.startswith('_'):
                        continue
                    elif name in ['online']:
                        val = False
                    elif name in ['gateway']:
                        val = None
                    clean[node_id][name] = val
            else:
                self.changes['lost'] = self.changes.get('lost', {})
                self.changes['lost'][node_id] = {
                    'hostname': hostname, 'new': None, 'old': last_seen
                }
                log.info('node change lost {}'.format(hostname))

        self.data['nodes'] = clean

    def _new(self, node_id, hostname):
        if node_id not in self.data['nodes'].keys():
            log.info('node change new {}'.format(hostname))
            self.data['nodes'][node_id] = {
                'first_seen': now,
                'reboots': 0,
                'uptime': 0
            }
            self.changes['new'] = self.changes.get('new', {})
            self.changes['new'][node_id] = {
                'hostname': hostname, 'new': now, 'old': None
            }

    def _current(self, node_id, hostname, uptime):
        self.data['nodes'][node_id]['last_seen'] = now
        self.data['nodes'][node_id]['online'] = True

        old_uptime = self.data['nodes'][node_id].get('uptime', 0)
        if uptime and old_uptime > uptime:
            self.data['nodes'][node_id]['reboots'] += 1
            self.changes['reboots'] = self.changes.get('reboots', {})
            self.changes['reboots'][node_id] = {
                'hostname': hostname, 'new': uptime, 'old': old_uptime
            }

    def _generic(self, node_id, hostname, name, val):
        old = self.data['nodes'][node_id].get(name)
        self.data['nodes'][node_id][name] = val
        if old and old != val:
            log.info('node change {} {}: {} {}'.format(
                name, hostname, old, val
            ))
            self.changes[name] = self.changes.get(name, {})
            self.changes[name][node_id] = {
                'hostname': hostname, 'new': val, 'old': old
            }

    def _extend(self, node_id, hostname):
        node = self.data['nodes'][node_id]
        first_seen = node.get('first_seen')
        last_seen = node.get('last_seen')
        uptime = node.get('uptime')
        gateway = node.get('gateway')

        if uptime:
            self.data['nodes'][node_id]['_uptime'] = epoch_repr(
                uptime, ms=True
            )
        if first_seen and last_seen:
            self.data['nodes'][node_id]['_lifespan'] = epoch_repr(
                abs(last_seen - first_seen), ms=True
            )
        if gateway:
            gw = self.data['nodes'].get(gateway.replace(':', ''))
            if gw:
                self.data['nodes'][node_id]['_gateway'] = gw.get(
                    'hostname'
                )

    def _gen_info(self):
        info = {}
        return info

    def update(self, fresh):
        self.changes = {}

        self._prepare_all()

        for node_id, data in fresh:
            hostname = data.get('hostname')
            uptime = data.get('uptime')
            self._new(node_id, hostname)
            self._current(node_id, hostname, uptime)
            for name, val in data.items():
                self._generic(node_id, hostname, name, val)
            self._extend(node_id, hostname)

        log.info('update done')
        if self.data['nodes']:
            info = self._gen_info()
            self.save(info=info)

        return self.changes
