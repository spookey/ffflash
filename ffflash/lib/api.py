from pprint import pformat
from re import search as re_search
from re import sub as re_sub


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
        return pformat(self.c)

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


def api_descr(rx, replace, text):
    '''
    Replace text if rx matches, or leave text unchanged

    :param rx: regex to match on ``text``
    :param replace: content to put into ``text`` on ``rx``
    :param text: content to work on
    :return str: ``text`` with replaced parts, or unchanged ``text``
    '''
    match = (
        False if not (rx and text) else re_search(rx, text)
    )
    if match and replace:
        text = re_sub(rx, replace, text)
    return text
