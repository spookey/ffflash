from sys import argv

from ffflash.lib.args import main_args
from ffflash.lib.clock import epoch_tstamp
from ffflash.lib.logger import AwesomeLogger

args = main_args(argv[1:])
log = AwesomeLogger(verbose=args.verbose)
now = epoch_tstamp(ms=True)
timeout = epoch_tstamp(rel=float(args.timeout), ms=True)

CODING = 'UTF-8'

from ffflash.main import main


def run():
    return main()
