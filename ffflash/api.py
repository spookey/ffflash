from datetime import datetime


class FFApi:
        def __init__(self, content):
            self.c = content

        def pull(self, *fields):
            c = self.c
            for f in fields:
                if f in c.keys():
                    if f == fields[-1]:
                        return c[f]
                    c = c[f]

        def push(self, value, *fields):
            c = self.c
            for f in fields:
                if f in c.keys():
                    if f == fields[-1]:
                        c[f] = value
                    c = c[f]

        def timestamp(self):
            if self.pull('state', 'lastchange') is not None:
                self.push(api_timestamp(), 'state', 'lastchange')


def api_timestamp(dt=None):
    if not dt:
        dt = datetime.now()
    return dt.isoformat('T')
