from contextlib import contextmanager
from socket import gaierror
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


@contextmanager
def www_fetch(url, fallback=None):
    try:
        resp = urlopen(url)
        yield resp.read().decode('utf-8')
    except (HTTPError, URLError, gaierror):
        yield fallback
    return
