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
        self.info.branches = {}
        self.info.count = {'online': 0, 'total': 0}
        self.info.gateways = {}
        self.info.roles = {}
        self.info.sums = {'clients_total': 0, 'clients_wifi': 0, 'reboots': 0}

        for node_id, node in self.data.items():
            self.info.count.total += 1
            if node.online:
                self.info.count.online += 1
                self.info.sums.clients_total += node.clients_total
                self.info.sums.clients_wifi += node.clients_wifi
                self.info.sums.reboots += node.reboots
                if node.gateway:
                    gw = self.data.get(node.gateway.replace(':', ''))
                    if gw:
                        node._gateway = gw.hostname
                        self.info.gateways[gw.hostname] = (
                            1 + self.info.gateways.get(gw.hostname, 0)
                        )
                if node.uptime:
                    node._uptime = epoch_repr(node.uptime, ms=True)
                if node.last_seen and node.first_seen:
                    node._lifespan = epoch_repr(
                        abs(node.last_seen - node.first_seen), ms=True
                    )

            if node.branch:
                self.info.branches[node.branch] = (
                    1 + self.info.branches.get(node.branch, 0)
                )
            if node.role:
                self.info.roles[node.role] = (
                    1 + self.info.roles.get(node.role, 0)
                )

        self.info.count.offline = abs(
            self.info.count.total - self.info.count.online
        )

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
                    'new': False, 'old': True
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
                'new': True, 'old': False
            }
            log.info('new node {}'.format(node.hostname))

    def __node_current(self, node_id, node):
        old_uptime = self.data[node_id].get('uptime', 0)
        if node.uptime and old_uptime > node.uptime:
            reboots = self.data[node_id].reboots
            self.data[node_id].reboots += 1
            self.changes.reboots[node_id] = {
                'hostname': node.hostname,
                'new': reboots + 1, 'old': reboots
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

    def update(self, fresh):
        self.changes = Element()

        self.__prepare_all()

        for node_id, node in fresh:
            self.__node_new(node_id, node)
            self.__node_current(node_id, node)
            for key, val in node.items():
                self.__node_generic(node_id, node, key, val)

        log.info('update finished')
        self.save()

        return self.changes
