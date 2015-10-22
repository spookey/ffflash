from ffflash import args, log
from ffflash.lib.args import spock
from ffflash.service import recent
from ffflash.store import Storage
from ffflash.poll import poll


def main():
    if not spock(args, log):
        log.error('wrong input. can\'t continue.')
        return 1

    storage = Storage(args.store)
    fresh = poll()
    changes = storage.update(fresh)

    if changes and args.recent:
        recent(changes)
