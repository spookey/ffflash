from contextlib import contextmanager
from shlex import split as s_split
from subprocess import PIPE, Popen

from ffflash import args, log


@contextmanager
def launch(cmdline):
    if isinstance(cmdline, str):
        cmdline = s_split(cmdline)
    if isinstance(cmdline, list) and cmdline and all(cmdline):
        try:
            log.info('launching {}'.format(' '.join(cmdline)))
            res = Popen(cmdline, stdout=PIPE, stderr=PIPE)
            out, err = res.communicate()

            if err is not None:
                err = err.decode().strip()
            if out is not None:
                out = out.decode().strip()

            yield res.returncode, out, err
        except OSError as ex:
            log.error('launch error {}'.format(ex))
            yield -1, None, None
    else:
        yield None, None, None


def ssh_wrapper(cmdline):
    if args.ssh:
        return 'ssh {opt} "{cmdline}"'.format(
            cmdline=cmdline,
            opt=args.ssh,
        )
    return cmdline


def construct_alfred_command(channel):
    return ssh_wrapper(
        '{sudo}{command} -z -f json -r {channel} -s {socket}'.format(
            channel=channel,
            command=args.ajson,
            socket=args.asock,
            sudo='sudo ' if args.sudo else ''
        )
    )
