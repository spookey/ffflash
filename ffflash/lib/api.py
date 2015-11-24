from datetime import datetime
from pprint import pformat
from re import search as re_search
from re import sub as re_sub


class FFApi:
        def __init__(self, content):
            self.c = content

        def pull(self, *fields):
            c = self.c
            for f in fields:
                if isinstance(c, dict) and f in c.keys():
                    if f == fields[-1]:
                        return c[f]
                    c = c[f]

        def push(self, value, *fields):
            c = self.c
            for f in fields:
                if isinstance(c, dict) and f in c.keys():
                    if f == fields[-1]:
                        c[f] = value
                    c = c[f]

        def timestamp(self):
            if self.pull('state', 'lastchange') is not None:
                self.push(api_timestamp(), 'state', 'lastchange')

        def show(self):
            return pformat(self.c)


def api_timestamp(dt=None):
    if not dt:
        dt = datetime.now()
    return dt.isoformat('T')


def api_descr(rx, rplc, txt):
    match = re_search(rx, txt)
    if match:
        txt = re_sub(rx, rplc, txt)
    return txt
