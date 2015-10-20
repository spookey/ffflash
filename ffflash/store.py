from os import path

from ffflash import log, now, timeout
from ffflash.lib.clock import epoch_repr
from ffflash.lib.files import read_json_file, write_json_file
from ffflash.poll import poll


class Storage:
    def __init__(self, storage):
        self._storage = path.abspath(storage)
        self.data = read_json_file(self._storage, fallback={})
        self.data['nodes'] = self.data.get('nodes', {})
        self._info()

    def _info(self):
        self.data['_info'] = self.data.get('_info', {})

        self.data['_info']['access'] = self.data['_info'].get('access', {})
        if not self.data['_info']['access'].get('first', False):
            self.data['_info']['access']['first'] = now
        self.data['_info']['access']['last'] = now
        self.data['_info']['access']['overall'] = epoch_repr(
            abs(now - self.data['_info']['access']['first']),
            ms=True
        )
        self.data['_info']['sums'] = self.data['_info'].get('sums', {})
        self.data['_info']['sums']['nodes'] = len(self.data['nodes'])
        self.data['_info']['sums']['clients'] = sum([
            max(n.get('clients_wifi'), n.get('clients_total')) for
            n in self.data['nodes'].values()
        ])
        self.data['_info']['sums']['reboots'] = sum([
            n.get('reboots') for n in self.data['nodes'].values()
        ])

    def save(self):
        self._info()
        if write_json_file(self._storage, self.data):
            log.info('storage saved {}'.format(self._storage))

    def update(self):
        changes = {}

        def _change(field, nid, data):
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

        remove = [
            nid for nid, node in self.data['nodes'].items() if
            not node.get('last_seen') or node['last_seen'] < timeout
        ]
        for rem in remove:
            node = self.data['nodes'][rem]
            hostname = node.get('hostname')
            changes['lost'] = changes.get('lost', {})
            changes['lost'][rem] = {
                'hostname': hostname, 'new': None, 'old': node.get('last_seen')
            }
            log.info('node change timeout {}'.format(hostname), end='\r')

        self.data['nodes'] = dict(
            (nid, node) for nid, node in self.data['nodes'].items() if
            nid not in remove and not node.update({'online': False})
        )

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
            [_change(field, node_id, node) for field in node.keys()]

        log.info(' ' * 80, end='\r')
        log.info('update done')
        if self.data['nodes']:
            self.save()
        return changes
