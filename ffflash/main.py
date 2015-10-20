from ffflash import args, log
from ffflash.lib.args import spock
from ffflash.service import recent
from ffflash.store import Storage


def main():
    if not spock(args, log):
        log.error('wrong input. can\'t continue.')
        return 1

    storage = Storage(args.store)
    changes = storage.update()

    if changes and args.recent:
        recent(changes)
