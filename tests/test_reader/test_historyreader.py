from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.reader.historyreader import HistoryReader
from testsupport import stub_open


class TestHistoryReader(TestCase):
    def test_read_infos(self) -> None:
        with stub_open(
            """[{"when": "1982-05-11",
                            "columns": [{"header": "minimo",
                                         "howmuch": "1"}],
                            "additional_details": []}]"""
        ):
            [actual] = HistoryReader(Path()).read_infos()

        expected = Info(
            date(1982, 5, 11),
            [Column(ColumnHeader.minimo, Decimal(1))],
            [],
            Path('/'),
        )

        self.assertEqual(actual, expected)
