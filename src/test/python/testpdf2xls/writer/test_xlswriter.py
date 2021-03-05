from datetime import date
from decimal import Decimal
from unittest import TestCase
from unittest.mock import patch

from pdf2xls.model import Column
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info
from pdf2xls.writer.xlswriter import XlsWriter

class TestXlsWriter(TestCase):
    def testWriteInfos(self) -> None:
        with patch('pdf2xls.writer.xlswriter.Workbook') as mock:
            XlsWriter('dummy').write_infos([
                Info(date(1982, 5, 11),
                     [Column(
                         ColumnHeader.minimo, Decimal("1"))],
                     [])
            ])

        mock.assert_called_once_with(write_only=True)
        mock().save.assert_called_once_with('dummy')
