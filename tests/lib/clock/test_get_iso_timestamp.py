from datetime import datetime

from dateutil import parser

from ffflash.lib.clock import get_iso_timestamp


def test_get_iso_timestamp_dt_passed():
    now = datetime.now()
    utcnow = datetime.utcnow()

    assert parser.parse(get_iso_timestamp(now)) == now
    assert parser.parse(get_iso_timestamp(utcnow)) == utcnow


def test_get_iso_timestamp_no_dt():
    assert datetime.now() <= parser.parse(get_iso_timestamp())
    assert parser.parse(get_iso_timestamp()) <= datetime.now()
    assert (
        datetime.now() <= parser.parse(get_iso_timestamp()) <= datetime.now()
    )
