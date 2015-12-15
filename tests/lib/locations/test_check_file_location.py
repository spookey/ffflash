from ffflash.lib.locations import check_file_location


def test_check_file_location_empty():
    assert check_file_location('', must_exist=True) is None
    assert check_file_location('', must_exist=False) is None


def test_check_file_location_on_folders(tmpdir):
    pf = tmpdir.join('parent')
    ne = pf.join('does_not_exist')

    assert tmpdir.listdir() == []

    assert check_file_location(str(ne), must_exist=False) is None
    assert check_file_location(str(ne), must_exist=True) is None

    assert check_file_location(str(pf), must_exist=False) == str(pf)
    assert check_file_location(str(pf), must_exist=True) is None

    assert tmpdir.remove() is None


def test_check_file_location(tmpdir):
    ne = tmpdir.join('does_not_exist')
    de = tmpdir.ensure('does_exist')

    assert check_file_location(str(ne), must_exist=False) == str(ne)
    assert check_file_location(str(ne), must_exist=True) is None

    assert check_file_location(str(de), must_exist=False) == str(de)
    assert check_file_location(str(de), must_exist=True) == str(de)

    assert tmpdir.remove() is None
