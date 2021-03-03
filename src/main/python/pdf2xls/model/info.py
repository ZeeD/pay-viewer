'info.Info is a namedtuple'

from datetime import date
from decimal import Decimal
from typing import NamedTuple
from typing import Optional

from . import keys


class InfoPoint(NamedTuple):
    when: date
    howmuch: Optional[Decimal]


class InfoDetail(NamedTuple):
    prev: Optional[int]
    fisc: Optional[int]
    cod: int
    descrizione: str
    ore_o_giorni: Decimal
    compenso_unitario: Decimal
    trattenute: Decimal
    competenze: Decimal


class Info(NamedTuple):
    when: date
    howmuch: Optional[Decimal]
    feature: keys.Keys
    detail: Optional[InfoDetail] = None


def infoPoint(info: Info) -> InfoPoint:
    'convert an info to an infopoint'
    return InfoPoint(info.when, info.howmuch)
