from ffflash.lib.locations import check_file_extension


def test_check_file_extension_no_ext():
    assert check_file_extension('file') == (None, None)
    assert check_file_extension('file', '') == (None, None)

    assert check_file_extension('file.txt') == (None, None)
    assert check_file_extension('file.txt', '') == (None, None)
    assert check_file_extension('file.txt', '.') == (None, None)
    assert check_file_extension('file.txt', '..') == (None, None)

    assert check_file_extension('file.txt', 'file') == (None, None)
    assert check_file_extension('file', 'file') == (None, None)


def test_check_file_extension():
    for ext in ['txt', '.txt', 'TXT', '.TXT', 'tXt', '.tXt', 'TxT', '.TxT']:
        assert check_file_extension('file.txt', ext) == ('file', '.txt')

    assert check_file_extension(
        'file.json', 'txt', 'yaml'
    ) == (None, None)
    assert check_file_extension(
        'file.json', 'txt', 'yaml', 'json'
    ) == ('file', '.json')


def test_check_file_extension_dir(tmpdir):
    assert check_file_extension(
        str(tmpdir.join('file.txt')), 'txt'
    ) == ('file', '.txt')
    assert check_file_extension(
        str(tmpdir.join('file.txt')), 'json'
    ) == (None, None)
    assert check_file_extension(
        str(tmpdir.join('file.txt'))
    ) == (None, None)
    assert check_file_extension(
        str(tmpdir.join('out')), 'txt'
    ) == (None, None)

    assert tmpdir.remove() is None
