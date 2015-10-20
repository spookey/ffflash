from sys import stderr, stdout


class AwesomeLogger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def _print(self, msg, sgn='#', **kwargs):
        print('{} {}'.format(sgn, msg), **kwargs)

    def info(self, msg, **kwargs):
        if self.verbose:
            self._print(msg, file=stdout, **kwargs)

    def warn(self, msg, **kwargs):
        self._print(msg, file=stderr, **kwargs)

    def error(self, msg, **kwargs):
        self._print(msg, sgn='%', file=stderr, **kwargs)
