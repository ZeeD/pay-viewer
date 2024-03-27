from datetime import date
from unittest import TestCase

from guilib.chartslider.chartslider import date2days
from guilib.chartslider.chartslider import days2date

from payviewer.qwtchartwidget.plot import days
from payviewer.qwtchartwidget.plot import months
from payviewer.qwtchartwidget.plot import normalized_xdatas
from payviewer.qwtchartwidget.plot import years


class TestNormalizedXdatas(TestCase):
    def test_normalized_xdatas(self) -> None:
        min_date = date(1982, 5, 11)
        max_date = date(1982, 5, 24)
        expected = [date(1982, 1, 1), date(1983, 1, 1)]

        actual = list(
            map(
                days2date,
                normalized_xdatas(date2days(min_date), date2days(max_date)),
            )
        )

        self.assertListEqual(expected, actual)


class TestDays(TestCase):
    def test_days(self) -> None:
        for min_date, max_date, expected in [
            (
                date(1982, 5, 11),
                date(1982, 5, 24),
                [date(1982, 5, 11), date(1982, 5, 18)],
            ),
            (
                date(1982, 5, 11),
                date(1982, 5, 25),
                [date(1982, 5, 11), date(1982, 5, 18), date(1982, 5, 25)],
            ),
        ]:
            with self.subTest(
                min_date=min_date, max_date=max_date, expected=expected
            ):
                actual = list(
                    map(
                        days2date,
                        days(date2days(min_date), date2days(max_date)),
                    )
                )

                self.assertListEqual(expected, actual)


class TestMonths(TestCase):
    def test_months(self) -> None:
        for min_date, max_date, expected in [
            (date(1982, 5, 11), date(1982, 5, 31), [date(1982, 5, 1)]),
            (
                date(1982, 5, 11),
                date(1982, 6, 1),
                [date(1982, 5, 1), date(1982, 6, 1)],
            ),
        ]:
            with self.subTest(
                min_date=min_date, max_date=max_date, expected=expected
            ):
                actual = list(
                    map(
                        days2date,
                        months(date2days(min_date), date2days(max_date)),
                    )
                )

                self.assertListEqual(expected, actual)


class TestYears(TestCase):
    def test_years(self) -> None:
        for min_date, max_date, expected in [
            (date(1982, 5, 11), date(1982, 12, 31), [date(1982, 1, 1)]),
            (
                date(1982, 5, 11),
                date(1983, 1, 1),
                [date(1982, 1, 1), date(1983, 1, 1)],
            ),
        ]:
            with self.subTest(
                min_date=min_date, max_date=max_date, expected=expected
            ):
                actual = list(
                    map(
                        days2date,
                        years(date2days(min_date), date2days(max_date)),
                    )
                )

                self.assertListEqual(expected, actual)
