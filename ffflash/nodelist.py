from .lib.api import api_descr
from .lib.files import check_file_location, load_file
from .lib.remote import www_fetch
from .lib.struct import struct_load


def _nodelist_fetch(ff):
    ff.log('fetching nodelist {}'.format(ff.args.nodelist))

    def _remote(url):
        with www_fetch(url, fallback=None) as response:
            if not response:
                return ff.log(
                    'could not fetch nodelist {}'.format(url),
                    level=False
                )
            with struct_load(response, fallback=None, as_yaml=False) as data:
                if not data:
                    return ff.log(
                        'could not unload nodelist {}'.format(url)
                    )
                return data

    location = check_file_location(ff.args.nodelist, must_exist=True)
    nodelist = (
        load_file(location, fallback=None, as_yaml=False)
        if location else
        _remote(ff.args.nodelist)
    )

    if not isinstance(nodelist, dict) or not all([
        nodelist.get(a) for a in ['version', 'nodes', 'updated_at']
    ]):
        return ff.log(
            '{} is no nodelist. wrong format'.format(ff.args.nodelist),
            level=False
        )

    return nodelist


def _nodelist_count(ff, nodelist):
    nodes, clients = 0, 0
    for node in nodelist.get('nodes', []):
        if node.get('status', {}).get('online', False):
            nodes += 1
            clients += node.get('status', {}).get('clients', 0)
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
