import pytest

from ffflash.main import run


def test_main_no_or_empty_apifile(tmpdir):
    with pytest.raises(SystemExit):
        run([])

    assert run([str(tmpdir.join('phony_api_file.txt')), '-d']) is True

    assert tmpdir.remove() is None
