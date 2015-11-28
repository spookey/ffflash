from urllib import request

from ffflash.lib.remote import fetch_www


def test_fetch_www_wrong_urls():
    for wu in ['', '2342', '/']:
        with fetch_www(wu) as t:
            assert t is None


def test_fetch_www_fallback():
    for wu in ['', '2342', '/']:
        for fb in [None, True, False, 'wrong', {}]:
            with fetch_www(wu, fallback=fb) as t:
                assert t == fb


def test_fetch_www_patched_results(monkeypatch, fake_request):
    monkeypatch.setattr(request, 'urlopen', fake_request)

    for td in [
        'test', '🐸', '\n\t', ' ',
        '{\n\t"a": {\n\t\t"b": "c"\n\t}\n}'
    ]:
        with fetch_www(td) as t:
            assert t == td
