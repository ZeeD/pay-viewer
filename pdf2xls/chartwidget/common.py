from datetime import date
from datetime import timedelta

from PySide6.QtCore import QDateTime


def date2days(d: date, *, epoch: date = date(1970, 1, 1)) -> int:
    return (d - epoch).days


def days2date(days: float, *, epoch: date = date(1970, 1, 1)) -> date:
    return epoch + timedelta(days=days)


def date2QDateTime(d: date, *, epoch: date = date(1970, 1, 1)) -> QDateTime:
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))


def date2millis(d: date, *, epoch: date = date(1970, 1, 1)) -> float:
    return (d - epoch).total_seconds() * 1000
