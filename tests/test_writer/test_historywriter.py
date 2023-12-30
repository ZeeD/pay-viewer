from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from model import Column
from model import ColumnHeader
from model import Info
from testsupport import stub_open
from writer.historywriter import HistoryWriter


class TestHistoryWriter(TestCase):
    def test_write_infos(self) -> None:
        with stub_open('') as mock:
            HistoryWriter(Path()).write_infos(
                [
                    Info(
                        date(1982, 5, 11),
                        [Column(ColumnHeader.minimo, Decimal('1'))],
                        [],
                    )
                ]
            )

        mock().write.assert_called()
