from json import loads
from socket import gaierror
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def _nodelist_fetch(ff):
    ff.log('fetching nodelist {}'.format(ff.args.nodelist))

    try:
        resp = urlopen(ff.args.nodelist)
        data = resp.read().decode('utf-8')
        nodelist = loads(data)
    except (HTTPError, URLError, gaierror, ValueError) as ex:
        return ff.log(
            'could not fetch nodelist {} {}'.format(ff.args.nodelist, ex),
            level=False
        )

    if not all([nodelist.get(a) for a in ['version', 'nodes', 'updated_at']]):
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
