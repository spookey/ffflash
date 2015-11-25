

def test_writers_skip_empty_content(tmpdir, write_f):
    '''in fact only matters for the write_file method'''
    fn, dp, ld = write_f

    f = tmpdir.join('file')
    assert tmpdir.listdir() == []

    assert fn(str(f), None) == dp(None)

    assert tmpdir.remove() is None


def test_writers_skip_on_folders(tmpdir, write_f):
    fn, dp, ld = write_f

    f = tmpdir.mkdir('folder')
    assert tmpdir.listdir() == [f]
    assert f.listdir() == []

    assert fn(str(f), 'some content') is None

    assert tmpdir.listdir() == [f]
    assert f.listdir() == []

    assert tmpdir.remove() is None


def test_writers_on_file(tmpdir, write_f):
    fn, dp, ld = write_f

    f = tmpdir.join('file')
    c = dp('some random unicode content 😺')
    assert tmpdir.listdir() == []

    assert fn(str(f), c) is not None
    assert ld(f.read_text('utf-8')) == c

    assert tmpdir.listdir() == [f]

    assert tmpdir.remove() is None
