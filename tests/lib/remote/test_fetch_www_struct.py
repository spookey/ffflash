from json import dumps as j_dump
from urllib import request

from yaml import dump as y_dump

from ffflash.lib.remote import fetch_www_struct


def test_fetch_www_struct_fallback():
    for wu in ['', '2342', '/']:
        for fb in [None, True, False, 'wrong', {}, [], [1, 2, 3]]:
            assert fetch_www_struct(wu, fallback=fb) == fb


def test_fetch_www_struct_generic(monkeypatch, fake_request):
    monkeypatch.setattr(request, 'urlopen', fake_request)

    for asy in [True, False]:
        assert fetch_www_struct('', as_yaml=asy) is None
        assert fetch_www_struct('""', as_yaml=asy) == ''
        assert fetch_www_struct('"test"', as_yaml=asy) == 'test'


def test_fetch_www_struct_load(monkeypatch, fake_request):
    monkeypatch.setattr(request, 'urlopen', fake_request)

    for dt in [
        'test', 23, [42, None], True, {"a": "b"}, {"c": {"d": 0}}
    ]:
        for asy, df in [(True, y_dump), (False, j_dump)]:
            assert fetch_www_struct(df(dt), as_yaml=asy) == dt
