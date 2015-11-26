'''
To share common values like the package name or release string between
setuptools, sphinx and the code itself, the info module is used.
'''


class Info:
    '''
    Shared Information is stored in a class, for easy access.
    '''
    author = 'Frieder Griesshammer'
    author_email = 'frieder.griesshammer@der-beweis.de'
    description = 'FreiFunk File nodeList And Sidecar Helper'
    name = 'ffflash'
    url = 'https://github.com/spookey/ffflash'
    version = '0.9'
    _release = 'a2'

    @property
    def release(self):
        ''':return: ``version`` + ``_release``'''
        return '{}{}'.format(self.version, self._release)

    @property
    def download_url(self):
        ''':return: url constructed from ``url`` and ``release`` for tgz'''
        return '{}/archive/{}.tar.gz'.format(self.url, self.release)

info = Info()
