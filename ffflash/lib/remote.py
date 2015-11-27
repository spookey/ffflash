from contextlib import contextmanager
from socket import gaierror
from urllib import error, request


@contextmanager
def www_fetch(url, fallback=None, timeout=5):
    '''
    Contextmanager to retrieve content from the web

    :param url: URL to fetch
    :param fallback: what to return instead in case of error
    :param timeout: timeout to pass to ``urllib.request``
    :yield str: fetched result as unicode string, or ``fallback``
    '''
    try:
        resp = request.urlopen(url, timeout=timeout)
        yield resp.read().decode('utf-8')
    except (error.HTTPError, error.URLError, gaierror, ValueError):
        yield fallback
