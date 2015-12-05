from operator import itemgetter
from os import path

from ffflash.info import info
from ffflash.lib.api import api_timestamp
from ffflash.lib.files import check_file_location, dump_file, load_file


def _rankfile_load(ff):
    if not ff.access_for('rankfile'):
        return (False, None, None)
    ff.log('handling rankfile {}'.format(ff.args.rankfile))

    rankfile = check_file_location(ff.args.rankfile, must_exist=False)
    if not rankfile:
        return ff.log(
            'wrong path for rankfile {}'.format(ff.args.rankfile),
            level=False
        ), None, None
    _, ext = path.splitext(rankfile)
    if not ext or ext.lower() not in ['.yaml', '.json']:
        return ff.log(
            'rankfile {} {} is neither json nor yaml'.format(rankfile, ext),
            level=False
        ), None, None
    as_yaml = True if ext == '.yaml' else False

    ranks = load_file(rankfile, fallback={
        'updated_at': 'never', 'nodes': []
    }, as_yaml=as_yaml)

    if not ranks or not isinstance(ranks, dict):
        return ff.log(
            'could not load rankfile {}'.format(rankfile),
            level=False
        ), None, None

    if not all([(a in ranks) for a in ['nodes', 'updated_at']]):
        return ff.log(
            'this is no rankfile {}'.format(rankfile),
            level=False
        ), None, None

    lranks = len(ranks.get('nodes', 0))
    ff.log((
        'creating new rankfile {}'.format(rankfile)
        if lranks == 0 else
        'loaded {} nodes'.format(lranks)
    ))

    return rankfile, ranks, as_yaml


def _rankfile_score(ff, ranks, nodelist):
    if not ff.access_for('rankfile'):
        return False
    if not all([
        ranks, isinstance(ranks, dict), ranks and 'nodes' in ranks,
        nodelist, isinstance(nodelist, dict), nodelist and 'nodes' in nodelist,
    ]):
        return ff.log('wrong input data passed', level=False)

    res = []
    exist = dict(
        (node.get('id'), node.get('score')) for node in ranks.get('nodes', [])
    )
    for node in nodelist.get('nodes', []):
        nid = node.get('id')
        if not nid:
            ff.log('node without id {}'.format(node))
            continue
        nr = {
            'id': nid,
            'score': exist.get(nid, ff.args.rankwelcome),
            'name': node.get('name')
        }

        if node.get('position', False):
            nr['score'] += ff.args.rankposition
        if node.get('status', {}).get('online', False):
            nr['score'] += ff.args.rankonline
            nr['online'] = True
            cl = node.get('status', {}).get('clients', 0)
            nr['score'] += (ff.args.rankclients * cl)
            nr['clients'] = cl
        else:
            nr['score'] -= ff.args.rankoffline
            nr['online'] = False
            nr['clients'] = 0
        if nr['score'] > 0:
            res.append(nr)

    ranks['nodes'] = list(sorted(res, key=itemgetter('score'), reverse=True))
    return ranks


def _rankfile_dump(ff, rankfile, ranks, as_yaml):
    if not ff.access_for('rankfile'):
        return False
    if not all([
        rankfile, ranks, isinstance(ranks, dict), all([
            (a in ranks) for a in ['nodes', 'updated_at'] if ranks
        ]), (as_yaml is not None)
    ]):
        return ff.log('wrong input data passed', level=False)

    ranks['updated_at'] = api_timestamp()
    ranks['version'] = info.release
    dump_file(rankfile, ranks, as_yaml=as_yaml)

    return True


def handle_rankfile(ff, nodelist):
    '''
    Entry function gather results from a retrieved ``--nodelist``  to store it
    into the ``--rankfile``.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :return: ``True`` if rankfile was modified else ``False``
    '''
    if not ff.access_for('rankfile'):
        return False
    if not nodelist or not isinstance(nodelist, dict):
        return False

    rankfile, ranks, as_yaml = _rankfile_load(ff)
    if not all([rankfile, ranks, (as_yaml is not None)]):
        return False

    ranks = _rankfile_score(ff, ranks, nodelist)
    if not ranks:
        return False

    return _rankfile_dump(ff, rankfile, ranks, as_yaml)
