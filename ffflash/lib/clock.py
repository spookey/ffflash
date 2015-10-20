from datetime import datetime


def tstamp(dt=None):
    if not isinstance(dt, datetime):
        dt = datetime.utcnow()
    return dt


def iso_tstamp(dt=None):
    dt = tstamp(dt)
    return dt.isoformat('T')


def epoch_tstamp(dt=None, rel=0, ms=False):
    dt = tstamp(dt)
    res = (dt - datetime.utcfromtimestamp(rel)).total_seconds()
    if ms:
        return 1000 * res
    return res


def epoch_repr(ts=0, ms=False):
    res = []
    if isinstance(ts, (int, float)):
        if ms:
            ts = ts / 1000
        for name, sec in [
            ('a', 60*60*24*356.25),
            ('m', 60*60*24*(356.25/12)),
            ('w', 60*60*24*7),
            ('d', 60*60*24),
            ('h', 60*60),
            ('m', 60),
            ('s', 1),
        ]:
            if ts >= sec:
                val, ts = divmod(ts, sec)
                res.append('{:.0f}{}'.format(val, name))
    return ' '.join(res)
