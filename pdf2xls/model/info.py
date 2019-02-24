'info.Info is a namedtuple'

import datetime
import decimal
import typing

from . import keys


class InfoPoint(typing.NamedTuple):
    when: datetime.datetime
    howmuch: decimal.Decimal


class Info(typing.NamedTuple):
    when: datetime.datetime
    howmuch: decimal.Decimal
    feature: keys.Keys


def infoPoint(info: Info) -> InfoPoint:
    'convert an info to an infopoint'
    return InfoPoint(info.when, info.howmuch)
