from datetime import datetime
from json import dumps, loads
from os import path
from sys import exit
from time import time


def readin(filename):
    '''reads json'''
    try:
        ffapi = str()
        if path.exists(filename):
            ffapi = filename
        elif path.exists(path.join(
                path.abspath(path.dirname(__file__)),
                filename)
        ):
            ffapi = path.join(path.abspath(path.dirname(__file__)), filename)
        else:
            raise Exception('json file not found')

        with open(ffapi, 'r') as fn:
            return loads(fn.read())

    except Exception as ex:
        exit(ex)


def writeout(filename, content):
    '''writes json'''
    try:
        with open(filename, 'w') as fn:
            return fn.write(dumps(content, indent=4))
    except Exception as ex:
        exit(ex)


def tstamp(short=False):
    '''get timestamp'''
    if short:
        return int(time())
    return datetime.now().isoformat('T')


class Loader(object):
    '''replace existing fields'''
    def __init__(self, filename):
        super(Loader, self).__init__()
        self.filename = filename
        self.ffapi = readin(self.filename)

    def dump(self, overwrite=False):
        '''writes ffapi'''
        if self.ffapi:
            filename = self.filename if overwrite else self.filename.replace(
                '.json', '_change.json'
            )
            self.set(['state', 'lastchange'], tstamp(short=False))
            return writeout(filename, self.ffapi)

    def get(self):
        '''get ffapi'''
        return self.ffapi

    def find(self, fields):
        '''finds fields'''
        scope = self.ffapi
        for field in fields:
            if field in scope.keys():
                if field == fields[-1]:
                    return scope[field]
                scope = scope[field]

    def set(self, fields, value):
        '''sets fields'''
        scope = self.ffapi
        for field in fields:
            if field in scope.keys():
                if field == fields[-1]:
                    scope[field] = value
                scope = scope[field]    # Pointerfun with Blinky!

if __name__ == '__main__':
    loader = Loader('ffapi_file.json')

    print('name => %s\n' % (loader.find(['name'])))
    print('location,city => %s\n' % (loader.find(['location', 'city'])))

    loader.set(['api'], '1.2.3')

    loader.dump(overwrite=False)
