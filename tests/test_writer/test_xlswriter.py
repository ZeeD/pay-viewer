from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.xlswriter import XlsWriter


class TestXlsWriter(TestCase):
    def test_write_infos(self) -> None:
        with patch('payviewer.writer.xlswriter.Workbook') as mock:
            XlsWriter(Path()).write_infos(
                [
                    Info(
                        date(1982, 5, 11),
                        [Column(ColumnHeader.minimo, Decimal('1'))],
                        [],
                    )
                ]
            )

        mock.assert_called_once_with(write_only=True)
        mock().save.assert_called_once_with(Path())
