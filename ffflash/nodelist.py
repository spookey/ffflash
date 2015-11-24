from .lib.api import api_descr
from .lib.remote import www_fetch
from .lib.struct import struct_load


def _nodelist_fetch(ff):
    ff.log('fetching nodelist {}'.format(ff.args.nodelist))

    with www_fetch(ff.args.nodelist, fallback=None) as data:
        if not data:
            return ff.log(
                'could not fetch nodelist {} {}'.format(ff.args.nodelist),
                level=False
            )

        with struct_load(data, fallback=None, as_yaml=False) as nodelist:
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
    if ff.api is None:
        return False

    modified = []
    if ff.api.pull('state', 'nodes') is not None:
        ff.api.push(nodes, 'state', 'nodes')
        modified.append(True)

    descr = ff.api.pull('state', 'description')
    if descr is not None:
        new = '[{} Nodes, {} Clients]'.format(nodes, clients)
        new_descr = api_descr(
            r'(\[[\d]+ Nodes, [\d]+ Clients\])', new, descr
        ) if descr else new
        ff.api.push(new_descr, 'state', 'description')

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
