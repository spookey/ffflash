from ffflash.inc.rankfile import handle_rankfile
from ffflash.lib.api import api_descr
from ffflash.lib.files import check_file_location, load_file
from ffflash.lib.remote import fetch_www_struct


def _nodelist_fetch(ff):
    '''
    Determines if ``--nodelist`` was a file or a url, and tries to fetch it.
    Validates nodelist to be json and to have the *version*, *nodes* and
    *updated_at* keys.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :return: the unpickled nodelist or ``False``/``None`` on error
    '''
    if not ff.access_for('nodelist'):
        return False

    ff.log('fetching nodelist {}'.format(ff.args.nodelist))

    nodelist = (
        load_file(ff.args.nodelist, fallback=None, as_yaml=False)
        if check_file_location(ff.args.nodelist, must_exist=True) else
        fetch_www_struct(ff.args.nodelist, fallback=None, as_yaml=False)
    )
    if not nodelist or not isinstance(nodelist, dict):
        return ff.log(
            'Could not fetch nodelist {}'.format(ff.args.nodelist),
            level=False
        )

    if not all([
        nodelist.get(a) for a in ['version', 'nodes', 'updated_at']
    ]):
        return ff.log(
            'This is no nodelist {}'.format(ff.args.nodelist),
            level=False
        )

    return nodelist


def _nodelist_count(ff, nodelist):
    '''
    Count online nodes and sum up their clients from a nodelist.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :param nodelist: nodelist from :meth:`_nodelist_fetch`, should contain a
        list of dictionaries at the key *nodes*
    :return: Tuple of counted nodes and clients
    '''
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
    '''
    Store the counted numbers in the api-file.

    Sets the key ``state`` . ``nodes`` with the node number.

    Leaves ``state`` . ``description`` untouched, if any already present.
    If empty, or the pattern ``\[[\d]+ Nodes, [\d]+ Clients\]`` is matched,
    the numbers in the pattern will be replaced.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :param nodes: Number of online nodes
    :param clients: Number of their clients
    :return: ``True`` if :attr:`api` was modified else ``False``
    '''
    if not ff.access_for('nodelist'):
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
    '''
    Entry function to receive a ``--nodelist`` and store determined results
    into both :attr:`api` and ``--rankfile`` (if specified).

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :return: ``True`` if :attr:`api` was modified else ``False``
    '''
    if not ff.access_for('nodelist'):
        return False

    nodelist = _nodelist_fetch(ff)
    if not nodelist:
        return False

    modified = []

    nodes, clients = _nodelist_count(ff, nodelist)
    if all([nodes, clients]):
        modified.append(
            _nodelist_dump(ff, nodes, clients)
        )

    if ff.access_for('rankfile'):
        modified.append(
            handle_rankfile(ff, nodelist)
        )

    return any(modified)
