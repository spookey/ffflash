from os import path

from ffflash import RELEASE, log, now, timeout
from ffflash.lib.clock import epoch_repr
from ffflash.lib.data import Element
from ffflash.lib.files import read_json_file, write_json_file


class Container:
    def __init__(self, spec, filename):
        self._spec = spec
        self._location = path.abspath(filename)

        content = read_json_file(self._location, fallback={})

        self.info = Element(content.get('_info', {}))
        self.data = Element(content.get(self._spec, {}))

    def _info(self):
        self.info.generator = RELEASE

        if not self.info.access.first:
            self.info.access.first = now
        self.info.access.last = now
        self.info.access.overall = epoch_repr(
            abs(now - self.info.access.first), ms=True
        )
        self.info.access.scrub = timeout
        self.info.access.spec = self._spec

    def save(self):
        if not self.data:
            log.warn('skipped {} save - empty data'.format(self._spec))
            return

        self._info()
        content = {
            '_info': self.info,
            self._spec: self.data
        }
        if write_json_file(self._location, content):
            log.info('{} saved {}'.format(self._spec, self._location))
