from os import path

from ffflash import RELEASE, log, now, timeout
from ffflash.lib.clock import epoch_repr
from ffflash.lib.data import merge_dicts
from ffflash.lib.files import read_json_file, write_json_file


class Container:
    def __init__(self, spec, filename):
        self._spec = spec
        self._location = path.abspath(filename)
        self.data = read_json_file(self._location, fallback={})

        self._info()

    def _info(self, info={}):
        self.data['_info'] = self.data.get('_info', {})
        self.data['_info']['generator'] = RELEASE

        self.data['_info']['access'] = self.data['_info'].get('access', {})
        if not self.data['_info']['access'].get('first', False):
            self.data['_info']['access']['first'] = now
        self.data['_info']['access']['last'] = now
        self.data['_info']['access']['overall'] = epoch_repr(
            abs(now - self.data['_info']['access']['first']),
            ms=True
        )
        self.data['_info']['access']['timeout'] = timeout

        if info:
            self.data['_info'] = merge_dicts(self.data['_info'], info)

    def save(self, info={}):
        self._info(info)
        if write_json_file(self._location, self.data):
            log.info('{} saved {}'.format(self._spec, self._location))
