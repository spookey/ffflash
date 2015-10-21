from ffflash import log, now, timeout
from ffflash.lib.container import Container
from ffflash.poll import poll


class Storage(Container):
    def __init__(self, storage):
        super(Storage, self).__init__('storage', storage)
        self.data['nodes'] = self.data.get('nodes', {})

    def _prepare_nodes(self):
        lost = {}
        outdated = [
            nid for nid, node in self.data['nodes'].items() if
            not node.get('last_seen') or node['last_seen'] < timeout
        ]
        for rem in outdated:
            node = self.data['nodes'][rem]
            hostname = node.get('hostname')
            lost[rem] = {
                'hostname': hostname, 'new': None, 'old': node.get('last_seen')
            }
            log.info('node change timeout {}'.format(hostname), end='\r')

        self.data['nodes'] = dict(
            (nid, node) for nid, node in self.data['nodes'].items() if
            nid not in outdated and not node.update({'online': False})
        )
        return lost

    def _change_node(self, field, nid, data, changes):
        node = self.data['nodes'][nid]
        hostname = node.get('hostname')
        old = node.get(field)
        new = data.get(field)
        self.data['nodes'][nid][field] = new
        if old and old != new:
            log.info('node change {} {}: {} {}'.format(
                field, hostname, old, new
            ), end='\r')
            changes[field] = changes.get(field, {})
            changes[field][nid] = {
                'hostname': hostname, 'new': new, 'old': old
            }

    def _update_nodes(self, changes):
        for node_id, node in poll():
            hostname = node.get('hostname')
            if node_id not in self.data['nodes'].keys():
                log.info('node change new {}'.format(hostname), end='\r')
                self.data['nodes'][node_id] = {
                    'first_seen': now,
                    'reboots': 0,
                    'uptime': 0
                }
                changes['new'] = changes.get('new', {})
                changes['new'][node_id] = {
                    'hostname': hostname, 'new': now, 'old': None
                }
            self.data['nodes'][node_id]['last_seen'] = now
            self.data['nodes'][node_id]['online'] = True
            uptime = self.data['nodes'][node_id].get('uptime', 0)
            if uptime > node['uptime']:
                self.data['nodes'][node_id]['reboots'] += 1
                changes['reboots'] = changes.get('reboots', {})
                changes['reboots'][node_id] = {
                    'hostname': hostname, 'new': node['uptime'], 'old': uptime
                }
            [self._change_node(
                field, node_id, node, changes
            ) for field in node.keys()]
        return changes

    def _gen_info(self):
        info = {
            'sums': self.data['_info'].get('sums', {})
        }
        info['sums']['nodes'] = len(self.data['nodes'])
        info['sums']['clients'] = sum([
            max(n.get('clients_wifi'), n.get('clients_total')) for
            n in self.data['nodes'].values()
        ])
        info['sums']['reboots'] = sum([
            n.get('reboots') for n in self.data['nodes'].values()
        ])
        return info

    def update(self):
        changes = {}

        lost = self._prepare_nodes()
        if lost:
            changes['lost'] = lost

        changes = self._update_nodes(changes)

        log.info(' ' * 80, end='\r')
        log.info('update done')
        if self.data['nodes']:
            self.save(
                info=self._gen_info()
            )
        return changes
