from datetime import date
from unittest import TestCase

from pdf2xls.dates import date2days
from pdf2xls.dates import days2date
from pdf2xls.qwtchartwidget.plot import days
from pdf2xls.qwtchartwidget.plot import months
from pdf2xls.qwtchartwidget.plot import normalized_xdatas
from pdf2xls.qwtchartwidget.plot import years


class TestNormalizedXdatas(TestCase):
    def testNormalizedXdatas(self) -> None:
        min_date = date(1982, 5, 11)
        max_date = date(1982, 5, 24)
        expected = [date(1982, 1, 1), date(1983, 1, 1)]

        actual = list(map(days2date,
                           normalized_xdatas(date2days(min_date),
                                             date2days(max_date))))

        self.assertListEqual(expected, actual)


class TestDays(TestCase):
    def testDays(self) -> None:
        for min_date, max_date, expected in [
            (date(1982, 5, 11), date(1982, 5, 24), [date(1982, 5, 11),
                                                    date(1982, 5, 18)]),
            (date(1982, 5, 11), date(1982, 5, 25), [date(1982, 5, 11),
                                                    date(1982, 5, 18),
                                                    date(1982, 5, 25)]),
        ]:
            with self.subTest(min_date=min_date,
                              max_date=max_date,
                              expected=expected):
                actual = list(map(days2date,
                                  days(date2days(min_date),
                                       date2days(max_date))))

                self.assertListEqual(expected, actual)


class TestMonths(TestCase):
    def testMonths(self) -> None:
        for min_date, max_date, expected in [
            (date(1982, 5, 11), date(1982, 5, 31), [date(1982, 5, 1)]),
            (date(1982, 5, 11), date(1982, 6, 1), [date(1982, 5, 1),
                                                   date(1982, 6, 1)]),
        ]:
            with self.subTest(min_date=min_date,
                              max_date=max_date,
                              expected=expected):
                actual = list(map(days2date,
                                  months(date2days(min_date),
                                         date2days(max_date))))

                self.assertListEqual(expected, actual)


class TestYears(TestCase):
    def testYears(self) -> None:
        for min_date, max_date, expected in [
            (date(1982, 5, 11), date(1982, 12, 31), [date(1982, 1, 1)]),
            (date(1982, 5, 11), date(1983, 1, 1), [date(1982, 1, 1),
                                                   date(1983, 1, 1)]),
        ]:
            with self.subTest(min_date=min_date,
                              max_date=max_date,
                              expected=expected):
                actual = list(map(days2date,
                                  years(date2days(min_date),
                                        date2days(max_date))))

                self.assertListEqual(expected, actual)
