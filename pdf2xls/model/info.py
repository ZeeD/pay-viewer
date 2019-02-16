'info.Info is a namedtuple'

import datetime
import decimal
import typing


class InfoPoint(typing.NamedTuple):
    when: datetime.datetime
    howmuch: decimal.Decimal


class Info(typing.NamedTuple):
    when: datetime.datetime
    howmuch: decimal.Decimal
    feature: str


def infoPoint(info: Info) -> InfoPoint:
    'convert an info to an infopoint'
    return InfoPoint(info.when, info.howmuch)
