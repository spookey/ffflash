from os import path

from ffflash.lib.files import check_file_location, dump_file, load_file
from ffflash.lib.struct import merge_dicts


def _sidecar_path(ff, sc):
    '''
    Check passed sidecars for valid paths, format (*json* or *yaml*) and for
    valid filenames (no double dots).

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :param sc: sidecar as passed by user
    :return: Tuple of either (``False``, ``None``, ``None``) on error or:

        * normalized and full path to ``sc``
        * unvalidated key-names into api-file
        * ``True`` if ``sc`` is a *yaml* file, ``False`` if it's *json*

    '''
    ff.log('handling sidecar {}'.format(sc))

    sidepath = check_file_location(sc)
    if not sidepath:
        return ff.log(
            'sidecar {} is either a folder, or parent folder does '
            'not exist yet skipping'.format(sc),
            level=False
        ), None, None

    sidename = path.basename(sidepath)
    name, ext = path.splitext(sidename)

    if not ext or ext.lower() not in ['.yaml', '.json']:
        return ff.log(
            'sidecar {} {} is neither json nor yaml'.format(sc, ext),
            level=False
        ), None, None

    fields = name.split('.')
    if not all([f for f in fields]):
        return ff.log(
            'sidecar {} {} name is invalid '
            '(check for double dots)'.format(sc, name),
            level=False
        ), None, None

    ff.log('sidecar path {} is valid. got {}'.format(sidepath, fields))
    return sidepath, fields, (True if ext == '.yaml' else False)


def _sidecar_load(ff, sidepath, fields, as_yaml):
    '''
    Loads content from ``sidepath`` if it exists, otherwise returns the values
    from the :attr:`api` instead.
    This is only done, if ``fields`` exist in :attr:`api`.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :param sidepath: full path to the sidecar
    :param fields: key-names into api-file
    :param as_yaml: load as *yaml* instead of *json*
    :return: The loaded content of ``sidepath`` or ``False``/``None`` on error
    '''
    if not ff.access_for('sidecars'):
        return False

    ff.log('searching for {}'.format('.'.join(fields)))

    apicont = ff.api.pull(*fields)
    if apicont is None:
        return ff.log(
            '{} does not exist. skipping'.format('.'.join(fields)),
            level=None
        )

    sidecont = load_file(sidepath, as_yaml=as_yaml)
    if sidecont is None:
        ff.log('sidecar {} does not exit yet. pulled data from api'.format(
            '.'.join(fields)
        ))
        return apicont

    return merge_dicts(apicont, sidecont)


def _sidecar_dump(ff, sidepath, content, fields, as_yaml):
    '''
    Stores ``content`` both in :attr:`api` and ``sidepath``.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :param sidepath: full path to the sidecar
    :param content: the value to store into sidecar/api-file
    :param fields: key-names into api-file
    :param as_yaml: dump as *yaml* instead of *json*
    :return: ``True`` if ``sidepath`` was modified else ``False``
    '''
    if not ff.access_for('sidecars'):
        return False

    if ff.api.pull(*fields) is None:
        return ff.log(
            '{} does not exist. can\'t push'.format('.'.join(fields)),
            level=None
        )

    ff.api.push(content, *fields)
    dump_file(sidepath, content, as_yaml=as_yaml)
    ff.log('saved sidecar {}'.format(sidepath))
    return True


def handle_sidecars(ff):
    '''
    Entry function to handle passed ``--sidecars``. Validating locations, names
    and content of sidecars. Generating them if necessary and update
    :attr:`api`.

    :param ff: running :class:`ffflash.main.FFFlash` instance
    :return: ``True`` if any sidecar was modified else ``False``
    '''
    if not ff.access_for('sidecars'):
        return False

    modified = []

    for sidecar in sorted(ff.args.sidecars):

        sidepath, fields, as_yaml = _sidecar_path(ff, sidecar)
        if not all([sidepath, fields, as_yaml is not None]):
            continue

        content = _sidecar_load(ff, sidepath, fields, as_yaml)
        if not content:
            continue

        modified.append(
            _sidecar_dump(ff, sidepath, content, fields, as_yaml)
        )

    return any(modified)
