from ffflash.lib.text import replace_text


def test_replace_text_empy_input():
    for rx, rpl, txt in [
        ('', '', ''), (r'', '', ''),
        ('', '', 'unchanged'), (r'', '', 'unchanged'),
        ('', '', None), (r'', '', None),
        ('', None, None), (r'', None, None),
        (None, None, None)
    ]:
        assert replace_text(rx, rpl, txt) == txt


def test_replace_text_returns_original_on_no_match():
    for rx, rpl, txt in [
        (r'a', 'b', 'c'), (r'aa', 'bb', 'cc'),
        (r'a{2}', 'bb', 'a'), (r'.a', 'b', 'a')
    ]:
        assert replace_text(rx, rpl, txt) == txt


def test_replace_text():
    assert replace_text(r'b', 'd', 'abc') == 'adc'
    assert replace_text(r'b', 'd', 'abbc') == 'addc'
    assert replace_text(r'a(.+)f', 'g', 'abcdef') == 'g'
    assert replace_text(r'(a.+f)', 'g', 'abcdef') == 'g'
    assert replace_text(r'(a(.+)f)', 'g', 'abcdef') == 'g'

    assert replace_text(r'\ ', '_', 'abc def') == 'abc_def'
    assert replace_text(r'\d{3}', '0', 'abc123') == 'abc0'
