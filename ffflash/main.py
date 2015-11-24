from pprint import pprint

from .api import FFApi
from .lib.files import dump_file, load_file
from .lib.args import args
from .nodelist import handle_nodelist
from .sidecars import handle_sidecars


class FFFlash:
    def __init__(self, argv=None):
        self.args = args(argv)

        c = load_file(self.args.APIfile, fallback={}, as_yaml=False)
        self.api = FFApi(c)

    def save(self):
        self.api.timestamp()
        return dump_file(self.args.APIfile, self.api.c, as_yaml=False)

    def log(self, message, level=True):
        c = {
            True: 'info', None: 'warn', False: 'error'
        }.get(level, level)

        if self.args.verbose or level is not True:
            print('{}\t{}'.format(c.upper(), message))
        return level


def main(argv=None):
    ff = FFFlash(argv)
    modified = [
        handle_nodelist(ff),
        handle_sidecars(ff)
    ]

    if ff.args.dry:
        ff.log('dry option selected  - preview')
        pprint(ff.api.c)
    else:
        if any(modified):
            ff.log('saving api file')
            ff.save()

    return not any(modified)
