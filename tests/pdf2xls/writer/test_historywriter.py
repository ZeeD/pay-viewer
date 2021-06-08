from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.writer.historywriter import HistoryWriter

from .. import stub_open


class TestHistoryWriter(TestCase):
    def testWriteInfos(self) -> None:
        with stub_open('') as mock:
            HistoryWriter(Path()).write_infos([
                Info(date(1982, 5, 11),
                     [Column(ColumnHeader.minimo, Decimal("1"))],
                     [])
            ])

        mock().write.assert_called()
