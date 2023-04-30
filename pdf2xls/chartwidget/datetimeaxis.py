from collections.abc import Iterator
from datetime import date
from datetime import datetime
from typing import cast

from PySide6.QtCharts import QCategoryAxis
from PySide6.QtCore import QDateTime
from PySide6.QtCore import QObject

from pdf2xls.dates import date2days


def first_january(d: date, *, before: bool=True) -> date:
    ret_year = d.year if before else d.year + 1

    return date(ret_year, 1, 1)


def next_first_of_the_month(day: date, *, delta_months: int=1) -> date:
    delta_years, m = divmod(day.month - 1 + delta_months, 12)

    return date(day.year + delta_years, m + 1, 1)


def create_days(begin: date, end: date, *, step: int=1) -> Iterator[date]:
    day = begin
    while True:
        yield day
        next_day = next_first_of_the_month(day, delta_months=step)
        if next_day > end:
            break
        day = next_day


class DateTimeAxis(QCategoryAxis):
    def __init__(self,
                 x_min: QDateTime,
                 x_max: QDateTime,
                 parent: QObject | None=None) -> None:
        super().__init__(parent)
        self.setLabelsPosition(
            QCategoryAxis.AxisLabelsPosition.AxisLabelsPositionOnValue)
        self.setTruncateLabels(False)

        x_min_date = cast(datetime, x_min.toPython()).date()
        x_max_date = cast(datetime, x_max.toPython()).date()

        self.setStartValue(date2days(x_min_date))

        self.min_date = first_january(x_min_date, before=True)
        self.max_date = first_january(x_max_date, before=False)

        self.setMin(date2days(self.min_date))
        self.setMax(date2days(self.max_date))

        self.reset_categories()

    def reset_categories(self) -> None:
        for label in self.categoriesLabels():
            self.remove(label)

        for step in (1, 3, 4, 6, 12, 24, 36, 48):
            days = list(create_days(self.min_date, self.max_date, step=step))
            if len(days) < 200:  # TODO find good split
                for day in days:
                    self.append(f'{day:%Y-%m-%d}', date2days(day))
                break
