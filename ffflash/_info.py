class Info:
    author = 'Frieder Griesshammer'
    author_email = 'frieder.griesshammer@der-beweis.de'
    name = 'ffflash'
    url = 'https://github.com/spookey/ffflash'
    version = '0.8'

    @property
    def release(self):
        return '{}{}'.format(self.version, '')
