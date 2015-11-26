from contextlib import contextmanager
from socket import gaierror
from urllib import error, request


@contextmanager
def www_fetch(url, fallback=None, timeout=5):
    try:
        resp = request.urlopen(url, timeout=timeout)
        yield resp.read().decode('utf-8')
    except (error.HTTPError, error.URLError, gaierror, ValueError):
        yield fallback
