from pprint import pprint

from .lib.files import dump_file, load_file
from .lib.service import api_timestamp, args
from .nodelist import handle_nodelist
from .sidecars import handle_sidecars


class FFFlash:
    class FFApi:
        def __init__(self, content):
            self.c = content

        def pull(self, *fields):
            c = self.c
            for f in fields:
                if f in c.keys():
                    if f == fields[-1]:
                        return c[f]
                    c = c[f]

        def push(self, value, *fields):
            c = self.c
            for f in fields:
                if f in c.keys():
                    if f == fields[-1]:
                        c[f] = value
                    c = c[f]

        def timestamp(self):
            if self.pull('state', 'lastchange') is not None:
                self.push(api_timestamp(), 'state', 'lastchange')

    def __init__(self, argv=None):
        self.args = args(argv)
        print(self.args)

        c = load_file(self.args.APIfile, fallback={}, as_yaml=False)
        self.api = self.FFApi(c)

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
