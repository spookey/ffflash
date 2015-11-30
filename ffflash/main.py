from ffflash.info import info
from ffflash.lib.api import FFApi
from ffflash.lib.args import parsed_args
from ffflash.lib.files import check_file_location, dump_file, load_file
from ffflash.inc.nodelist import handle_nodelist
from ffflash.inc.sidecars import handle_sidecars


class FFFlash:
    def __init__(self, args):
        self.args = args
        self.location = check_file_location(self.args.APIfile, must_exist=True)
        self.api = None

        self.load_api()

    def load_api(self):
        if (self.api is None) and self.location:
            c = load_file(self.location, as_yaml=False)
            if c:
                self.api = FFApi(c)

    def save(self):
        if (self.api is not None) and self.location:
            self.api.timestamp()
            return dump_file(self.location, self.api.c, as_yaml=False)

    def access_for(self, name):
        return all([
            (self.api is not None),
            {
                'sidecars': self.args.sidecars,
                'nodelist': self.args.nodelist,
                'rankfile': (self.args.nodelist and self.args.rankfile),
            }.get(name, False)
        ])

    def log(self, message, level=True):
        c = {
            True: 'info', None: 'warn', False: 'error'
        }.get(level, level) if (
            level is None or isinstance(level, (bool, str))
        ) else 'output'

        if self.args.verbose or level is not True:
            print('{}\t{}'.format(c.upper(), message))
        return level


def run(argv=None):
    ff = FFFlash(parsed_args(argv))

    ff.log(info.ident)

    if ff.api is None:
        return not ff.log('Error loading API file', level=False)

    modified = [
        handle_sidecars(ff),
        handle_nodelist(ff)
    ]

    if ff.args.dry:
        ff.log('\n{}'.format(ff.api.pretty()), level='API file preview')
    else:
        if any(modified):
            ff.log('saving api file'.format(
                ff.save()
            ))

    return not any(modified)
