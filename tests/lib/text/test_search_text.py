from ffflash.lib.text import search_text


def test_search_text_empty_input():
    for rx, txt in [
        (None, None), (r'', None), (None, ''), (r'', ''),
        (r'a', None), (None, 'a'), (r'a', ''), (r'', 'a')
    ]:
        assert not search_text(rx, txt)


def test_search_text():
    assert not search_text(r'a', 'b')
    assert search_text(r'a', 'a').group(0) == 'a'
    assert search_text(r'b', 'abcdef').group(0) == 'b'
    assert search_text(r'.*', 'abc').group(0) == 'abc'
    assert search_text(r'.', 'abc').group(0) == 'a'
    assert search_text(r'.+', 'abc').group(0) == 'abc'
    assert search_text(r'.{2}', 'abc').group(0) == 'ab'
    assert search_text(r'bc', 'abcdef').group(0) == 'bc'
    assert not search_text(r'bd', 'abcdef')
    assert search_text(r'b.d', 'abcdef').group(0) == 'bcd'

    b_d = search_text(r'b(.)d', 'abcdef')
    assert b_d.group(0) == 'bcd'
    assert b_d.group(1) == 'c'

    a_f = search_text(r'a(.(cd).)f', 'abcdef')
    assert a_f.group(0) == 'abcdef'
    assert a_f.group(1) == 'bcde'
    assert a_f.group(2) == 'cd'
