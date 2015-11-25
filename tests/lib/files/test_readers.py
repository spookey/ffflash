import pytest


def test_readers_fallback(read_f):
    fn, ld, dp = read_f
    f = 'some file'

    assert fn(f) is None
    assert fn(f, '') == ''
    assert fn('', f) == f
    assert fn(f, False) is False
    assert fn(f, True) is True
    assert fn(f, {}) == {}


def test_readers_on_folders(tmpdir, read_f):
    fn, ld, dp = read_f
    assert fn('/') is None

    f = tmpdir.mkdir('folder')
    assert tmpdir.listdir() == [f]
    assert f.listdir() == []

    assert fn(str(tmpdir)) is None
    assert fn(str(f)) is None
    assert fn(str(f), 'fallback') == 'fallback'

    assert tmpdir.remove() is None


def test_readers_on_empty_file(tmpdir, read_f):
    fn, ld, dp = read_f

    e = tmpdir.join('empty_file')
    c = dp('')
    e.write_text(c, 'utf-8')

    assert not fn(str(e))
    assert fn(str(e)) == ld(c)
    assert fn(str(e), 'fallback') == ld(c)

    assert tmpdir.remove() is None


def test_readers_on_file(tmpdir, read_f):
    fn, ld, dp = read_f

    f = tmpdir.join('content')
    c = dp('some random unicode content 😺')
    f.write_text(c, 'utf-8')

    assert fn(str(f)) is not None
    assert fn(str(f)) == ld(c)
    assert fn(str(f), 'fallback') == ld(c)

    assert tmpdir.remove() is None


def test_readers_on_file_wrong_encoding(tmpdir, read_f):
    fn, ld, dp = read_f

    f = tmpdir.join('content')
    c = dp('Яне говорю по-русски')
    f.write_text(c, 'koi8_r')

    def check():
        assert fn(str(f)) is not None
        assert fn(str(f)) == ld(c)

    if fn.__name__ == 'lf':
        with pytest.raises(UnicodeDecodeError):
            check()
    else:
        check()

    assert tmpdir.remove() is None
