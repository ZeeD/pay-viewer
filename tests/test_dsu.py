from datetime import date
from decimal import Decimal
from typing import ClassVar
from typing import override
from unittest import TestCase


class TestDSU(TestCase):
    WHENS: ClassVar[list[date]] = [
        date(2001, 1, 1),
        date(2004, 1, 1),
        date(2002, 1, 1),
        date(2003, 1, 1),
    ]
    DATA: ClassVar[list[list[Decimal]]] = [
        [Decimal(1), Decimal(90)],
        [Decimal(2), Decimal(80)],
        [Decimal(4), Decimal(70)],
        [Decimal(3), Decimal(60)],
    ]

    @override
    def setUp(self) -> None:
        self.whens = self.WHENS[:]
        self.data = [data[:] for data in self.DATA]

    def test_sort_idxs_whens(self) -> None:
        idxs = list(range(len(self.whens)))
        idxs.sort(key=self.whens.__getitem__)

        self.whens[:] = map(self.whens.__getitem__, idxs)
        self.data[:] = map(self.data.__getitem__, idxs)

        expected_whens = [
            date(2001, 1, 1),
            date(2002, 1, 1),
            date(2003, 1, 1),
            date(2004, 1, 1),
        ]
        expected_data = [
            [Decimal(1), Decimal(90)],
            [Decimal(4), Decimal(70)],
            [Decimal(3), Decimal(60)],
            [Decimal(2), Decimal(80)],
        ]

        self.assertEqual(expected_whens, self.whens)
        self.assertEqual(expected_data, self.data)

    def test_sort_idxs_data_0(self) -> None:
        index = 0

        idxs = list(range(len(self.data)))
        idxs.sort(key=lambda i: self.data[i][index])

        self.whens[:] = map(self.whens.__getitem__, idxs)
        self.data[:] = map(self.data.__getitem__, idxs)

        expected_whens = [
            date(2001, 1, 1),
            date(2004, 1, 1),
            date(2003, 1, 1),
            date(2002, 1, 1),
        ]
        expected_data = [
            [Decimal(1), Decimal(90)],
            [Decimal(2), Decimal(80)],
            [Decimal(3), Decimal(60)],
            [Decimal(4), Decimal(70)],
        ]

        self.assertEqual(expected_whens, self.whens)
        self.assertEqual(expected_data, self.data)

    def test_sort_idxs_data_1(self) -> None:
        index = 1

        idxs = list(range(len(self.data)))
        idxs.sort(key=lambda i: self.data[i][index])

        self.whens[:] = map(self.whens.__getitem__, idxs)
        self.data[:] = map(self.data.__getitem__, idxs)

        expected_whens = [
            date(2003, 1, 1),
            date(2002, 1, 1),
            date(2004, 1, 1),
            date(2001, 1, 1),
        ]
        expected_data = [
            [Decimal(3), Decimal(60)],
            [Decimal(4), Decimal(70)],
            [Decimal(2), Decimal(80)],
            [Decimal(1), Decimal(90)],
        ]

        self.assertEqual(expected_whens, self.whens)
        self.assertEqual(expected_data, self.data)

    def test_check(self) -> None:
        self.assertEqual(2003, self.whens[-1].year)
