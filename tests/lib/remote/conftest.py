import pytest


@pytest.fixture
def fake_request(request):
    def r(read_result, *args, **kwargs):
        class R:
            def read(self):
                return bytes(read_result, 'utf-8')

        return R()

    return r
