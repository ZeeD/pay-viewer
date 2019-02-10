'info.Info is a namedtuple'

import datetime
import decimal
import typing


class InfoPoint(typing.NamedTuple):
    when: datetime.datetime
    howmuch: decimal.Decimal


class Info(InfoPoint):
    feature: str

    def infoPoint(self) -> InfoPoint:
        return InfoPoint(self.when, self.howmuch)
