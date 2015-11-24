from .lib.remote import www_fetch
from .lib.struct import load


def _nodelist_fetch(ff):
    ff.log('fetching nodelist {}'.format(ff.args.nodelist))

    with www_fetch(ff.args.nodelist, fallback=None) as data:
        if not data:
            return ff.log(
                'could not fetch nodelist {} {}'.format(ff.args.nodelist),
                level=False
            )

        with load(data, fallback=None, as_yaml=False) as nodelist:
            if not nodelist:
                return ff.log(
                    'could not unload nodelist {}'.format(ff.args.nodelist)
                )

            if not all([
                nodelist.get(a) for a in ['version', 'nodes', 'updated_at']
            ]):
                return ff.log(
                    'this is no nodelist. wrong format',
                    level=False
                )

            return nodelist


def _nodelist_count(ff, nodelist):
    nodes, clients = 0, 0
    for node in nodelist.get('nodes', []):
        if node.get('status', {}).get('online', False):
            nodes += 1
        if node.get('status', {}).get('clients', False):
            clients += 1
    ff.log('found {} nodes, {} clients'.format(nodes, clients))

    if not all([nodes, clients]):
        ff.log('your nodelist seems to be empty', level=False)

    return nodes, clients


def _nodelist_dump(ff, nodes, clients):
    modified = []
    if ff.api.pull('state', 'nodes') is not None:
        ff.api.push(nodes, 'state', 'nodes')
        modified.append(True)

    if ff.api.pull('state', 'description') is not None:
        ff.api.push(
            '{} Nodes, {} Clients'.format(nodes, clients),
            'state', 'description'
        )
        modified.append(True)

    return any(modified)


def handle_nodelist(ff):
    if not ff.args.nodelist:
        return False

    nodelist = _nodelist_fetch(ff)
    if not nodelist:
        return False

    nodes, clients = _nodelist_count(ff, nodelist)
    if not all([nodes, clients]):
        return False

    return _nodelist_dump(ff, nodes, clients)
