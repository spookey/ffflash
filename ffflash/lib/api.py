from ffflash.lib.text import make_pretty


class FFApi:
    '''
    Helper class provide some easy way to access and modify dictionaries.
    It only provides reading and replacing already existing keys.

    :param content: The initial data to work with
    '''
    def __init__(self, content):
        self.c = content

    def pretty(self):
        '''
        :return str: current content in a human readable way
            using **pprint.pformat**
        '''
        return make_pretty(self.c)

    def pull(self, *fields):
        '''
        Retrieve contents from deep down somewhere in the dictionary.

        :param fields: one or more key names to retrieve
        '''
        c = self.c
        for f in fields:
            if isinstance(c, dict) and f in c.keys():
                if f == fields[-1]:
                    return c[f]
                c = c[f]

    def push(self, value, *fields):
        '''
        Replace contents deeply inside the dictionary, if the key already
        exists.

        :param value: the actual data to be written
        :param fields: one or more key names where to write ``value``
        '''
        c = self.c
        for f in fields:
            if isinstance(c, dict) and f in c.keys():
                if f == fields[-1]:
                    c[f] = value
                c = c[f]
