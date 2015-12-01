'''
To share common values like the package name or release string between
setuptools, sphinx and the code itself, the info module is used.
'''


class Info:
    '''
    Shared Information is stored in a class, for easy access.
    '''
    def __init__(self):
        self.author = 'Frieder Griesshammer'
        self.author_email = 'frieder.griesshammer@der-beweis.de'
        self.description = 'FreiFunk File nodeList And Sidecar Helper'
        self.cname = 'FFFlash'
        self.url = 'https://github.com/spookey/ffflash'
        self.doc_url = 'https://ffflash.readthedocs.org'
        self.pkg_url = 'https://pypi.python.org/pypi/ffflash'
        self.version = '0.9'

        self.name = self.cname.lower()
        self.release = '{}{}'.format(self.version, 'a6')
        self.ident = '{} {}'.format(self.name, self.release)
        self.download_url = '{}/archive/{}.tar.gz'.format(
            self.url, self.release
        )

    @property
    def rst_epilog(self):
        '''
        :return str: Restructured Text with substitutions for the info values,
            so they can be displayed in sphinx documentation
        '''
        return '\n\n'.join([
            '.. |info_{}| replace:: {}'.format(k, v)
            for k, v in self.__dict__.items()
        ])


info = Info()
