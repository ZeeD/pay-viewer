from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase

from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.historywriter import HistoryWriter
from testsupport import stub_open


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
