from os import path

from .lib.files import check_file_location, dump_file, load_file
from .lib.struct import merge_dicts


def _sidecar_path(ff, sc):
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

    return sidepath, fields, (True if ext == '.yaml' else False)


def _sidecar_load(ff, sidepath, fields, as_yaml):
    if ff.api is None:
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
        return apicont

    return merge_dicts(apicont, sidecont)


def _sidecar_dump(ff, sidepath, content, fields, as_yaml):
    if ff.api is None:
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
    if not ff.args.sidecars:
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
