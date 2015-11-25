from .main import main
ffflash = main


class Info:
    author = 'Frieder Griesshammer'
    email = 'frieder.griesshammer@der-beweis.de'
    name = 'ffflash'
    url = 'https://github.com/spookey/ffflash'
    version = '0.7'

    @property
    def release(self):
        return '{}{}'.format(self.version, 'a9')

_info = Info()
