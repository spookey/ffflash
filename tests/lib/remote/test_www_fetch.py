from urllib import request

from ffflash.lib.remote import www_fetch


def test_www_fetch_wrong_urls():
    for wu in ['', '2342', '/']:
        with www_fetch(wu) as t:
            assert t is None


def test_www_fetch_fallback():
    for wu in ['', '2342', '/']:
        for fb in [None, True, False, 'wrong', {}]:
            with www_fetch(wu, fallback=fb) as t:
                assert t == fb


def test_www_decode_patched_results(monkeypatch):
    def r(u):
        class R:
            def read(self):
                return bytes(u, 'utf-8')

        return R()

    monkeypatch.setattr(request, 'urlopen', r)

    for td in ['test', '🐸', '\n\t', ' ']:
        with www_fetch(td) as t:
            assert t == td
