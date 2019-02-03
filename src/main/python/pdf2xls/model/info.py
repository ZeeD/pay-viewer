'info.Info is a namedtuple'

import typing
import datetime
import decimal

class Info(typing.NamedTuple):
    feature: str
    when: datetime.datetime
    howmuch: decimal.Decimal
