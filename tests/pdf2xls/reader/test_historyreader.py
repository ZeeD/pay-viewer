from datetime import date
from decimal import Decimal
from unittest import TestCase

from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.reader.historyreader import HistoryReader

from .. import stub_open
from pathlib import Path


class TestHistoryReader(TestCase):
    def testReadInfos(self) -> None:
        with stub_open('''[{"when": "1982-05-11",
                            "columns": [{"header": "minimo",
                                         "howmuch": "1"}],
                            "additional_details": []}]'''):
            [actual] = HistoryReader(Path()).read_infos()

        expected = Info(date(1982, 5, 11),
                        [Column(ColumnHeader.minimo, Decimal("1"))],
                        [])

        self.assertEqual(actual, expected)
