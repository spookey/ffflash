from contextlib import contextmanager
from socket import gaierror
from urllib import error, request

from ffflash.lib.files import load_struct


@contextmanager
def fetch_www(url, fallback=None, timeout=5):
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


def fetch_www_struct(url, fallback=None, timeout=5, as_yaml=False):
    '''
    Helper to unpickle either *json* or *yaml* from fetched files

    :param url: URL to fetch
    :param fallback: what to return in case of (fetch or unpickle) error
    :param timeout: timeout to pass down to :meth:`fetch_www`
    :param as_yaml: load content as *yaml* instead of *json*
    :return: unpickled data from ``url``
    '''
    with fetch_www(url, fallback=None, timeout=timeout) as resp:
        with load_struct(resp, fallback=fallback, as_yaml=as_yaml) as data:
            return data
