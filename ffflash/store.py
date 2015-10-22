from ffflash import log, now, timeout
from ffflash.lib.clock import epoch_repr
from ffflash.lib.container import Container
from ffflash.lib.data import Element


class Storage(Container):
    def __init__(self, storage):
        super().__init__('nodes', storage)
        self.changes = Element()

    def _info(self):
        super()._info()

    def __prepare_all(self):
        clean = Element()
        for node_id, data in self.data.items():
            node = Element(data)
            if node.last_seen and node.last_seen > timeout:
                for name, val in node.items():
                    if name.startswith('_'):
                        continue
                    elif name in ['online']:
                        val = False
                    elif name in ['gateway']:
                        val = None
                    clean[node_id][name] = val
            else:
                self.changes.lost[node_id] = {
                    'hostname': node.hostname,
                    'new': None, 'old': node.last_seen
                }
                log.info('lost node {}'.format(node.hostname))

        self.data = clean

    def __node_new(self, node_id, node):
        if node_id not in self.data.keys():
            self.data[node_id] = Element({
                'first_seen': now,
                'reboots': 0,
                'uptime': 0
            })
            self.changes.new[node_id] = {
                'hostname': node.hostname,
                'new': now, 'old': None
            }
            log.info('new node {}'.format(node.hostname))

    def __node_current(self, node_id, node):
        old_uptime = self.data[node_id].get('uptime', 0)
        if node.uptime and old_uptime > node.uptime:
            self.data[node_id].reboots += 1
            self.changes.reboots[node_id] = {
                'hostname': node.hostname,
                'new': node.uptime, 'old': old_uptime
            }
            log.info('reboot node {}'.format(node.hostname))
        self.data[node_id].uptime = node.uptime
        self.data[node_id].last_seen = now
        self.data[node_id].online = True

    def __node_generic(self, node_id, node, key, val):
        old = self.data[node_id].get(key)
        self.data[node_id][key] = val
        if old and old != val:
            self.changes[key][node_id] = {
                'hostname': node.hostname,
                'new': val, 'old': old
            }
            log.info('{} node change {}'.format(key, node.hostname))

    def __node_extend(self, node_id, node):
        node = self.data[node_id]
        if node.uptime:
            self.data[node_id]._uptime = epoch_repr(node.uptime, ms=True)
        if node.last_seen and node.first_seen:
            self.data[node_id]._lifespan = epoch_repr(
                abs(node.last_seen - node.first_seen), ms=True
            )
        if node.gateway:
            gateway = self.data.get(node.gateway.replace(':', ''))
            if gateway:
                self.data[node_id]._gateway = gateway.get('hostname')

    def update(self, fresh):
        self.changes = Element()

        self.__prepare_all()

        for node_id, node in fresh:
            self.__node_new(node_id, node)
            self.__node_current(node_id, node)
            for key, val in node.items():
                self.__node_generic(node_id, node, key, val)
            self.__node_extend(node_id, node)

        log.info('update finished')
        self.save()

        return self.changes
