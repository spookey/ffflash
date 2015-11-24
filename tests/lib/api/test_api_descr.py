from ffflash.lib.api import api_descr


def test_api_descr_wrong_params():
    u = 'unchanged'
    assert api_descr('', '', '') == ''
    assert api_descr(r'', '', '') == ''
    assert api_descr('', '', u) == u
    assert api_descr(r'', '', u) == u


def test_api_descr():
    text = 'a b c'
    assert api_descr(r'b', 'd', text) == 'a d c'
    assert api_descr(r'.*(b).*', 'd', text) == 'd'
    assert api_descr(r'.*', 'e', text) == 'e'
    assert api_descr(r'.+', 'f', text) == 'f'
    assert api_descr(r'.', 'g', text) == 'g' * len(text)
