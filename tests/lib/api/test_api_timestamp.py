from datetime import datetime

from dateutil import parser

from ffflash.lib.api import api_timestamp


def test_api_timestamp_dt_passed():
    now = datetime.now()
    utcnow = datetime.utcnow()

    assert parser.parse(api_timestamp(now)) == now
    assert parser.parse(api_timestamp(utcnow)) == utcnow


def test_api_timestamp_no_dt():
    assert datetime.now() <= parser.parse(api_timestamp())
    assert parser.parse(api_timestamp()) <= datetime.now()
    assert datetime.now() <= parser.parse(api_timestamp()) <= datetime.now()
