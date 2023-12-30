from datetime import date
from decimal import Decimal
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from model import Column
from model import ColumnHeader
from model import Info
from writer.xlswriter import XlsWriter


class TestXlsWriter(TestCase):
    def test_write_infos(self) -> None:
        with patch('writer.xlswriter.Workbook') as mock:
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
