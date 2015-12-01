import pytest

from ffflash.lib.args import parsed_args
from ffflash.main import FFFlash


@pytest.fixture
def fffake(request):
    def fake_ffflash(
        apifile,
        nodelist=None, rankfile=None,
        dry=False, verbose=False,
        sidecars=[]
    ):
        a = [str(apifile)]
        if nodelist:
            a.extend(['-n', str(nodelist)])
        if rankfile:
            a.extend(['-r', str(rankfile)])
        if dry:
            a.append('-d')
        if verbose:
            a.append('-v')
        if sidecars:
            a.append('-s')
            [a.append(str(s)) for s in sidecars]
        return FFFlash(parsed_args(a))

    return fake_ffflash
